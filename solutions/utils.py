"""A set of utility functions for the Advent of Code."""

import os


def read_input(day: int) -> str:
    """Reads the input file of the given day.

    Args:
        day: An integer representing the day.

    Returns:
        The contents of the day's input file as a string.
    """
    # Assumes the input file is ../inputs/dayXX.txt relative to this source file's directory, where
    # XX is a two-digit representation of day.
    sourcedir = os.path.dirname(__file__)
    inputpath = f'{sourcedir}/../inputs/day{day:02d}.txt'
    with open(inputpath) as inputfile:
        contents = inputfile.read().strip()
    return contents
