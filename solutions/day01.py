"""Solution to day 01 of the Advent of Code."""

from typing import List

import utils


def _read_changes(input_string: str) -> List[int]:
    """Reads frequency changes from a given input string.

    Args:
        input_string: A string containing the day's input.

    Returns:
        A list integers representing changes.
    """
    return [int(line) for line in input_string.split('\n')]


def _apply_change(frequency: int, change: int) -> int:
    """Applies a change to a frequency.

    Args:
        frequency: A integer representation of the frequency to change.
        change: An integer representing the change to apply.

    Returns:
        An integer representing the new frequency.
    """
    return frequency + change


def get_final_frequency(input_string: str) -> int:
    """Computes the final frequency given an input string.

    Args:
        input_string: The puzzle input.

    Returns:
        The final frequency after applying all changes."""
    changes = _read_changes(input_string)
    frequency = 0
    for change in changes:
        frequency = _apply_change(frequency, change)
    return frequency


def get_first_repetition(input_string: str) -> int:
    """Finds the first repetition given an input string.

    Args:
        input_string: The puzzle input.

    Returns:
        The first frequency to appear twice.
    """
    changes = _read_changes(input_string)
    frequency = 0
    seen_frequencies = {frequency}
    while True:
        for change in changes:
            frequency = _apply_change(frequency, change)
            if frequency in seen_frequencies:
                return frequency
            seen_frequencies.add(frequency)


def _run_tests() -> None:
    """Tests solution."""
    assert get_final_frequency('+1\n+1\n+1') == 3
    assert get_final_frequency('+1\n+1\n-2') == 0
    assert get_final_frequency('-1\n-2\n-3') == -6
    assert get_first_repetition('+1\n-1') == 0
    assert get_first_repetition('+3\n+3\n+4\n-2\n-4') == 10
    assert get_first_repetition('-6\n+3\n+8\n+5\n-6') == 5
    assert get_first_repetition('+7\n+7\n-2\n-7\n-4') == 14


def _print_answers(final_frequency: int = None,
                   first_repetition: int = None) -> None:
    """Prints answers.

    Args:
        final_frequency: The answer to the first part of the day's puzzle.
        first_repetition: The answer to the second part of the day's puzzle.
    """
    print('Answers for day 01:')
    print(f'  Final frequency: {final_frequency}')
    print(f'  First repetition: {first_repetition}')


def main() -> None:
    """Runs tests and prints answers to day's puzzle."""
    _run_tests()
    input_string = utils.read_input(1)
    final_frequency = get_final_frequency(input_string)
    first_repetition = get_first_repetition(input_string)
    _print_answers(final_frequency, first_repetition)


if __name__ == '__main__':
    main()
