import uuid
from datetime import datetime
from enum import IntEnum
from smile.database import db

class FaceRecogTokenModel(db.Model):
  __tablename__ = 'face_recog_token'

  pk = db.Column(db.Integer, primary_key=True)
  token_id = db.Column(db.String(256))
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

  @staticmethod
  def get(token_id):
    return FaceRecogSuccessModel.query.filter(FaceRecogTokenModel.token_id == token_id).first()

  @staticmethod
  def insert():
    token = FaceRecogTokenModel()

    token_id = str(uuid.uuid4())
    token.token_id = token_id

    db.session.add(token)
    db.session.commit()

    return token_id

class FaceRecogSuccessModel(db.Model):
  __tablename__ = 'face_recog_success'

  pk = db.Column(db.Integer, primary_key=True)
  token_id = db.Column(db.String(256))
  recognized_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

  @staticmethod
  def get_all():
    return FaceRecogSuccessModel.query.order_by(FaceRecogSuccessModel.pk).all()

  @staticmethod
  def insert(token_id):
    success = FaceRecogSuccessModel()

    success.token_id = token_id

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
  token_id = db.Column(db.String(256))
  value = db.Column(db.Integer, nullable=False, default=int(FaceRecogState.NO_FACE))
  recognized_at = db.Column(db.DateTime, nullable=True)
  updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

  @staticmethod
  def get(token_id):
    return db.session.query(FaceRecogStateModel).filter(FaceRecogStateModel.token_id == token_id).one_or_none()

  @staticmethod
  def insert(token_id):
    state = FaceRecogStateModel()

    state.token_id = token_id

    db.session.add(state)
    db.session.commit()

  @staticmethod
  def update(token_id, new_state, recognized_at):
    state = FaceRecogStateModel.get(token_id)
    if FaceRecogState(state.value) == new_state:
      return

    state.value = int(new_state)
    state.recognized_at = recognized_at
    state.updated_at = datetime.now()

    db.session.add(state)
    db.session.commit()
