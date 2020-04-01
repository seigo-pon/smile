import time
from datetime import datetime
from flask import Blueprint, current_app, Response
from smile.module.camera import LiveCamera, LiveCameraError, frame_to_jpeg
from smile.module.vision import detect_face, draw_face, detect_smile, draw_smile
from smile.models.models import FaceRecognitionState, FaceRecognitionStateModel

def get_recog_state(app):
  state = FaceRecognitionState.NO_FACE
  with app.app_context():
    state = FaceRecognitionStateModel.get()
  return state

def update_recog_state(app, state, recognized_at):
  with app.app_context():
    FaceRecognitionStateModel.update(state, recognized_at)

def is_over_time(src, dest, interval):
  if src is None or dest is None:
    return False
  return (dest - src).seconds > interval

def gen_live_face(app):
  try:
    live_camera = LiveCamera()

    while True:
      frame = live_camera.get_frame()
      if frame is not None:
        state = get_recog_state(app)
        now = datetime.now()

        if state.current == FaceRecognitionState.FAIL:
          if is_over_time(state.recognized_at, now, 5):
            update_recog_state(app, FaceRecognitionState.NO_FACE, None)

        elif state.current == FaceRecognitionState.NO_FACE:
          bbox = detect_face(frame)
          if bbox is not None:
            frame = draw_face(frame, bbox)

            update_recog_state(app, FaceRecognitionState.DETECT_FACE, now)

        elif state.current == FaceRecognitionState.DETECT_FACE:
          bbox = detect_face(frame)
          if bbox is not None:
            frame = draw_face(frame, bbox)

            if is_over_time(state.recognized_at, now, 5):
              update_recog_state(app, FaceRecognitionState.DETECT_SMILE, now)
          else:
            if is_over_time(state.recognized_at, now, 5):
              update_recog_state(app, FaceRecognitionState.FAIL, now)

        elif state.current == FaceRecognitionState.DETECT_SMILE:
          face_bbox = detect_face(frame)
          if face_bbox is not None:
            frame = draw_face(frame, face_bbox)

            smile_bbox = detect_smile(frame, face_bbox)
            if smile_bbox is not None:
              frame = draw_smile(frame, smile_bbox)

              if is_over_time(state.recognized_at, now, 5):
                update_recog_state(app, FaceRecognitionState.DETECT_SMILE, now)
            else:
              if is_over_time(state.recognized_at, now, 5):
                update_recog_state(app, FaceRecognitionState.FAIL, now)
          else:
            if is_over_time(state.recognized_at, now, 5):
              update_recog_state(app, FaceRecognitionState.FAIL, now)

        yield b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + frame_to_jpeg(frame) + b'\r\n\r\n'
      else:
        yield ''

      time.sleep(0.5)
  except LiveCameraError as e:
    print(e)
    yield ''
