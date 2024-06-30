"""
this module search the dividends of given numbers, which without remainder
this module is synchronous
"""
import logging
from time import time


logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


def factorize(*number):
    """
    this method receive numbers as parameters and count dividers for these numbers
    for each number the founded array appended to result_array
    method return result_array
    """
    result_arr = []
    for i in number:  # i - заданное число, n - итератор от 0 до заданного числа, m - оператор фильтра
        i_result = [n for n in filter(lambda m: i % m == 0, range(1, i + 1))]
        result_arr.append(i_result)
        logger.debug(f"{i_result}")
    return result_arr


if __name__ == '__main__':
    """
    this is a main method
    it start the function factorize with numbers as parameters.
    """
    timer = time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    logger.debug(f"Performance time - {time() - timer}")
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]