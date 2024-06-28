import multiprocessing
import os
import shutil
from pathlib import Path
import sys
import logging
from threading import Thread, RLock
from time import time

logger = logging.getLogger()
streem_handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(processName)s %(threadName)s %(message)s'
)
streem_handler.setFormatter(formatter)
logger.addHandler(streem_handler)
logger.setLevel(logging.DEBUG)

t_lock = RLock()


def check_dir(locker: RLock, source_path: Path, target_path: Path):

    for item in source_path.iterdir():
        if item.is_dir():
            locker.acquire()
            logger.debug(f'check directory: {source_path}')
            check_dir(locker, item, target_path)
            locker.release()
        elif item.is_file():
            locker.acquire()
            copy_file_to_new_dir(item, target_path)
            locker.release()


def copy_file_to_new_dir(file_path: Path, target_dir_path: Path):
    logger.debug(f'copy file: {file_path}')
    new_dir = file_path.suffix[1:]  # take new folder name from the file
    if target_dir_path.joinpath(new_dir).exists():
        shutil.move(file_path, target_dir_path.joinpath(new_dir))
    else:
        os.makedirs(target_dir_path.joinpath(new_dir))
        shutil.move(file_path, target_dir_path.joinpath(new_dir))


def is_empty(dir_path: Path) -> bool:
    return len(os.listdir(dir_path)) == 0


# def remove_empty_folders(locker: RLock, dir_path: Path):
#     for folder in dir_path.iterdir():
#
#         if not is_empty(folder):
#             locker.acquire()
#             logger.debug(f' {folder} is not empty')
#             remove_empty_folders(locker, folder)
#             locker.release()
#
#         else:
#             locker.acquire()
#             logger.debug(f'remove {folder}')
#             os.rmdir(folder)
#             locker.release()
#     os.rmdir(dir_path)


if __name__ == '__main__':

    source_path = Path(sys.argv[1])
    target_path = Path(sys.argv[2])

    timer = time()

    threads = []
    for i in range(multiprocessing.cpu_count()):
        thread = Thread(target=check_dir, args=(t_lock, source_path, target_path))
        thread.start()
        threads.append(thread)
    [el.join() for el in threads]

    # threads = []
    # new_lock = threadLock()
    # for i in range(3):
    #     thread = Thread(target=remove_empty_folders, args=(new_lock, source_path))
    #     thread.start()
    #     threads.append(thread)
    # [el.join() for el in threads]

    logger.debug(f'Performance time: {time() - timer}')

