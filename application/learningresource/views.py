from flask import (
    Blueprint,
    render_template,
    redirect,
    flash,
    url_for,
    request,
    current_app,
    jsonify
)

from flask.ext.security import login_required
from flask.ext.login import current_user
import json

import application.modules.lr_service as lr_service


learningresource = Blueprint('learningresource', __name__)

@learningresource.route('/learning-resource/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        filterJson = request.get_json()
        current_app.logger.info(filterJson)
        current_app.logger.info(filterJson['filter'])
        current_app.logger.info(type(filterJson['filter']))

        current_app.logger.info('getting items')
        try:
            courses = lr_service.get_courses(filterJson)    
        except Exception as e:
            current_app.logger.exception(e, exc_info=True)
            raise
        current_app.logger.info('got items')
        return json.dumps(courses)

    return render_template('learningresource/search.html')

@learningresource.route('/learning-resource/course/<resource_id>')
def view_resource(resource_id):
    course = lr_service.get_resource(resource_id)
    return render_template('learningresource/view_resource.html', course=course)

# API
@learningresource.route('/api/learning-resource/course/<resource_id>')
def api_view_resource(resource_id):
    course = lr_service.get_resource(resource_id)
    return jsonify(course)
