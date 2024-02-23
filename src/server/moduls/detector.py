import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from library.helpers.kafka_function import get_producer
from library.helpers.redis_connect import RedisConnect
from library.helpers.model_yolo import Model
from pyspark.sql import SparkSession
from loguru import logger


class SparkDetector:
    """A class for detecting frames using Spark streaming.

    Attributes:
        __spark: The Spark session object.
        __spark_stream: The Spark stream object.
        __producer: The Kafka producer object.
        __redis: The Redis connection object.
        __model: The model object for rendering frames.

    Methods:
        __init__: Initializes the SparkDetector class with Spark session, Spark stream, producer, Redis connection, and model.
        __enter__: Enters the context management block.
        __exit__: Exits the context management block and closes resources.
        __get_spark_session: Creates and returns a Spark session.
        __get_spark_stream: Creates and returns a Spark stream for reading from Kafka.
        __frame_detected: Processes detected frames and sends detection alerts.
        run: Runs the Spark stream processing for detecting frames and sending alerts.
    """
    @logger.catch(level='INFO')
    def __init__(self):
        """Initializes the SparkDetector class with Spark session, Spark stream, producer, Redis connection, and model.
        """
        self.__spark = self.__get_spark_session()
        self.__spark_stream = self.__get_spark_stream()
        self.__producer = get_producer()
        self.__redis = RedisConnect(False)
        self.__model = Model()

    @logger.catch(level='INFO')
    def __enter__(self):
        """Enters the context management block.

        Returns:
            self The SparkDetector instance
        """
        return self

    @logger.catch(level='INFO')
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exits the context management block and closes resources.

        Args:
            exc_type The type of exception raised.
            exc_val The exception value.
            exc_tb The exception traceback.
        """
        self.__producer.close()
        self.__redis.stop()
        self.__spark.stop()

    @logger.catch(level='INFO')
    def __get_spark_session(self):
        """Creates and returns a Spark session.

        Returns:
            spark The Spark session object
        """
        spark = SparkSession.builder \
                            .appName('DetectorFrame') \
                            .master("local[*]") \
                            .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0') \
                            .getOrCreate()
        spark.sparkContext.setLogLevel("ERROR")
        return spark

    @logger.catch(level='INFO')
    def __get_spark_stream(self):
        """Creates and returns a Spark stream for reading from Kafka.

        Returns:
            stream The Spark stream object
        """
        stream = self.__spark.readStream \
                             .format('kafka') \
                             .option('kafka.bootstrap.servers', 'localhost:9092') \
                             .option('subscribe', 'stream') \
                             .option("startingOffsets", "latest") \
                             .option('failOnDataLoss', 'false') \
                             .load()
        stream.selectExpr("CAST(value AS STRING)")
        return stream

    @logger.catch(level='INFO')
    def __frame_detected(self, batch_df, batch_id):
        """Processes detected frames and sends detection alerts.

        Args:
            batch_df The DataFrame containing detected frames.
            batch_id The ID of the batch.
        """
        data_collect = batch_df.collect()
        for data_row in data_collect:
            frame_id = data_row['value'].decode('utf-8')
            frame = self.__model.render(self.__redis.get(frame_id))
            self.__redis.set(frame, frame_id)
            self.__producer.send('detection', bytes(frame_id, 'utf-8'), timestamp_ms=1000)

    @logger.catch(level='INFO')
    async def run(self):
        """Runs the Spark stream processing for detecting frames and sending alerts.
        """
        self.__spark_stream.writeStream \
                           .foreachBatch(self.__frame_detected) \
                           .outputMode('append') \
                           .start() \
                           .awaitTermination()
