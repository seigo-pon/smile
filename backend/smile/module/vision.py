import cv2

class Bbox(object):
  def __init__(self, bbox):
    self.x = int(bbox[0])
    self.y = int(bbox[1])
    self.w = int(bbox[2])
    self.h = int(bbox[3])

def detect_face(frame):
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
  face_min_size = (int(gray.shape[1]*0.4), int(gray.shape[0]*0.6))
  detected_bboxes = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=face_min_size)
  if len(detected_bboxes) == 0:
    return None

  detected_bbox = sorted(detected_bboxes, key=lambda x: x[2]*x[3])[0]
  return Bbox(detected_bbox)

def draw_face(frame, bbox):
  lt = (bbox.x, bbox.y)
  rb = (bbox.x+bbox.w, bbox.y+bbox.h)
  cv2.rectangle(frame, lt, rb, (0, 255, 255), thickness=2)
  return frame

def detect_smile(frame, bbox):
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  gray_face = gray[bbox.y:bbox.y+bbox.h, bbox.x:bbox.x+bbox.w]

  smile_cascade = cv2.CascadeClassifier('./data/haarcascade_smile.xml')
  smile_min_size = (int(bbox.w*0.2), int(bbox.h*0.2))
  detected_bboxes = smile_cascade.detectMultiScale(gray_face, scaleFactor=1.2, minNeighbors=10, minSize=smile_min_size)
  if len(detected_bboxes) == 0:
    return None

  detected_bbox = sorted(detected_bboxes, key=lambda x: x[2]*x[3])[0]
  return Bbox(detected_bbox)

def draw_smile(frame, face_bbox, bbox):
  lt = (face_bbox.x+bbox.x, face_bbox.y+bbox.y)
  rb = (face_bbox.x+bbox.x+bbox.w, face_bbox.y+bbox.y+bbox.h)
  cv2.rectangle(frame, lt, rb, (255, 255, 0), thickness=2)
  return frame
