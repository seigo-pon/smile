import cv2

class LiveCameraError(Exception):
  pass

class LiveCamera(object):
  def __init__(self):
    self.capture = cv2.VideoCapture(0)
    if not self.capture.isOpened():
      raise LiveCameraError('Fail camera open.')

    self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
  
  def __del__(self):
    self.capture.release()
  
  def get_frame(self):
    success, frame = self.capture.read()
    return cv2.flip(frame, 1) if success else None

def frame_to_jpeg(frame):
  params = [int(cv2.IMWRITE_JPEG_QUALITY), 85]
  ret, jpg = cv2.imencode('.jpg', frame, params)
  return jpg.tobytes() if ret else None
