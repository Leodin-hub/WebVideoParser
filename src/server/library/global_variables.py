import numpy as np
import cv2

PORT_KAFKA = 'localhost:9092'
REDIS_PORT = {'host': 'localhost', 'port': 6379}
RUN_PORT = {'host': '127.0.0.1', 'port': 8080}


def gen_img(text: str):
    img = np.zeros((640, 1080, 3), np.uint8)
    cv2.putText(img, text, (160, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_encode = cv2.imencode('.jpg', img)[1]
    return img_encode.tobytes()
