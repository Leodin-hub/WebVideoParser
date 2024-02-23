import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient
from kafka.errors import TopicAlreadyExistsError
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
    try:
        admin.create_topics([NewTopic('url_video', 2, 1),
                             NewTopic('stream', 2, 1),
                             NewTopic('detection', 2, 1)],
                            validate_only=False)
    except TopicAlreadyExistsError:
        logger.error('Topics have already been created')
    admin.close()


@logger.catch(level='INFO')
def get_producer():
    return KafkaProducer(bootstrap_servers=[PORT_KAFKA])


@logger.catch(level='INFO')
def get_consumer(topic: str):
    return KafkaConsumer(topic, bootstrap_servers=[PORT_KAFKA], auto_offset_reset='earliest')
