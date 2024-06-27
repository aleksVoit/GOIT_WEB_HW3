import os
import shutil
from pathlib import Path
import sys
import logging


logger = logging.getLogger()
streem_handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(processName)s %(lineno)s %(message)s'
)
streem_handler.setFormatter(formatter)
logger.addHandler(streem_handler)
logger.setLevel(logging.DEBUG)


def check_dir(source_path: Path, target_path: Path):
    for item in source_path.iterdir():
        if item.is_dir():
            check_dir(item, target_path)
            if is_empty(item):
                os.rmdir(item)
        elif item.is_file():
            copy_file_to_new_dir(item, target_path)


def copy_file_to_new_dir(file_path: Path, target_dir_path: Path):

    new_dir = file_path.suffix[1:]  # take new folder name from the file
    if target_dir_path.joinpath(new_dir).exists():
        shutil.move(file_path, target_dir_path.joinpath(new_dir))
    else:
        os.makedirs(target_dir_path.joinpath(new_dir))
        shutil.move(file_path, target_dir_path.joinpath(new_dir))


def is_empty(dir_path: Path) -> bool:
    return len(os.listdir(dir_path)) == 0


if __name__ == '__main__':

    source_path = Path(sys.argv[1])
    target_path = Path(sys.argv[2])
    print(source_path, target_path)
    check_dir(source_path, target_path)
    if is_empty(source_path):
        os.rmdir(source_path)
