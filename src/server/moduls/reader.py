import sys
sys.path.append('../server')
from library.helpers.redis_connect import RedisConnect
from library.helpers.kafka_function import get_producer, get_consumer
import asyncio
import cv2


class Reading:
    def __init__(self):
        self.producer = get_producer()
        self.consumer = get_consumer('url_video')
        self.redis = RedisConnect(True)
        self.camera = cv2.VideoCapture()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.consumer.unsubscribe()

    async def start(self):
        print('start reader')
        task_waiting = asyncio.create_task(self.waiting_for_stream())
        task_stream = asyncio.create_task(self.read_stream())
        await task_waiting
        await task_stream

    async def waiting_for_stream(self):
        print('start waiting for stream')
        while True:
            msg = self.consumer.poll()
            if msg:
                value = ''
                for m in msg:
                    value = msg[m][0].value.decode('utf-8')
                self.camera = cv2.VideoCapture(value)
                print(f'Url video stream: {value}\nConnect is: {self.camera.isOpened()}')
            await asyncio.sleep(0.01)

    async def read_stream(self):
        print('start read stream')
        while True:
            if self.camera.isOpened():
                success, frame = self.camera.read()
                if success:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_encode = cv2.imencode('.jpg', frame)[1]
                    s = self.redis.set(frame_encode.tobytes())
                    self.producer.send('stream', bytes(s, 'utf-8'), timestamp_ms=1000)
            await asyncio.sleep(0.01)
