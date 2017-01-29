import multiprocessing as mp
import random

import time
from pip._vendor.requests.packages.urllib3.connectionpool import xrange

items = [random.random() for _ in xrange(10000)]


def multiprocessing():
    pool_size = 5
    pool = mp.Pool(pool_size)

    for item in items:
        pool.apply_async(worker, (item,))

    pool.close()
    pool.join()


def worker(item):
    try:
        my_function(item)
    except:
        print('error with item')


def my_function(item):
    for x in range(0, 10000):
        #some operation
        comparison = (x == item)


def normal():

    for item in items:
        worker(item)

if __name__ == '__main__':
    start_time = time.time()
    multiprocessing()
    elapsed_time = time.time() - start_time
    print("Elapsed time with multiprocessing {time}".format(time=elapsed_time))

    start_time2 = time.time()
    normal()
    elapsed_time2 = time.time() - start_time2
    print("Elapsed time without multiprocessing {time}".format(time=elapsed_time2))
