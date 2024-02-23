import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from library.helpers.redis_connect import RedisConnect
from library.helpers.kafka_function import get_consumer
from library.global_variables import gen_img
from loguru import logger
import asyncio


class Streamer:
    """A class for streaming images using Kafka consumer and Redis.

    Attributes:
        consumer: The Kafka consumer object for receiving image data.
        redis: The RedisConnect object for storing and retrieving images.
        img: The current image data to be streamed.

    Methods:
        __init__: Initializes the Streamer class with a Kafka consumer, Redis connection, and initial image data.
        __exit__: Unsubscribes the Kafka consumer when exiting the context management block.
        get_img: A generator function that retrieves image data from Kafka and Redis and yields image frames.

    Google Style Parameters:
        - You should call the `__init__` method before accessing the `get_img` method.
        - Use the `get_img` method to continuously retrieve and yield image frames.
    """
    @logger.catch(level='INFO')
    def __init__(self):
        """Initializes the Streamer class with a Kafka consumer, Redis connection, and initial image data.
        """
        self.consumer = get_consumer('detection')
        if self.consumer is None:
            logger.critical('Kafka could not connect to the image')
            sys.exit()
        self.redis = RedisConnect(False)
        self.img = gen_img('Wait to stream')

    @logger.catch(level='INFO')
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Unsubscribes the Kafka consumer when exiting the context management block.

        Args:
            exc_type: The type of exception raised.
            exc_val: The exception value.
            exc_tb: The exception traceback.
        """
        self.consumer.unsubscribe()

    @logger.catch(level='INFO')
    async def get_img(self):
        """A generator function that retrieves image data from Kafka and Redis and yields image frames.

        Yields:
            image_frame: A frame of image data as bytes.
        """
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
