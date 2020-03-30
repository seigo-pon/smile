import cv2
import models
import time
from datetime import datetime
from flask import Flask

class FaceCamera(object):
  def __init__(self):
    self.capture = cv2.VideoCapture(0)
    self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
  
  def __del__(self):
    self.capture.release()
  
  def get_frame(self):
    success, frame = self.capture.read()
    return cv2.flip(frame, 1) if success else None

class FaceFrame(object):
  def __init__(self, face):
    self.x = int(face[0])
    self.y = int(face[1])
    self.w = int(face[2])
    self.h = int(face[3])

def detect_face(frame):
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
  detected_faces = face_cascade.detectMultiScale(gray, 1.1, 5)
  if len(detected_faces) == 0:
    return None

  detected_face = sorted(detected_faces, key=lambda x: x[2]*x[3])[0]
  face_frame = FaceFrame(detected_face)

  if (gray.shape[1] * 0.4) < face_frame.w or (gray.shape[0] * 0.4) < face_frame.h:
    return face_frame
  return None

def draw_face(frame, face_frame):
  lt = (face_frame.x, face_frame.y)
  rb = (face_frame.x + face_frame.w, face_frame.y + face_frame.h)
  cv2.rectangle(frame, lt, rb, (0, 255, 255), thickness=2)
  return frame

def detect_smile(frame, face_frame):
  if 0:
    return face_frame
  return None

def draw_smile(frame, smile_frame):
  lt = (smile_frame.x, smile_frame.y)
  rb = (smile_frame.x + smile_frame.w, smile_frame.y + smile_frame.h)
  cv2.rectangle(frame, lt, rb, (255, 255, 0), thickness=2)
  return frame

def to_jpeg(frame):
  params = [int(cv2.IMWRITE_JPEG_QUALITY), 85]
  ret, jpg = cv2.imencode('.jpg', frame, params)
  return jpg.tobytes() if ret else None

def get_state(app):
  state = models.FaceRecognitionState.NO_FACE
  with app.app_context():
    state = models.get_face_recognition_state()
  return state

def update_state(app, state, recognized_at):
  with app.app_context():
    models.update_face_recognition_state(state, recognized_at)

def is_over_time(src, dest, interval):
  if src is None or dest is None:
    return False
  return (dest - src).seconds > interval

def gen(app, face_camera):
  while True:
    frame = face_camera.get_frame()
    if frame is not None:
      state = get_state(app)
      now = datetime.now()

      if state.current == models.FaceRecognitionState.FAIL:
        if is_over_time(state.recognized_at, now, 5):
          update_state(app, models.FaceRecognitionState.NO_FACE, None)
      if state.current == models.FaceRecognitionState.NO_FACE:
        face_frame = detect_face(frame)
        if face_frame is not None:
          frame = draw_face(frame, face_frame)

          if is_over_time(state.recognized_at, now, 5):
            update_state(app, models.FaceRecognitionState.DETECT_FACE, now)
      elif state.current == models.FaceRecognitionState.DETECT_FACE:
        face_frame = detect_face(frame)
        if face_frame is not None:
          frame = draw_face(frame, face_frame)

          if is_over_time(state.recognized_at, now, 5):
            update_state(app, models.FaceRecognitionState.DETECT_SMILE, now)
        else:
          if is_over_time(state.recognized_at, now, 5):
            update_state(app, models.FaceRecognitionState.FAIL, now)
      elif state.current == models.FaceRecognitionState.DETECT_SMILE:
        face_frame = detect_face(frame)
        if face_frame is not None:
          frame = draw_face(frame, face_frame)

          smile_frame = detect_smile(frame, face_frame)
          if smile_frame is not None:
            frame = draw_smile(frame, smile_frame)

            if is_over_time(state.recognized_at, now, 5):
              update_state(app, models.FaceRecognitionState.DETECT_SMILE, now)
          else:
            if is_over_time(state.recognized_at, now, 5):
              update_state(app, models.FaceRecognitionState.FAIL, now)
        else:
          if is_over_time(state.recognized_at, now, 5):
            update_state(app, models.FaceRecognitionState.FAIL, now)

      yield b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + to_jpeg(frame) + b'\r\n\r\n'
    else:
      yield ""

    time.sleep(0.2)
