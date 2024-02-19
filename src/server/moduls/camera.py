import numpy as np
import asyncio
import cv2


class Camera:
    def __init__(self):
        self.camera = cv2.VideoCapture()
        self.generic_img = None
        self.url_connect = ''

    @staticmethod
    def gen_img(text: str):
        img = np.zeros((640, 1080, 3), np.uint8)
        cv2.putText(img, text, (160, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_encode = cv2.imencode('.jpg', img)[1]
        img_bytes = img_encode.tobytes()
        return img_bytes

    def connect_url(self, url_video):
        if url_video != self.url_connect:
            self.camera = cv2.VideoCapture(url_video)
            self.url_connect = url_video

    async def stream(self):
        while True:
            success, frame = self.camera.read()
            if success:
                yield frame.tobytes()
            else:
                yield None
            await asyncio.sleep(0.01)
