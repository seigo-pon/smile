import cv2
import models
import time

class FaceCamera(object):
  def __init__(self):
    self.video = cv2.VideoCapture(0)
  
  def __del__(self):
    self.video.release()
  
  def get_frame(self):
    success, frame = self.video.read()
    return cv2.flip(frame, 1) if success else None

def detect_face(frame):
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
  detected_faces = face_cascade.detectMultiScale(gray, 1.1, 5)
  if len(detected_faces) == 0:
    return None

  detected_face = sorted(detected_faces, key=lambda x: x[2]+x[3])[0]
  if len(detected_face) != 4:
    return None

  return detected_face

def draw_face(frame, detected_face):
  x = int(detected_face[0])
  y = int(detected_face[1])
  w = int(detected_face[2])
  h = int(detected_face[3])
  cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
  return frame

def jpeg(frame):
  params = [int(cv2.IMWRITE_JPEG_QUALITY), 85]
  ret, jpg = cv2.imencode('.jpg', frame, params)
  return jpg.tobytes() if ret else None

def gen(face_camera):
  while True:
    frame = face_camera.get_frame()
    if frame is not None:
      detected_face = detect_face(frame)
      if detected_face is not None:
        # models.update_face_recognition_state(models.FaceRecognitionState.START)
        frame = draw_face(frame, detected_face)
      # else:
        # models.update_face_recognition_state(models.FaceRecognitionState.PREPARE)

      yield b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + jpeg(frame) + b'\r\n\r\n'
    else:
      yield ""

    time.sleep(0.2)
