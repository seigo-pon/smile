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
  detected_bboxes = face_cascade.detectMultiScale(gray, 1.1, 5)
  if len(detected_bboxes) == 0:
    return None

  detected_bbox = sorted(detected_bboxes, key=lambda x: x[2]*x[3])[0]
  bbox = Bbox(detected_bbox)

  if (gray.shape[1] * 0.4) < bbox.w or (gray.shape[0] * 0.4) < bbox.h:
    return bbox
  return None

def draw_face(frame, bbox):
  lt = (bbox.x, bbox.y)
  rb = (bbox.x + bbox.w, bbox.y + bbox.h)
  cv2.rectangle(frame, lt, rb, (0, 255, 255), thickness=2)
  return frame

def detect_smile(frame, bbox):
  if 1:
    return None
  return bbox

def draw_smile(frame, bbox):
  lt = (bbox.x, bbox.y)
  rb = (bbox.x + bbox.w, bbox.y + bbox.h)
  cv2.rectangle(frame, lt, rb, (255, 255, 0), thickness=2)
  return frame
