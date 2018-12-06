"""Solution to day 05 of the Advent of Code.

Reading input:
    The input provides the polymer as a string. This is fine as is. See
    _read_polymer function.

Matching units:
    Checking whether two units match is only a question of checking if both are
    the same letter and one is uppercase and the other lowercase. See
    _units_match function.

Reducing a polymer:
    Reducing a polymer is the core of the problem. Strings are immutable in
    Python so repeatedly removing characters from the middle of the string would
    yield terrible performance. Similarly, removing elements from the middle of
    a list yiels terrible performance as well, so converting our polymer string
    into a list would not solve the problem. On the other hand, appending values
    to the end of a list and popping values from the end of a list can be done
    in constant time. We can read through our polymer string and append each
    unit to a list one by one. If the unit we are reading matches the last unit
    in the list (effectively its neighbor in the polymer) then instead of
    appending the new unit, we pop the last unit from the list and discard both.
    A single pass with this algorithm provides a list of units that, when
    joined, make up the reduced polymer. See _reduce_polymer function.

Part 1:
    Once we have the reduced polymer, all we need to do is measure its length.
    See get_reduced_size function.

Improving a polymer:
    To improve a polymer, all we need to do is remove all units of a given type.
    Using regular expressions, we can replace all instances of the unit type
    characters (both lowercase and uppercase) by nothing, effectively removing
    them in one pass. See _improve_polymer function.

Part 2:
    Finding the best improved polymer is only a question of building all 26
    improved polymers and seeing which one is the smallest once reduced. See
    get_improved_size function.
"""

import re
import string

import utils


def _read_polymer(input_string: str) -> str:
    """Reads the polymer from a given input string.

    Args:
        input_string: A string containing the day's input.

    Returns:
        A string representing the polymer.
    """
    return input_string


def _units_match(unit_1: str, unit_2: str) -> bool:
    """Checks whether both units are of the same type and opposite polarity.

    Args:
        unit_1: A single-character string representing the first unit.
        unit_2: A single-character string representing the second unit.

    Returns:
        Whether the two units are of the same type (same letter) and opposite
        polarity (one uppercase, one lowercase).
    """
    if unit_1.islower():
        return unit_1.upper() == unit_2
    return unit_1.lower() == unit_2


def _reduce_polymer(polymer: str) -> str:
    """Triggers the units in a given polymer and provides the reduced version.

    Args:
        polymer: A string representing the polymer.

    Returns:
        A string representing the reduced polymer.
    """
    reduced_units = []
    for unit in polymer:
        if not reduced_units:
            reduced_units.append(unit)
        elif _units_match(unit, reduced_units[-1]):
            reduced_units.pop()
        else:
            reduced_units.append(unit)
    return ''.join(reduced_units)


def _improve_polymer(polymer: str, unit_type: str) -> str:
    """Removes a given unit type from a given polymer.

    Args:
        polymer: A string representing a polymer.
        unit_type: A single-character string representing the unit type.

    Returns:
        A string representing the reduced polymer.
    """
    return re.sub(f'{unit_type.lower()}|{unit_type.upper()}', '', polymer)


def get_reduced_size(input_string: str) -> int:
    """Finds the size of the polymer once it ahs been reduced.

    Args:
        input_string: The puzzle input.

    Returns:
        An integer representing the size of the reduced polymer.
    """
    polymer = _read_polymer(input_string)
    reduced_polymer = _reduce_polymer(polymer)
    return len(reduced_polymer)


def get_improved_size(input_string: str) -> int:
    """Finds the smallest polymer possible and provides its length.

    Args:
        input_string: The puzzle input.

    Returns:
        An integer representing the size of the smallest reduced polymer.
    """
    polymer = _read_polymer(input_string)
    return min([
        len(_reduce_polymer(_improve_polymer(polymer, unit_type)))
        for unit_type in string.ascii_lowercase
    ])


def _run_tests() -> None:
    """Tests solution."""
    assert get_reduced_size('aA') == 0
    assert get_reduced_size('abBA') == 0
    assert get_reduced_size('abAB') == 4
    assert get_reduced_size('aabAAB') == 6
    assert get_reduced_size('dabAcCaCBAcCcaDA') == 10
    assert get_improved_size('dabAcCaCBAcCcaDA') == 4


def _print_answers(reduced_size: int = None, improved_size: int = None) -> None:
    """Prints answers.

    Args:
        reduced_size: The reduced size of the polymer.
        improved_size: The reduced size of the improved polymer.
    """
    print('Answers for day 05:')
    print(f'  Reduced size: {reduced_size}')
    print(f'  Improved size: {improved_size}')


def main() -> None:
    """Runs tests and prints answers to day's puzzle."""
    _run_tests()
    input_string = utils.read_input(5)
    reduced_size = get_reduced_size(input_string)
    improved_size = get_improved_size(input_string)
    _print_answers(reduced_size, improved_size)


if __name__ == '__main__':
    main()
