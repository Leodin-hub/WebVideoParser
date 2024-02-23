import sys
sys.path.append('../server')
from kafka import KafkaAdminClient, KafkaProducer, KafkaConsumer
from library.global_variables import PORT_KAFKA
from kafka.admin import NewTopic
from loguru import logger


def delete_topic():
    admin = KafkaAdminClient(bootstrap_servers=PORT_KAFKA)
    topics = admin.list_topics()
    admin.delete_topics(topics=topics)
    admin.close()


def init_topic():
    admin = KafkaAdminClient(bootstrap_servers=PORT_KAFKA)
    admin.create_topics([NewTopic('url_video', 2, 1)])
    admin.create_topics([NewTopic('stream', 2, 1)])
    admin.create_topics([NewTopic('detection', 2, 1)])
    admin.close()


@logger.catch(level='INFO')
def get_producer():
    return KafkaProducer(bootstrap_servers=[PORT_KAFKA])


@logger.catch(level='INFO')
def get_consumer(topic: str):
    return KafkaConsumer(topic, bootstrap_servers=[PORT_KAFKA], auto_offset_reset='earliest')
