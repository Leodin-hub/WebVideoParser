from redis import Redis


class RedisConnect:
    def __init__(self, reader: bool):
        self.connect_redis = Redis(host='localhost', port=6379, db=0)
        if reader:
            self.connect_redis.flushall()
        self.id_last_img = 0

    def set(self, img, id_img=None):
        if id_img is not None:
            self.connect_redis.set(id_img, img)
        else:
            self.connect_redis.set(str(self.id_last_img), img)
            self.id_last_img += 1
            return str(self.id_last_img - 1)

    def get(self, id_img):
        img = self.connect_redis.get(id_img)
        return img
