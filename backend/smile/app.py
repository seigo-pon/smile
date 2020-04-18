import logging
import os
import time
from datetime import datetime
from flask import Flask, render_template, Response
from smile.api import api_bp
from smile.database import init_db
from smile.face_image import gen_face_image
from smile.models.models import FaceRecogState, FaceRecogStateModel

def create_app():
  app = Flask(__name__, static_folder='../../front/dist/static', template_folder='../../front/dist')

  app.config['SECRET_KEY'] = os.urandom(24)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  app.register_blueprint(api_bp)

  logging.basicConfig(level=logging.DEBUG)

  with app.app_context():
    init_db(app)

  return app

app = create_app()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
  return render_template('index.html')

@app.route('/face/camera/<token_id>')
def face_camera(token_id):
  return Response(gen_face_image(app, token_id), mimetype='multipart/x-mixed-replace; boudary=frame')
