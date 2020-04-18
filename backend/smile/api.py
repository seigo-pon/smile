from flask import Blueprint
from flask_restful import Api, Resource
from smile.models.models import FaceRecogTokenModel, FaceRecogSuccessModel, FaceRecogStateModel

api_bp = Blueprint('api', __name__, url_prefix='/api')

class FaceRecogTokenApi(Resource):
  def get(self):
    token_id = FaceRecogTokenModel.insert()

    FaceRecogStateModel.insert(token_id)

    return {'accesstoken': token_id}

class FaceRecogListApi(Resource):
  def get(self, token_id):
    token = FaceRecogTokenApi.get(token_id)
    if not token:
      return {}

    success_list = FaceRecogSuccessModel.get_all(token_id)
    return [
      {'id': x.pk, 'token': x.token_id, 'recognized_at': x.recognized_at.timestamp()} for x in success_list
    ]

class FaceRecogStateApi(Resource):
  def get(self, token_id):
    token = FaceRecogTokenApi.get(token_id)
    if not token:
      return {}

    state = FaceRecogStateModel.get(token_id)
    return {'id': state.pk, 'state': state.value}

api = Api(api_bp)
api.add_resource(FaceRecogTokenApi, '/face/token')
api.add_resource(FaceRecogListApi, '/face/list/<string:token_id>')
api.add_resource(FaceRecogStateApi, '/face/state/<string:token_id>')
