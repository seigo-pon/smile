import time
from abc import *
from datetime import datetime
from smile.module.camera import LiveCamera, LiveCameraError, frame_to_jpeg
from smile.module.vision import detect_face, draw_face, detect_smile, draw_smile
from smile.models.models import FaceRecogState, FaceRecogStateModel

class FaceRecogAction(metaclass=ABCMeta):
  @abstractmethod
  def do(self, app, frame):
    pass

class FaceRecogNoFaceAction(FaceRecogAction):
  def do(self, app, frame):
    now = datetime.now()
    action = FaceRecogNoFaceAction()

    bbox = detect_face(frame)
    if bbox is not None:
      frame = draw_face(frame, bbox)

      update_recog_state(app, FaceRecogState.DETECT_FACE, now)
      action = FaceRecogDetectFaceAction()

    return (action, frame)

class FaceRecogDetectFaceAction(FaceRecogAction):
  def do(self, app, frame):
    state = get_recog_state(app)
    now = datetime.now()
    action = FaceRecogDetectFaceAction()

    bbox = detect_face(frame)
    if bbox is not None:
      frame = draw_face(frame, bbox)

      if is_over_time(state.recognized_at, now, 5):
        update_recog_state(app, FaceRecogState.DETECT_SMILE, now)
        action = FaceRecogDetectSmileAction()
    else:
      if is_over_time(state.recognized_at, now, 5):
        update_recog_state(app, FaceRecogState.FAIL, now)
        action = FaceRecogFailAction()

    return (action, frame)

class FaceRecogDetectSmileAction(FaceRecogAction):
  def do(self, app, frame):
    state = get_recog_state(app)
    now = datetime.now()
    action = FaceRecogDetectSmileAction()

    face_bbox = detect_face(frame)
    if face_bbox is not None:
      frame = draw_face(frame, face_bbox)

      smile_bbox = detect_smile(frame, face_bbox)
      if smile_bbox is not None:
        frame = draw_smile(frame, smile_bbox)

        if is_over_time(state.recognized_at, now, 5):
          update_recog_state(app, FaceRecogState.SUCCESS, now)
          action = FaceRecogSuccessAction()
      else:
        if is_over_time(state.recognized_at, now, 5):
          update_recog_state(app, FaceRecogState.FAIL, now)
          action = FaceRecogFailAction()
    else:
      if is_over_time(state.recognized_at, now, 5):
        update_recog_state(app, FaceRecogState.FAIL, now)
        action = FaceRecogFailAction()

    return (action, frame)

class FaceRecogSuccessAction(FaceRecogAction):
  def do(self, app, frame):
    state = get_recog_state(app)
    now = datetime.now()
    action = FaceRecogSuccessAction()

    face_bbox = detect_face(frame)
    if face_bbox is not None:
      frame = draw_face(frame, face_bbox)

      smile_bbox = detect_smile(frame, face_bbox)
      if smile_bbox is not None:
        frame = draw_smile(frame, smile_bbox)

    if is_over_time(state.recognized_at, now, 5):
      update_recog_state(app, FaceRecogState.NO_FACE, None)
      action = FaceRecogNoFaceAction()

    return (action, frame)

class FaceRecogFailAction(FaceRecogAction):
  def do(self, app, frame):
    state = get_recog_state(app)
    now = datetime.now()
    action = FaceRecogFailAction()

    if is_over_time(state.recognized_at, now, 5):
      update_recog_state(app, FaceRecogState.NO_FACE, None)
      action = FaceRecogNoFaceAction()

    return (action, frame)

def get_recog_state(app):
  state = FaceRecogState.NO_FACE
  with app.app_context():
    state = FaceRecogStateModel.get()
  return state

def update_recog_state(app, state, recognized_at):
  with app.app_context():
    FaceRecogStateModel.update(state, recognized_at)

def is_over_time(src, dest, interval):
  if src is None or dest is None:
    return False
  return (dest - src).seconds > interval

def gen_face_image(app):
  try:
    live_camera = LiveCamera()
    action = FaceRecogNoFaceAction()

    while True:
      frame = live_camera.get_frame()
      if frame is not None:
        action, frame = action.do(app, frame)
        yield b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + frame_to_jpeg(frame) + b'\r\n\r\n'
      else:
        yield ''

      time.sleep(0.5)

  except LiveCameraError as e:
    print(e)
    yield ''
