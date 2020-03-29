import api
import camera
import models
import time
from flask import Flask, render_template, Response

app = Flask(__name__, static_folder='../front/dist/static', template_folder='../front/dist')
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
    if not models.get_all():
      models.insert()

  app.run()

