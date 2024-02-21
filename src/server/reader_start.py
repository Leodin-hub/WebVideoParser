from moduls.reader import Reading
import asyncio
import sys


def main():
    reader = Reading()
    try:
        asyncio.run(reader.start())
    except KeyboardInterrupt:
        sys.exit()


if __name__ == '__main__':
    main()
