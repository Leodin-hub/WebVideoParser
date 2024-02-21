import sys
sys.path.append('../server')
from library.global_variables import PORT_KAFKA
from kafka import KafkaAdminClient, KafkaProducer, KafkaConsumer
from kafka.admin import NewTopic


def delete_topic():
    admin = KafkaAdminClient(bootstrap_servers=PORT_KAFKA)
    topics = admin.list_topics()
    for topic in topics:
        admin.delete_topics(topics=topic)
    admin.close()


def init_topic():
    admin = KafkaAdminClient(bootstrap_servers=PORT_KAFKA)
    admin.create_topics([NewTopic('url_video', 2, 1)])
    admin.create_topics([NewTopic('stream', 2, 1)])
    admin.create_topics([NewTopic('detection', 2, 1)])
    admin.close()


def get_producer():
    return KafkaProducer(bootstrap_servers=[PORT_KAFKA])


def get_consumer(topic: str):
    return KafkaConsumer(topic, bootstrap_servers=[PORT_KAFKA], auto_offset_reset='earliest')
