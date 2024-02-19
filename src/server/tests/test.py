import sys
sys.path.append('../server')
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
from redis import Redis
from moduls.model_yolo import Model
from yolov5 import detect

# Set up Redis connection
r = Redis(host='localhost', port=6379, db=0)
model = Model()

# Set up Spark session
spark = SparkSession.builder \
    .appName("KafkaSparkYOLOv5") \
    .getOrCreate()

# Read data from Kafka topic
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "input_topic") \
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
    .selectExpr("detected_frame_id AS key", "detected_frame_id AS value") \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "stream") \
    .option("checkpointLocation", "/tmp/checkpoint") \
    .start()

spark.streams.awaitAnyTermination()