import sys
sys.path.append('../server')
import asyncio
from moduls.kafka_base import KafkaBase


class Streamer(KafkaBase):
    def __init__(self):
        super().__init__('stream')
        self.camera.generic_img = self.camera.gen_img('Wait to stream')

    def get_img(self):
        while True:
            msg = self.consumer.poll()
            if msg:
                value = ''
                for m in msg:
                    value = msg[m][0].value.decode('utf-8')
                return self.redis.get(value)
            else:
                return self.camera.generic_img
