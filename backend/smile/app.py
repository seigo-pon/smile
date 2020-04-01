import logging
import time
from datetime import datetime
from flask import Flask, render_template, Response
from smile.api import api_bp
from smile.database import init_db
from smile.live_face import gen_live_face
from smile.models.models import FaceRecognitionState, FaceRecognitionStateModel

def create_app():
  app = Flask(__name__, static_folder='../../front/dist/static', template_folder='../../front/dist')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.register_blueprint(api_bp)
  logging.basicConfig(level=logging.DEBUG)

  with app.app_context():
    init_db(app)

    if FaceRecognitionStateModel.get() is None:
      FaceRecognitionStateModel.insert()
    FaceRecognitionStateModel.update(FaceRecognitionState.NO_FACE, None)

  return app

app = create_app()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
  return render_template('index.html')

@app.route('/liveface')
def live_face():
  return Response(gen_live_face(app), mimetype='multipart/x-mixed-replace; boudary=frame')
