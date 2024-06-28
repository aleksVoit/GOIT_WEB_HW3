from multiprocessing import Process, RLock as P_lock
import os
import shutil
from pathlib import Path
import sys
import logging
from threading import Thread, RLock as T_lock
from time import time

logger = logging.getLogger()
streem_handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(processName)s %(threadName)s %(message)s'
)
streem_handler.setFormatter(formatter)
logger.addHandler(streem_handler)
logger.setLevel(logging.DEBUG)

t_lock = T_lock()
p_lock = P_lock()


def check_dir(locker: T_lock, source_path: Path, target_path: Path):

    for item in source_path.iterdir():
        if item.is_dir():
            logger.debug(f'check directory: {source_path}')
            check_dir(locker, item, target_path)

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


if __name__ == '__main__':

    source_path = Path(sys.argv[1])   # Path(sys.argv[1]) | Path('../garbage')
    target_path = Path(sys.argv[2])

    timer = time()

    threads = []
    for folder in source_path.iterdir():
        logger.debug(f'check folder: {folder}')
        thread = Thread(target=check_dir, args=(t_lock, folder, target_path))
        thread.start()
        threads.append(thread)
    [el.join() for el in threads]

    # processes = []
    # for folder in source_path.iterdir():
    #     logger.debug(f'check folder: {folder}')
    #     process = Process(target=check_dir, args=(p_lock, folder, target_path))
    #     process.start()
    #     processes.append(process)
    # [el.join() for el in processes]

    logger.debug(f'Performance time: {time() - timer}')

