import sys
sys.path.append('../server')
import asyncio
from moduls.kafka_base import KafkaBase


class Reading(KafkaBase):
    def __init__(self):
        super().__init__('url_video')

    async def start(self):
        task_waiting = asyncio.create_task(self.waiting_for_stream())
        task_stream = asyncio.create_task(self.read_stream())
        await task_waiting
        await task_stream

    async def waiting_for_stream(self):
        try:
            while True:
                msg = self.consumer.poll()
                if msg:
                    for m in msg:
                        self.camera.connect_url(msg[m][0].value.decode('utf-8'))
                    print(f'Connect: {self.camera.url_connect}')
                await asyncio.sleep(0.03)
        except KeyboardInterrupt:
            sys.exit()

    async def read_stream(self):
        try:
            task_stream = self.camera.stream()
            while True:
                frame = task_stream.__next__()
                if frame:
                    s = self.redis.set(frame)
                    self.producer.send('stream', s)
                    print(s)
                await asyncio.sleep(0.03)
        except KeyboardInterrupt:
            sys.exit()


if __name__ == '__main__':
    reader = Reading()
    asyncio.run(reader.start())
