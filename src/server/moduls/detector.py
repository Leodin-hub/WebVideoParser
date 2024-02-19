import sys
sys.path.append('../server')
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
from moduls.model_yolo import Model
from redis import Redis

# Set up Redis connection
r = Redis(host='localhost', port=6379, db=0)
model = Model()

# Set up Spark session
spark = SparkSession.builder \
    .appName("KafkaSparkYOLOv5") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0") \
    .getOrCreate()

# Read data from Kafka topic
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "stream") \
    .load()


# Define function to process frames
def process_frame(frame_id):
    frame = r.get(frame_id)
    detected_frame = model.render(frame)
    r.set(frame_id, detected_frame)
    return frame_id


process_frame_udf = udf(process_frame, StringType())

# Apply processing function to each message in the Kafka stream
processed_df = df \
    .selectExpr("CAST(value AS STRING) as frame_id") \
    .withColumn("detected_frame_id", process_frame_udf("frame_id"))

# Write processed frames back to another Kafka topic
processed_df \
    .selectExpr("detected_frame_id AS key") \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "detection") \
    .option("checkpointLocation", "/tmp/checkpoint") \
    .start()

spark.streams.awaitAnyTermination()
# import sys
# sys.path.append('../server')
# from kafka import KafkaProducer, KafkaConsumer
# from moduls.redis_connect import RedisConnect
# from moduls.model_yolo import Model
# import asyncio
#
# class Detector:
#     def __init__(self):
#         self.consumer = KafkaConsumer('stream', group_id='group2', bootstrap_servers=['localhost:9092'],
#                                       auto_offset_reset='earliest')
#         self.redis = RedisConnect(False)
#         self.model = Model()
#
#     async def detection(self):
#         while True:
#             msg = self.consumer.poll()
#             if msg:
#                 value = ''
#                 for m in msg:
#                     value = msg[m][0].value.decode('utf-8')
#                 img = self.redis.get(value)
#                 if img is not None:
#                     img = self.model.render(img)
#                     self.redis.set(img, value)
#                     print(f'Detection {value}')
#             await asyncio.sleep(0.01)
