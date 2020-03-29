import models
from flask import Blueprint
from flask_restful import Api, Resource

api_bp = Blueprint('api', __name__, url_prefix='/api')

class LastFaceRecognitionSuccessList(Resource):
  def get(self):
    success_list = models.get_face_recognition_success_all()
    return [
      {'id': success.pk, 'recognized_at': success.recognized_at.timestamp()} for success in success_list
    ]

class CurrentFaceRecognitionState(Resource):
  def get(self):
    state = models.get_face_recognition_state()
    return {'id': state.pk, 'state': state.current}

api = Api(api_bp)
api.add_resource(LastFaceRecognitionSuccessList, '/last_list')
api.add_resource(CurrentFaceRecognitionState, '/state')
