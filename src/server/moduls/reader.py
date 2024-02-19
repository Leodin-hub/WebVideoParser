import sys
sys.path.append('../server')
from kafka import KafkaProducer, KafkaConsumer
from moduls.redis_connect import RedisConnect
import asyncio
import cv2


class Reading:
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
        self.consumer = KafkaConsumer('url_video', group_id='group1', bootstrap_servers=['localhost:9092'],
                                      auto_offset_reset='earliest')
        self.redis = RedisConnect(True)
        self.camera = cv2.VideoCapture()

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
            await asyncio.sleep(0.03)

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
            await asyncio.sleep(0.03)


# if __name__ == '__main__':
#     reader = Reading()
#     try:
#         asyncio.run(reader.start())
#     except KeyboardInterrupt:
#         sys.exit()
