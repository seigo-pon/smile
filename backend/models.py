from datetime import datetime
from enum import IntEnum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FaceRecognitionSuccessModel(db.Model):
  __tablename__ = 'face_recognition_success'

  pk = db.Column(db.Integer, primary_key=True)
  recognized_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

class FaceRecognitionState(IntEnum):
  PREPARE = 0
  START = 1
  SUCCESS = 2
  FAIL = 3

class FaceRecognitionStateModel(db.Model):
  __tablename__ = 'face_recognition_state'

  pk = db.Column(db.Integer, primary_key=True)
  current = db.Column(db.Integer, nullable=False, default=int(FaceRecognitionState.PREPARE))
  recognized_at = db.Column(db.DateTime, nullable=True)
  succeed_at = db.Column(db.DateTime, nullable=True)
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

def update_face_recognition_state(current_state):
  state = get_face_recognition_state()

  if current_state == FaceRecognitionState.PREPARE:
    state.recognized_at = None
    state.succeed_at = None
  elif current_state == FaceRecognitionState.START:
    if state.recognized_at is None:
      state.recognized_at = datetime.now()
  elif current_state == FaceRecognitionState.SUCCESS:
    if state.succeed_at is None:
      state.succeed_at = datetime.now()

  state.current = int(current_state)
  state.updated_at = datetime.now()

  db.session.add(state)
  db.session.commit()
