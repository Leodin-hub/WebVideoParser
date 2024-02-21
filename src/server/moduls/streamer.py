import sys
sys.path.append('../server')
from library.helpers.redis_connect import RedisConnect
from library.helpers.kafka_function import get_consumer
from library.global_variables import gen_img
import asyncio


class Streamer:
    def __init__(self):
        self.consumer = get_consumer('detection')
        self.redis = RedisConnect(False)
        self.img = gen_img('Wait to stream')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.consumer.unsubscribe()

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
