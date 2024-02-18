import asyncio
import random
import sys
import time


async def g():
    it = 0
    while True:
        print(it)
        it += 1
        await asyncio.sleep(random.random())
        # time.sleep(random.random())


async def h():
    it = 1000
    while True:
        print(it)
        it -= 1
        await asyncio.sleep(random.random())
        # time.sleep(random.random())


async def wait():
    while True:
        print('Wait')
        await asyncio.sleep(0.2)


async def b():
    try:
        task1 = asyncio.create_task(g())
        task2 = asyncio.create_task(h())
        task3 = asyncio.create_task(wait())
        while True:
            await task1
            await task2
            await task3
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    asyncio.run(b())
