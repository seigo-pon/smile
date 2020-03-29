import models
from flask import Blueprint
from flask_restful import Api, Resource

api_bp = Blueprint('api', __name__, url_prefix='/api')

class Face(Resource):
    def get(self):
        return [{'id': model.rf_id, 'recognized_at': model.recognized_at.timestamp()} for model in models.get_all()]

api = Api(api_bp)
api.add_resource(Face, '/face')
