from moduls.detector import SparkDetector
from loguru import logger
import asyncio
import sys


@logger.catch(level='INFO')
def main():
    """External detector runner function
    """
    detect = SparkDetector()
    asyncio.run(detect.run())


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
