# added here as the other models imports flasks etc
import json
import uuid
import math

import application.modules.dates as mls_dates
from copy import deepcopy

class Statement:
    DEFAULT_PLANNER_EMAIL = 'planner@gmail.com'

    VERBS = {
        'read': {
            'id': 'http://activitystrea.ms/schema/1.0/read',
            'display': {'en': 'read'}
        },
        'complete': {
            'id': 'http://activitystrea.ms/schema/1.0/complete',
            'display': {'en': 'complete'}
        },
        'plan': {
            'id': 'http://www.tincanapi.co.uk/verbs/planned_learning',
            'display': {'en': 'planned'}
        },
        'enroll': {
            'id': 'http://www.tincanapi.co.uk/verbs/enrolled_onto_learning_plan',
            'display': {'en': 'enrolled onto plan'}
        },
        'watch': {
            'id': 'http://activitystrea.ms/schema/1.0/watch',
            'display': {'en': 'watch'}
        },
        'void': {
            'id': 'http://adlnet.gov/expapi/verbs/voided',
            'display': {'en': 'voided'}
        }
    }

    RESOURCE_TYPES = {
        'website': {
            'id': 'http://activitystrea.ms/schema/1.0/page',
            'name': 'website'
        },
        'book': {
            'id': 'http://id.tincanapi.com/activitytype/book',
            'name': 'book'
        },
        'elearning': {
            'id': 'http://adlnet.gov/expapi/activities/course',
            'name': 'e-learning'
        },
        'video': {
            'id': 'http://activitystrea.ms/schema/1.0/video',
            'name': 'video'
        }
    }

    def __init__(self, actor=None, verb=None, statement_obj=None, timestamp=None, grouping=None, planner_actor=None, duration=None, required=None, id=None):
        self._actor = None
        self.actor = actor
        self._verb = None
        self.verb = verb
        self._statement_obj = None
        self.statement_obj = statement_obj
        self._planned_items = []
        # only 1 for now
        self._group_id = None
        self.grouping = grouping

        self._planner_actor = None
        self.planner_actor = planner_actor
        
        self._duration = None
        self.duration = duration

        self._required = None
        self.required = required

        self._timestamp = None
        self.timestamp = timestamp

        self._id = None
        self.id = id        

    @property
    def actor(self):
        return self._actor

    @actor.setter
    def actor(self, actor):
        self._actor = self._parse_actor(actor)

    @property
    def planner_actor(self):
        return self._planner_actor

    @planner_actor.setter
    def planner_actor(self, planner_actor):
        self._planner_actor = self._parse_actor(planner_actor)

    def _parse_actor(self, actor):
        if type(actor) is dict:
            return actor.get('mbox').replace('mailto:', '')
        else:
            return actor


    @property
    def verb(self):
        return self._verb

    @verb.setter
    def verb(self, verb):
        if verb is not None:
            if type(verb) is dict:
                self._verb = verb
            else:
                self._verb = Statement.create_verb(verb)

    def get_verb_display_name(self):
        return self.verb.get('display').get('en')


    @property
    def statement_obj(self):
        return self._statement_obj

    @statement_obj.setter
    def statement_obj(self, statement_obj):
        if statement_obj is not None:
            if type(statement_obj) is dict:
                self._statement_obj = statement_obj
            else:
                self._statement_obj = Statement.create_substatement_obj(statement_obj)

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration):
        self._duration = duration

    @property
    def required(self):
        return self._required

    @required.setter
    def required(self, required):
        self._required = required

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        self._timestamp = timestamp

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def planned_items(self):
        return self._planned_items


    # GROUPING - only 1 group for now
    @property
    def grouping(self):
        return self._group_id

    @grouping.setter
    def grouping(self, grouping):
        if type(grouping) is dict:
            self._group_id = grouping.get('id')
        else:
            self._group_id = grouping

    def _grouping_to_json(self):
        return [{
            'objectType': 'Activity',
            'id': self.grouping
        }]



    def get_statement_obj_display_name(self):
        return self.statement_obj.get('definition').get('name').get('en')



    # GENERATING JSON
    def to_json(self):
        result_json = {
            'id': self.id,
            'actor': self._actor_to_json(),
            'verb': self._verb_to_json(),
            'object': self._statement_obj_to_json()
        }
        
        if self.required or self.duration:
            result_json['result'] = self._result_to_json()

        if self.grouping: #or category
            result_json['context'] = {
                'contextActivities': {
                    'grouping': self._grouping_to_json()
                }
            }
        
        result_json['timestamp'] = self.timestamp or mls_dates.get_timestamp()

        if len(self.planned_items) > 0:
            result_batch_json = []
            for plan_item in self.planned_items:
                plan_item.id = plan_item.id or Statement.create_id()

                # we are forcing learning as planner for simplicity
                ref_statement = Statement(
                    actor=self.actor,
                    verb=Statement.create_verb('plan'),
                    statement_obj=Statement.create_reference_obj(plan_item.id)).to_json()

                result_batch_json.append(ref_statement)
                result_batch_json.append(plan_item.to_json())

            result_batch_json.insert(0, result_json)
            return result_batch_json
        else:
            return result_json

    def _actor_to_json(self):
        return {
            'objectType': 'Agent',
            'mbox': 'mailto:%s' % self._actor
        }

    def _verb_to_json(self):
        return self.verb

    def _statement_obj_to_json(self):
        if type(self.statement_obj) is Statement:
            result_json = self.statement_obj.to_json()
            result_json['objectType'] = 'SubStatement'
            return result_json
        else:
            result_json = self.statement_obj

            # result_json['objectType'] = 'Activity'
            return result_json

    def _result_to_json(self):
        result_json = {}
        if self.duration is not None:
            result_json['duration'] = self.duration
        if self.required is not None:
            result_json['completion'] = self.required

        return result_json



    @classmethod
    def create_verb(cls, verb_key, name=None):
        if name:
            verb = deepcopy(Statement.VERBS.get(verb_key))
            verb['display']['en'] = name
            return verb
        else:
            return Statement.VERBS.get(verb_key)

    @classmethod
    def create_activity_obj(cls, uri, name, resource_type=None):
        result_obj = {
            'id': uri,
            'definition': {
                'name': {
                    'en': name
                }
            }
        }

        if resource_type:
            if 'http' in resource_type:
                result_obj['definition']['type'] = resource_type
            else:
                result_obj['definition']['type'] = Statement.RESOURCE_TYPES.get(resource_type).get('id')

        return result_obj

    # needs to be public?
    @classmethod
    def create_substatement_obj(cls, statement):
        return statement

    @classmethod
    def create_reference_obj(cls, statement_id):
        return {
            'objectType': 'StatementRef',
            'id': statement_id
        }

    @classmethod
    def create_id(cls):
        return str(uuid.uuid1())

    @classmethod
    def get_resource_type(cls, url):
        return next((Statement.RESOURCE_TYPES[res_key] for res_key in Statement.RESOURCE_TYPES if Statement.RESOURCE_TYPES[res_key]['id'] == url), None)


    # PLAN SPECIFIC
    @classmethod
    def create_plan(csl, plan_name, learner_actor=None, planner_actor=None, verb_name=None):
        new_plan = Statement(actor=learner_actor, planner_actor=planner_actor)
        new_plan.verb = Statement.create_verb('enroll', verb_name)
        new_plan.statement_obj = Statement.create_activity_obj(
            uri='http://www.tincanapi.co.uk/wiki/learning_plan:'+str(uuid.uuid1()),
            name=plan_name)
        return new_plan

    def add_planned_item(self, statement, verb_name=None):
        statement.grouping = self.statement_obj['id']
        statement.actor = self.actor
        self._planned_items.append(statement)




    # @classmethod
    # def from_dict(cls, json_dict):
    #     return cls(**json_dict)

    # @classmethod
    # def from_json(cls, json_str):
    #     json_dict = json.loads(json_str)
    #     return from_dict(json_dict)


class Question:
    def __init__(self, title, tag, description, guide, multichoice, choices, answer=None):
        self.title = title
        self.tag = tag
        self.description = description
        self.guide = guide
        self.is_multichoice = multichoice
        self.choices = choices
        self.answer = answer

    def get_score(self):
        score = 0
        if self.answer:
            if self.is_multichoice:
                score = math.ceil((len(self.answer)/len(self.choices)) * 5)
            else:
                # we don't have option weight so we've got to reverse scoring as 1st item is 0 but
                # it's actually the highes score at the moment - this will change
                score = math.ceil(5 - (int(self.answer.get(self.tag))/(len(self.choices)-1)) * 5)
        return score

    def get_choices_vals(self):
        return [(str(index), caption) for (index, caption) in enumerate(self.choices, start=0)]

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_dict(cls, json_dict):
        return cls(**json_dict)

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return from_dict(json_dict)

