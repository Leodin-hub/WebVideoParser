import sys
sys.path.append('../server')
from kafka import KafkaProducer, KafkaConsumer
from moduls.camera import Camera
from moduls.redis_connect import RedisConnect


class KafkaBase:
    def __init__(self, topic: str):
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
        self.consumer = KafkaConsumer(topic, group_id='group1', bootstrap_servers=['localhost:9092'],
                                      auto_offset_reset='earliest')
        self.redis = RedisConnect()
        self.redis.clear_db()
        self.camera = Camera()
