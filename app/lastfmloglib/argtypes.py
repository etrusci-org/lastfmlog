import os
import argparse
import time




def cliparserArgTypeQueryLimit(number: int) -> int:
    number = int(number)
    if number < 1:
        raise argparse.ArgumentTypeError('must be > 0')
    return number


def cliparserArgTypeFrom(number: int) -> int:
    number = int(number)
    if number < 0:
        raise argparse.ArgumentTypeError('must be >= 0')
    return number


def cliparserArgTypeTo(number: int) -> int:
    number = int(number)
    if number > time.time():
        raise argparse.ArgumentTypeError('can not be in the future')
    return number


def cliparserArgTypeExistingDirectoryPath(dirPath: str) -> str:
    if not os.path.exists(dirPath) \
    or not os.path.isdir(dirPath):
        raise argparse.ArgumentTypeError('directory does not exist or path does not point to a direcotry')
    return dirPath
