from flask import Blueprint
from flask_restful import Api, Resource
from smile.models.models import FaceRecognitionSuccessModel, FaceRecognitionStateModel

api_bp = Blueprint('api', __name__, url_prefix='/api')

class FaceRecognitionSuccessList(Resource):
  def get(self):
    success_list = FaceRecognitionSuccessModel.get_all()
    return [
      {'id': x.pk, 'recognized_at': x.recognized_at.timestamp()} for x in success_list
    ]

class CurrentFaceRecognitionState(Resource):
  def get(self):
    state = FaceRecognitionStateModel.get()
    return {'id': state.pk, 'current': state.current}

api = Api(api_bp)
api.add_resource(FaceRecognitionSuccessList, '/recoglist')
api.add_resource(CurrentFaceRecognitionState, '/recogstate')
