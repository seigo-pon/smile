import cv2
import time

class FaceCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        ret, jpg = cv2.imencode('.jpg', image)
        return jpg.tobytes()

def gen(face_camera):
    while True:
        frame = face_camera.get_frame()
        yield b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
        time.sleep(0.2)
