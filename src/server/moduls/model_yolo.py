import numpy as np
import yolov5
import cv2


class Model:
    def __init__(self):
        self.model = yolov5.load('moduls/yolov5s.pt')
        self.model.conf = 0.25
        self.model.iou = 0.45
        self.model.agnostic = False
        self.model.multi_label = False
        self.model.max_det = 1000

    def render(self, img):
        img = np.frombuffer(img, np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        frame = self.model(img)
        frame.render()
        buffer = cv2.imencode('.jpg', img)[1]
        return buffer.tobytes()
