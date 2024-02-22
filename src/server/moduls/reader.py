import sys
sys.path.append('../server')
from library.helpers.redis_connect import RedisConnect
from library.helpers.kafka_function import get_producer, get_consumer
import asyncio
import cv2


class Reading:
    """Class for reading video stream frames and processing them using a producer and consumer.

    Attributes:
        producer: The producer object for sending processed frame data.
        consumer: The consumer object for receiving video stream URLs.
        redis: The Redis connection object for storing frame data.
        camera: The OpenCV VideoCapture object for capturing frames from the video stream.

    Methods:
        __exit__(self, exc_type, exc_val, exc_tb): Unsubscribes the consumer when the instance is exited.
        start(self): Start reading and processing the video stream frames.
        waiting_for_stream(self): Continuously waits for available video stream URLs from the consumer.
        read_stream(self): Reads frames from the video stream, processes and sends them using the producer.
    """
    def __init__(self):
        """Initialize the Reading class with necessary attributes.

        The __init__ method sets up the Reading class with the producer, consumer, Redis connection, and VideoCapture object.
        These objects are necessary for reading and processing video stream frames.
        """
        self.producer = get_producer()
        self.consumer = get_consumer('url_video')
        self.redis = RedisConnect(True)
        self.camera = cv2.VideoCapture()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Unsubscribe the consumer when exiting the context management block.

        This method is called when the instance is exited, and it ensures that the consumer
        is unsubscribed from the video stream topic.

        Args:
            exc_type: The type of exception raised.
            exc_val: The exception value.
            exc_tb: The exception traceback.
        """
        self.consumer.unsubscribe()

    async def start(self):
        """Start reading and processing the video stream frames.

        The start method initiates the reading and processing of video stream frames. It creates
        and runs asynchronous tasks for waiting for stream URLs and reading the frames.
        """
        print('start reader')
        task_waiting = asyncio.create_task(self.waiting_for_stream())
        task_stream = asyncio.create_task(self.read_stream())
        await task_waiting
        await task_stream

    async def waiting_for_stream(self):
        """Continuously wait for video stream URLs from the consumer.

        This method continuously polls the consumer for available video stream URLs. When a new URL is received,
        it updates the VideoCapture object with the new stream and checks the connection status.
        """
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
        """Read frames from the video stream and process them.

        The read_stream method reads frames from the video stream, converts them to RGB format,
        encodes them as JPEG images, stores them in Redis, and sends them using the producer.
        """
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
