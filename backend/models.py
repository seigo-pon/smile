from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FaceRecognitionModel(db.Model):
  __tablename__ = 'face_recognition'

  rf_id = db.Column(db.Integer, primary_key=True)
  recognized_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

def init_db(app):
  db.init_app(app)
  db.create_all()

def get_all():
  return FaceRecognitionModel.query.order_by(FaceRecognitionModel.rf_id).all()

def insert():
  model = FaceRecognitionModel()
  db.session.add(model)
  db.session.commit()
