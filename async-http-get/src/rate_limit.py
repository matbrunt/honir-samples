import asyncio

# simple script to illustrate how you can have a task loop that does not exceed starting more than 5 tasks per 5 second interval.
# https://docs.python.org/3/library/asyncio-sync.html#asyncio.Semaphore
# https://stackoverflow.com/questions/67981218/why-doesnt-this-asyncio-semaphore-implementation-work-with-aiohttp-in-python

async def dequeue(sem, sleep):
    """Wait for a duration and then increment the semaphore"""
    try:
        await asyncio.sleep(sleep)
    finally:
        sem.release()


async def task(sem, sleep, data):
    """Decrement the semaphore, schedule an increment, and then work"""
    await sem.acquire()
    asyncio.create_task(dequeue(sem, sleep))
    # logic here
    print(data)


async def main():
    max_concurrent = 5
    sleep = 5

    sem = asyncio.Semaphore(max_concurrent)
    tasks = [asyncio.create_task(task(sem, sleep, i)) for i in range(15)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
