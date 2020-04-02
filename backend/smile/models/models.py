from datetime import datetime
from enum import IntEnum
from smile.database import db

class FaceRecogSuccessModel(db.Model):
  __tablename__ = 'face_recog_success'

  pk = db.Column(db.Integer, primary_key=True)
  recognized_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

  @staticmethod
  def get_all():
    return FaceRecogSuccessModel.query.order_by(FaceRecogSuccessModel.pk).all()

  @staticmethod
  def insert():
    success = FaceRecogSuccessModel()

    db.session.add(success)
    db.session.commit()

class FaceRecogState(IntEnum):
  NO_FACE = 0
  DETECT_FACE = 1
  DETECT_SMILE = 2
  SUCCESS = 3
  FAIL = 4

class FaceRecogStateModel(db.Model):
  __tablename__ = 'face_recog_state'

  pk = db.Column(db.Integer, primary_key=True)
  value = db.Column(db.Integer, nullable=False, default=int(FaceRecogState.NO_FACE))
  recognized_at = db.Column(db.DateTime, nullable=True)
  updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

  @staticmethod
  def get():
    return db.session.query(FaceRecogStateModel).one_or_none()

  @staticmethod
  def insert():
    state = FaceRecogStateModel()

    db.session.add(state)
    db.session.commit()

  @staticmethod
  def update(new_state, recognized_at):
    state = FaceRecogStateModel.get()
    if FaceRecogState(state.value) == new_state:
      return

    state.value = int(new_state)
    state.recognized_at = recognized_at
    state.updated_at = datetime.now()

    db.session.add(state)
    db.session.commit()
