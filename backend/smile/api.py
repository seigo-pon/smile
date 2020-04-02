from flask import Blueprint
from flask_restful import Api, Resource
from smile.models.models import FaceRecogSuccessModel, FaceRecogStateModel

api_bp = Blueprint('api', __name__, url_prefix='/api')

class FaceRecogListApi(Resource):
  def get(self):
    success_list = FaceRecogSuccessModel.get_all()
    return [
      {'id': x.pk, 'recognized_at': x.recognized_at.timestamp()} for x in success_list
    ]

class FaceRecogStateApi(Resource):
  def get(self):
    state = FaceRecogStateModel.get()
    return {'id': state.pk, 'state': state.value}

api = Api(api_bp)
api.add_resource(FaceRecogListApi, '/face/list')
api.add_resource(FaceRecogStateApi, '/face/state')
