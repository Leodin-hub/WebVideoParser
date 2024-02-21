from moduls.detector import SparkDetector
import asyncio
import sys


def main():
    detect = SparkDetector()
    try:
        asyncio.run(detect.run())
    except KeyboardInterrupt:
        sys.exit()


if __name__ == '__main__':
    main()