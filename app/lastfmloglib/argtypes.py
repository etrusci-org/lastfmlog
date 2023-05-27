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
        raise argparse.ArgumentTypeError(f'can not be in the future')
    return number
