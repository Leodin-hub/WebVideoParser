from moduls.reader import Reading
import asyncio
import sys


def main():
    """External reader runner function
    """
    reader = Reading()
    asyncio.run(reader.start())


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
