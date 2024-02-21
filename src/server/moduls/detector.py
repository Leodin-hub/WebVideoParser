import sys
sys.path.append('../server')
from library.helpers.kafka_function import get_producer
from library.helpers.redis_connect import RedisConnect
from library.helpers.model_yolo import Model
from pyspark.sql import SparkSession


class SparkDetector:
    def __init__(self):
        self.__spark = self.__get_spark_session()
        self.__spark_stream = self.__get_spark_stream()
        self.__producer = get_producer()
        self.__redis = RedisConnect(False)
        self.__model = Model()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__producer.close()
        self.__redis.stop()
        self.__spark.stop()

    def __get_spark_session(self):
        spark = SparkSession.builder \
                            .appName('DetectorFrame') \
                            .master("local[*]") \
                            .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0') \
                            .getOrCreate()
        spark.sparkContext.setLogLevel("ERROR")
        return spark

    def __get_spark_stream(self):
        stream = self.__spark.readStream \
                             .format('kafka') \
                             .option('kafka.bootstrap.servers', 'localhost:9092') \
                             .option('subscribe', 'stream') \
                             .option("startingOffsets", "latest") \
                             .option('failOnDataLoss', 'false') \
                             .load()
        stream.selectExpr("CAST(value AS STRING)")
        return stream

    def __frame_detected(self, batch_df, batch_id):
        data_collect = batch_df.collect()
        for data_row in data_collect:
            frame_id = data_row['value'].decode('utf-8')
            print(f'frame_id: {frame_id}, type: {type(frame_id)}')
            frame = self.__model.render(self.__redis.get(frame_id))
            self.__redis.set(frame, frame_id)
            self.__producer.send('detection', bytes(frame_id, 'utf-8'), timestamp_ms=1000)

    async def run(self):
        self.__spark_stream.writeStream \
                           .foreachBatch(self.__frame_detected) \
                           .outputMode('append') \
                           .start() \
                           .awaitTermination()
