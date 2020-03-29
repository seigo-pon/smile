from datetime import datetime
from enum import IntEnum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FaceRecognitionSuccessModel(db.Model):
  __tablename__ = 'face_recognition_success'

  pk = db.Column(db.Integer, primary_key=True)
  recognized_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

class FaceRecognitionState(IntEnum):
  PREPARE = 1
  START = 2
  SUCCESS = 3
  FAILE = 4

class FaceRecognitionStateModel(db.Model):
  __tablename__ = 'face_recognition_state'

  pk = db.Column(db.Integer, primary_key=True)
  current = db.Column(db.Integer, nullable=False, default=int(FaceRecognitionState.PREPARE))
  updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

def init_db(app):
  db.init_app(app)
  db.create_all()

def get_face_recognition_success_all():
  return FaceRecognitionSuccessModel.query.order_by(FaceRecognitionSuccessModel.pk).all()

def insert_face_recognition_success():
  success = FaceRecognitionSuccessModel()
  db.session.add(success)
  db.session.commit()

def get_face_recognition_state():
  return db.session.query(FaceRecognitionStateModel).one_or_none()

def insert_face_recognition_state():
  state = FaceRecognitionStateModel()
  print(f"state = {state}")
  db.session.add(state)
  db.session.commit()

def update_face_recognition_state(current_state):
  state = get_face_recognition_state()
  state.current = int(current_state)
  db.session.add(state)
  db.session.commit()
