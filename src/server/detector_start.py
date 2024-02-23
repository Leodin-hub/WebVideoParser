import os
import sys
sys.path.append(os.path.dirname(__file__))
from moduls.detector import SparkDetector
from loguru import logger
import asyncio


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
