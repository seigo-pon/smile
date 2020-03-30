from datetime import datetime
from enum import IntEnum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FaceRecognitionSuccessModel(db.Model):
  __tablename__ = 'face_recognition_success'

  pk = db.Column(db.Integer, primary_key=True)
  recognized_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

class FaceRecognitionState(IntEnum):
  NO_FACE = 0
  DETECT_FACE = 1
  DETECT_SMILE = 2
  SUCCESS = 3
  FAIL = 4

class FaceRecognitionStateModel(db.Model):
  __tablename__ = 'face_recognition_state'

  pk = db.Column(db.Integer, primary_key=True)
  current = db.Column(db.Integer, nullable=False, default=int(FaceRecognitionState.NO_FACE))
  recognized_at = db.Column(db.DateTime, nullable=True)
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

  db.session.add(state)
  db.session.commit()

def update_face_recognition_state(new_state, recognized_at):
  state = get_face_recognition_state()
  if FaceRecognitionState(state.current) == new_state:
    return

  state.current = int(new_state)
  state.recognized_at = recognized_at
  state.updated_at = datetime.now()

  db.session.add(state)
  db.session.commit()
