from moduls.detector import SparkDetector
import asyncio
import sys


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
