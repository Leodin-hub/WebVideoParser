import sys
sys.path.append('../server')
from kafka import KafkaProducer, KafkaConsumer
from moduls.redis_connect import RedisConnect
from moduls.model_yolo import Model
import asyncio

class Detector:
    def __init__(self):
        self.consumer = KafkaConsumer('stream', group_id='group2', bootstrap_servers=['localhost:9092'],
                                      auto_offset_reset='earliest')
        self.redis = RedisConnect(False)
        self.model = Model()

    async def detection(self):
        while True:
            msg = self.consumer.poll()
            if msg:
                value = ''
                for m in msg:
                    value = msg[m][0].value.decode('utf-8')
                img = self.redis.get(value)
                if img is not None:
                    img = self.model.render(img)
                    self.redis.set(img, value)
            await asyncio.sleep(0.01)
