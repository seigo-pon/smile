from datetime import datetime
from enum import IntEnum
from smile.database import db

class FaceRecognitionSuccessModel(db.Model):
  __tablename__ = 'face_recognition_success'

  pk = db.Column(db.Integer, primary_key=True)
  recognized_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

  @staticmethod
  def get_all():
    return FaceRecognitionSuccessModel.query.order_by(FaceRecognitionSuccessModel.pk).all()

  @staticmethod
  def insert():
    success = FaceRecognitionSuccessModel()

    db.session.add(success)
    db.session.commit()

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

  @staticmethod
  def get():
    return db.session.query(FaceRecognitionStateModel).one_or_none()

  @staticmethod
  def insert():
    state = FaceRecognitionStateModel()

    db.session.add(state)
    db.session.commit()

  @staticmethod
  def update(new_state, recognized_at):
    state = FaceRecognitionStateModel.get()
    if FaceRecognitionState(state.current) == new_state:
      return

    state.current = int(new_state)
    state.recognized_at = recognized_at
    state.updated_at = datetime.now()

    db.session.add(state)
    db.session.commit()
