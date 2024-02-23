from moduls.reader import Reading
from loguru import logger
import asyncio
import sys


@logger.catch(level='INFO')
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
