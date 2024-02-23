from loguru import logger
import numpy as np
import yolov5
import cv2


class Model:
    """A class for using YOLOv5 model to detect objects in images.

    Attributes:
        model: The YOLOv5 model loaded from a specified path.
        conf: The confidence threshold for object detection.
        iou: The intersection over union threshold.
        agnostic: Boolean value to determine whether to use class-agnostic detection.
        multi_label: Boolean value to determine whether to allow multi-label classification.
        max_det: The maximum number of detections to consider.

    Methods:
        __init__: Initializes the Model class with default YOLOv5 model parameters.
        render: Processes an image using the YOLOv5 model and returns the processed image buffer.
    """
    @logger.catch(level='INFO')
    def __init__(self):
        """Initializes the Model class with default YOLOv5 model parameters.
        """
        self.model = yolov5.load('moduls/yolov5s.pt')
        self.model.conf = 0.25
        self.model.iou = 0.45
        self.model.agnostic = False
        self.model.multi_label = False
        self.model.max_det = 1000

    @logger.catch(level='INFO')
    def render(self, img):
        """Processes an image using the YOLOv5 model and returns the processed image buffer.

        Args:
            img: The input image data as a bytes-like object.

        Returns:
            buffer: The processed image buffer as a bytes-like object.
        """
        img = np.frombuffer(img, np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        frame = self.model(img)
        frame.render()
        buffer = cv2.imencode('.jpg', img)[1]
        return buffer.tobytes()
