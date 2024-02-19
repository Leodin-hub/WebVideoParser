from moduls.detector import Detector
import asyncio
import sys

if __name__ == '__main__':
    detector = Detector()
    try:
        asyncio.run(detector.detection())
    except KeyboardInterrupt:
        sys.exit()