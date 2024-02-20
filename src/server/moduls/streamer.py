import sys
sys.path.append('../server')
from moduls.redis_connect import RedisConnect
from kafka import KafkaConsumer
import numpy as np
import asyncio
import cv2


def gen_img(text: str):
    img = np.zeros((640, 1080, 3), np.uint8)
    cv2.putText(img, text, (160, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_encode = cv2.imencode('.jpg', img)[1]
    img_bytes = img_encode.tobytes()
    return img_bytes


class Streamer:
    def __init__(self):
        self.consumer = KafkaConsumer('detection', group_id='group3', bootstrap_servers=['localhost:9092'],
                                      auto_offset_reset='earliest')
        self.redis = RedisConnect(False)
        self.img = gen_img('Wait to stream')

    async def get_img(self):
        while True:
            msg = self.consumer.poll()
            if msg:
                value = ''
                for m in msg:
                    value = msg[m][0].value.decode('utf-8')
                img = self.redis.get(value)
                if img is not None:
                    self.img = img
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + self.img + b'\r\n')
            await asyncio.sleep(0.02)
