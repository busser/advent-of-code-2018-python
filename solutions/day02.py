"""Solution to day 02 of the Advent of Code.

Reading input:
    Each line in the onput file is a box ID. This is as easy as it gets. See
    _read_box_ids function.

Counting letters:
    In order to count the number of times a letter appears in a given box ID, we
    keep track of the number of times we've seen each letter with a dictionary.
    The key is the letter and the value is the count so far. See _count_letters
    function.

Part 1:
    Computing the checksum is only a question of counting how many words have a
    2 or 3 in the values of the dictionary returned by _count_letters. See
    get_checksum function.

Letters in common:
    Using list comprehensions, we can build a list of the letters any two box
    IDs have in the same position. Read https://waymoot.org/home/python_string/
    for an analysis of string concatenation performance in Python. See
    _letters_in_common function.

Similar box IDs:
    Two box IDs are similar if the amount of letters they have in the same
    position is one less than the length of the IDs. We can check if this is the
    case for every combination of box ID in order to find a pair of similar box
    IDs. See _similar_box_ids function.

Part 2:
    Once we have a pair of similar box IDs, we can join the letters they have in
    common to build the answer we are looking for. See
    get_similar_box_ids_overlap function.
"""

import itertools
from typing import Dict, List, Tuple

import utils


def _read_box_ids(input_string: str) -> List[str]:
    """Reads box IDs from a given input string.

    Args:
        input_string: A string containing the day's input.

    Returns:
        A list of strings representing box IDs.
    """
    return input_string.split('\n')


def _count_letters(box_id: str) -> Dict[str, int]:
    """Counts the number of times each letter appears in a given box ID.

    Args:
        box_id: The string to count the letters of.

    Returns:
        A dictionary where the keys are all letters in the box ID and the value
        is the number of times the letter appears in the box ID.
    """
    count = {}
    for letter in box_id:
        count[letter] = count.get(letter, 0) + 1
    return count


def _letters_in_common(box_id_1: str, box_id_2: str) -> List[str]:
    """Returns the letters two box IDs have in common in the same position.

    For example:
        'abcde', 'axcye' -> 'ace': the second and fourth characters differ.

    Args:
        box_id_1: First box ID.
        box_id_2: Second box ID.

    Returns:
        A list of the letters the two box IDs have in common in the same
        position.
    """
    return [
        let_1 for (let_1, let_2) in zip(box_id_1, box_id_2) if let_1 == let_2
    ]


def _similar_box_ids(box_ids: List[str]) -> Tuple[str, str]:
    """Finds the two correct box IDs (all letters in common but one).

    Args:
        box_ids: A list of box IDs.

    Returns:
        A pair of box IDs which have all letters in common except one.
    """
    for (box_id_1, box_id_2) in itertools.combinations(box_ids, 2):
        letters = _letters_in_common(box_id_1, box_id_2)
        if len(letters) == len(box_id_1) - 1:
            return (box_id_1, box_id_2)
    return None


def get_checksum(input_string: str) -> int:
    """Computes the checksum given an input string.

    Args:
        input_string: The puzzle input.

    Returns:
        The checksum.
    """
    box_ids = _read_box_ids(input_string)
    ids_with_two, ids_with_three = 0, 0
    for box_id in box_ids:
        letter_count = _count_letters(box_id)
        if 2 in letter_count.values():
            ids_with_two += 1
        if 3 in letter_count.values():
            ids_with_three += 1
    return ids_with_two * ids_with_three


def get_similar_box_ids_overlap(input_string: str) -> str:
    """Finds the common letters in the correct box IDs given an input string.

    Args:
        input_string: The puzzle input.

    Returns:
        The common letters.
    """
    box_ids = _read_box_ids(input_string)
    correct_box_ids = _similar_box_ids(box_ids)
    return ''.join(_letters_in_common(*correct_box_ids))


def _run_tests() -> None:
    """Tests solution."""
    assert get_checksum(
        'abcdef\nbababc\nabbcde\nabcccd\naabcdd\nabcdee\nababab') == 12
    assert get_similar_box_ids_overlap(
        'abcde\nfghij\nklmno\npqrst\nfguij\naxcye\nwvxyz') == 'fgij'


def _print_answers(checksum: int = None, common_letters: str = None) -> None:
    """Prints answers.

    Args:
        checksum: The answer to the first part of the day's puzzle.
        common_letters: The answer to the second part of the day's puzzle.
    """
    print('Answers for day 02:')
    print(f'  Checksum: {checksum}')
    print(f'  Letters in common: {common_letters}')


def main() -> None:
    """Runs tests and prints answers to day's puzzle."""
    _run_tests()
    input_string = utils.read_input(2)
    checksum = get_checksum(input_string)
    letters_in_common = get_similar_box_ids_overlap(input_string)
    _print_answers(checksum, letters_in_common)


if __name__ == '__main__':
    main()
