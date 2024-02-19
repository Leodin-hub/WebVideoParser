from moduls.reader import Reading
import asyncio
import sys

if __name__ == '__main__':
    reader = Reading()
    try:
        asyncio.run(reader.start())
    except KeyboardInterrupt:
        sys.exit()
