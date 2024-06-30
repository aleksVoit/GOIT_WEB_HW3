"""
this module search the dividends of given numbers, which divide without remainder
this module use performs itself in few processes, with common list of arrays, and Queue
"""
import logging
from multiprocessing import Process, Manager, current_process, Queue
from multiprocessing.sharedctypes import Array
from time import time


logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


def factorize(*numbers) -> []:
    """
    this method search dividers of numbers
    it uses Processes to search dividers of each number in a separate process
    it uses multiprocessing.Manager() for collecting arrays of dividers for each number
    it uses Queue for Processes
    """

    result_arr = Manager().list()
    queue = Queue()

    processes = []
    for num in numbers:  # i - заданное число, n - итератор от 0 до заданного числа, m - оператор фильтра
        p = Process(target=count, args=(queue, result_arr))
        processes.append(p)
        p.start()
        queue.put(num)

    [p.join() for p in processes]

    logger.debug(f'{result_arr}')
    return result_arr


def count(q: Queue, result_arr: list):
    """
    this method receive Queue, take a number from Queue, count dividers
    and append array of dividers to common fo all Processes result_arr
    """
    num = q.get()
    logger.debug(f'{current_process()} - started - number: {num}')
    result = [n for n in filter(lambda m: num % m == 0, range(1, num + 1))]
    result_arr.append(result)


if __name__ == '__main__':
    timer = time()

    a, b, c, d = factorize(128, 255, 99999, 10651060)

    logger.debug(f"Performance time - {time() - timer}")
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]
