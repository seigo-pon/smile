import api
import camera
import models
import time
from flask import Flask, render_template, Response

app = Flask(__name__, static_folder='../front/dist/static', template_folder='../front/dist')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.register_blueprint(api.api_bp)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
  return render_template('index.html')

@app.route('/face_camera')
def face_camera():
  return Response(camera.gen(camera.FaceCamera()), mimetype='multipart/x-mixed-replace; boudary=frame')

if __name__ == '__main__':
  with app.app_context():
    models.init_db(app)

    if models.get_face_recognition_state() is None:
      models.insert_face_recognition_state()
    models.update_face_recognition_state(models.FaceRecognitionState.PREPARE)

  app.run()

