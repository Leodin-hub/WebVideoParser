from pyspark.sql.types import StringType
from pyspark.sql.functions import udf
from pyspark.sql import SparkSession
from pyspark import SparkConf

conf = SparkConf().setMaster('local').setAppName('test').set('spark.local.dir', '/tmp/spark-temp')
spark = SparkSession.builder \
    .appName('DetectorFrame') \
    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0') \
    .getOrCreate()
spark.sparkContext.setLogLevel("WARN")

df = spark \
    .readStream \
    .format('kafka') \
    .option('kafka.bootstrap.servers', 'localhost:9092') \
    .option('subscribe', 'stream') \
    .load()
df.selectExpr('CAST(value as STRING)')


@udf(returnType=StringType())
def process_frame(frame_id: str):
    return frame_id


process_frame_udf = udf(process_frame, StringType())

processed_df = df \
    .selectExpr("CAST(value AS STRING) as frame_id") \
    .withColumn("detected_frame_id", process_frame("frame_id"))

processed_df \
    .selectExpr('detected_frame_id as value') \
    .writeStream \
    .format('kafka') \
    .option('kafka.bootstrap.servers', 'localhost:9092') \
    .option('topic', 'detection') \
    .option('startingTimestamp', '1000') \
    .option("checkpointLocation", "/tmp/checkpoint") \
    .start() \
    .awaitTermination()

# ds = df \
#   .selectExpr("CAST(value AS STRING)") \
#   .writeStream \
#   .format("kafka") \
#   .option("kafka.bootstrap.servers", "localhost:9092") \
#   .option("topic", "detection") \
#   .option("checkpointLocation", "/tmp/checkpoint") \
#   .start() \
#   .awaitTermination()
