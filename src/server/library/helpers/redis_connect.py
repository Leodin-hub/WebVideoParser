import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from library.global_variables import REDIS_PORT
from loguru import logger
from redis import Redis


class RedisConnect:
    """
    A class for interacting with Redis for storing and retrieving image data.

    Attributes:
        connect_redis: The Redis connection object.
        id_last_img: The ID of the last stored image.

    Methods:
        __init__: Initializes the RedisConnect class with a Redis connection and sets the initial image ID.
        check_connect: Checks the connection status to Redis by pinging.
        set: Sets an image in Redis with or without specifying an image ID.
        get: Retrieves an image from Redis based on the provided image ID.
        stop: Closes the Redis connection.
    """
    @logger.catch(level='INFO')
    def __init__(self, reader: bool):
        """Initializes the RedisConnect class with a Redis connection and sets the initial image ID.

        Args:
            reader: A boolean flag indicating whether to clear all data when reading.
        """
        self.connect_redis = Redis(**REDIS_PORT, db=0)
        if not self.connect_redis.ping():
            logger.critical('Redis could not connect to the image')
            sys.exit()
        if reader:
            self.connect_redis.flushall()
        self.id_last_img = 0

    @logger.catch(level='INFO')
    def check_connect(self):
        """Checks the connection status to Redis by pinging.

        Returns:
            ping_response: The response from the Redis ping command.
        """
        return self.connect_redis.ping()

    @logger.catch(level='INFO')
    def set(self, img, id_img=None):
        """Sets an image in Redis with or without specifying an image ID.

        Args:
            img: The image data to store in Redis.
            id_img: Optional image ID to store the image with a specific key.

        Returns:
            image_id: The ID of the stored image as a string.
        """
        if id_img is not None:
            self.connect_redis.set(id_img, img)
        else:
            self.connect_redis.set(str(self.id_last_img), img)
            self.id_last_img += 1
            return str(self.id_last_img - 1)

    @logger.catch(level='INFO')
    def get(self, id_img):
        """Retrieves an image from Redis based on the provided image ID.

        Args:
            id_img: The ID of the image to retrieve from Redis.

        Returns:
            img: The retrieved image data.
        """
        img = self.connect_redis.get(id_img)
        return img

    @logger.catch(level='INFO')
    def stop(self):
        """Closes the Redis connection.
        """
        self.connect_redis.close()
