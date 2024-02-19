from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
from redis import Redis
# import numpy as np
# import yolov5
# import cv2

# Set up Redis connection
# r = Redis(host='localhost', port=6379, db=0)
# model = yolov5.load('moduls/yolov5s.pt')
# model.conf = 0.25
# model.iou = 0.45
# model.agnostic = False
# model.multi_label = False
# model.max_det = 1000


# def render(img):
#     img = np.frombuffer(img, np.uint8)
#     img = cv2.imdecode(img, cv2.IMREAD_COLOR)
#     frame = model(img)
#     frame.render()
#     buffer = cv2.imencode('.jpg', img)[1]
#     return buffer.tobytes()


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
    # r = Redis(host='localhost', port=6379, db=0)
    # frame = r.get(frame_id)
    # # detected_frame = render(frame)
    # detected_frame = frame
    # r.set(frame_id, detected_frame)
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
    .option('timestamp_ms', '1000') \
    .option("checkpointLocation", "/tmp/checkpoint") \
    .start()
    # .awaitTermination()

spark.streams.awaitAnyTermination()
