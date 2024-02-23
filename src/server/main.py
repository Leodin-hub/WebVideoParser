import os
import sys
sys.path.append(os.path.dirname(__file__))
from detector_start import main as detector_start
from server_start import main as server_start
from reader_start import main as reader_start
from multiprocessing import Process
from loguru import logger


@logger.catch(level='INFO')
def main():
    """The main function that runs the entire project
    """
    p1 = Process(target=server_start)
    p2 = Process(target=reader_start)
    p3 = Process(target=detector_start)
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
