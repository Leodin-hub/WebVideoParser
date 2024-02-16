import sys
import time

from redis import Redis
from kafka import KafkaProducer, KafkaConsumer
import cv2
import numpy as np


class Reading:
    def __init__(self):
        self.connect_redis = Redis(host='localhost',
                                   port=6379, db=0,
                                   charset="utf-8",
                                   decode_responses=True)
        self.camera = cv2.VideoCapture()
        self.img_wait = self.gen_img_wait()
        self.url_stream = ''
        self.connecting = False
        self.id_message = 0
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
        self.consumer = KafkaConsumer('url_video', group_id='group1', bootstrap_servers=['localhost:9092'],
                                      auto_offset_reset='earliest')

    def gen_img_wait(self):
        img = np.zeros((640, 1080, 3), np.uint8) * 188
        cv2.putText(img, 'Wait to video stream', (130, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_encode = cv2.imencode('.jpg', img)[1]
        img_byte = img_encode.tobytes()
        return img_byte

    def connect_to_url(self):
        try:
            self.camera = cv2.VideoCapture(self.url_stream)
            self.connecting = True
        except:
            self.connecting = False

    def reading_stream(self):
        try:
            print('start reading')
            while True:
                msg = self.consumer.poll()
                if msg:
                    for m in msg:
                        self.url_stream = msg[m][0].value.decode('utf-8')
                    print(self.url_stream)
                    self.connect_to_url()
                success, frame = self.camera.read()
                if success:
                    self.connect_redis.set(str(self.id_message), frame.tobytes())
                    self.producer.send('stream', bytes(str(self.id_message), 'utf-8'))
                    self.id_message += 1
                    print(self.id_message)
                time.sleep(0.03)
        except KeyboardInterrupt:
            sys.exit()


if __name__ == '__main__':
    reader = Reading()
    reader.reading_stream()
