import cv2
import yolov5


class Model:
    def __init__(self):
        self.model = yolov5.load('moduls/yolov5s.pt')
        self.model.conf = 0.25
        self.model.iou = 0.45
        self.model.agnostic = False
        self.model.multi_label = False
        self.model.max_det = 1000

    def render(self, img):
        frame = self.model(img)
        frame.render()
        ret, buffer = cv2.imencode('.jpg', img)
        img = buffer.tobytes()
        return (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
