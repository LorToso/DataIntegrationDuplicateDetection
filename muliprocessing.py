import concurrent
from multiprocessing.pool import ThreadPool as Pool
import random

import time
from pip._vendor.requests.packages.urllib3.connectionpool import xrange


def multiprocessing():
    pool_size = 5
    pool = Pool(pool_size)
    items = [random.random() for _ in xrange(10000)]

    for x in range(0, 10000):
        pool.apply_async(worker, (items,))

    pool.close()
    pool.join()


def worker(items):
    for item in items:
        try:
            y = item + 1
        except:
            print('error with item')


def normal():
    items = [random.random() for _ in xrange(10000)]
    for x in range(0, 10000):
        worker(items)

if __name__ == '__main__':
    start_time = time.time()
    multiprocessing()
    elapsed_time = time.time() - start_time
    print("Elapsed time with multiprocessing {time}".format(time=elapsed_time))

    start_time2 = time.time()
    normal()
    elapsed_time2 = time.time() - start_time2
    print("Elapsed time without multiprocessing {time}".format(time=elapsed_time2))
