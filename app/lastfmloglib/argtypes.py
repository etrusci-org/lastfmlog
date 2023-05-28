import os
import argparse
import time




def cliparserArgTypeQueryLimit(number: int) -> int:
    number = int(number)

    if number <= 0:
        raise argparse.ArgumentTypeError('must be > 0')

    return number


def cliparserArgTypeFrom(number: int) -> int:
    number = int(number)

    if number < 0:
        raise argparse.ArgumentTypeError('must be >= 0')

    if number >= int(time.time()):
        raise argparse.ArgumentTypeError('must be < unixtime_now')

    return number


def cliparserArgTypeTo(number: int) -> int:
    number = int(number)

    if number <= 0:
        raise argparse.ArgumentTypeError('must be > 0')

    if number > int(time.time()):
        raise argparse.ArgumentTypeError('must be <= unixtime_now')

    return number


def cliparserArgTypeExistingDirectoryPath(dirPath: str) -> str:
    if not os.path.exists(dirPath):
        raise argparse.ArgumentTypeError('path does not exist')

    if not os.path.isdir(dirPath):
        raise argparse.ArgumentTypeError('path does not point to a directory')

    return dirPath
