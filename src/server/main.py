from multiprocessing import Process
from server_start import main as server_start
from reader_start import main as reader_start
from detector_start import main as detector_start


def main():
    p1 = Process(target=server_start)
    p2 = Process(target=reader_start)
    p3 = Process(target=detector_start)
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
    # geek


if __name__ == '__main__':
    main()
