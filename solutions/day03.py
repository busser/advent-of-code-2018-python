"""Solution to day 03 of the Advent of Code.

Reading input:
    Each line in the input contains five integers we are interested in,
    separated by meaningless characters. We can use regular expressions to find
    those integers and store them in an easy-to-use format. See _read_claims
    function.

Number of claims per square:
    In order to count the number of times any square inch of fabric has been
    claimed, we build a matrix of zeros representing the square inches of
    fabric. For each claim, we increment the values of each of the squares in
    the claim's area. This builds a matrix where each cell contains the number
    of times the corresponding square inch has been claimed. See
    _count_claims_per_square function.

Part 1:
    Once we have the number of times each square inch of fabric has been
    claimed, all we need to do is count the number of cells that have a value of
    two or more. See count_overclaimed_squares function.

Overlapping claims:
    Checking if a claim overlaps with any other comes down to checking if each
    square inch of fabric in the claim's area has a value of 1 in the matrix
    built by the _count_claims_per_square function. See _claim_overlaps
    function.

Part 2:
    After counting the number of claims for each square inch, we can check each
    claim to find the one that overlaps with no other and obtain its ID. See
    get_intact_claim_id function.
"""

import itertools
import re
from typing import List, NamedTuple

import utils


class AreaClaim(NamedTuple):  # pylint: disable=R0903
    """Represents an Elf's claim on an area of fabric.

    Attributes:
        id: The claim's ID.
        x: The number of inches between the left edge of the fabric and the left
            edge of the rectangle.
        y: The number of inches between the top edge of the fabric and the top
            edge of the rectangle.
        width: The width of the rectangle in inches.
        height: The height of the rectangle in inches.
    """
    id: int
    x: int
    y: int
    width: int
    height: int


def _read_claims(input_string: str) -> List[AreaClaim]:
    """Reads area claims from a given input string.

    Args:
        input_string: A string containing the day's input.

    Returns:
        A list of AreaClaim representing the area claims.
    """
    return [
        AreaClaim(*[int(num)
                    for num in re.findall('[0-9]+', line)])
        for line in input_string.split('\n')
    ]


def _count_claims_per_square(claims: List[AreaClaim]) -> List[List[int]]:
    """Counts the number of claims for each square inch of fabric.

    Args:
        claims: A list of claims on areas of fabric.

    Returns:
        A matrix of the number of claims for each square inch of fabric.
    """
    square_claims = [[0 for i in range(1000)] for j in range(1000)]
    for claim in claims:
        for row in range(claim.y, claim.y + claim.height):
            for col in range(claim.x, claim.x + claim.width):
                square_claims[row][col] += 1
    return square_claims


def _claim_overlaps(claim: AreaClaim, square_claims: List[List[int]]) -> bool:
    """Checks whether the given claim overlaps with any other claim.

    Args:
        claim: The claim to check.
        square_claims: The number of claims for each square inch of fabric.

    Returns:
        Whether the claim is the only one to affect the squares it contains.
    """
    for row in range(claim.y, claim.y + claim.height):
        for col in range(claim.x, claim.x + claim.width):
            if square_claims[row][col] > 1:
                return True
    return False


def count_overclaimed_squares(input_string: str) -> int:
    """Counts the number of square inches that have overlapping claims.

    Args:
        input_string: The puzzle input.

    Returns:
        The number of square inches that have overlapping claims.
    """
    claims = _read_claims(input_string)
    claims_per_square = _count_claims_per_square(claims)
    overlaps = sum(
        [1 for count in itertools.chain(*claims_per_square) if count >= 2])
    return overlaps


def get_intact_claim_id(input_string: str) -> int:
    """Finds the ID of the only claim that does not overlap.

    Args:
        input_string: The puzzle input.

    Returns:
        The ID of the only claim that does not overlap.
    """
    claims = _read_claims(input_string)
    claims_per_square = _count_claims_per_square(claims)
    for claim in claims:
        if not _claim_overlaps(claim, claims_per_square):
            return claim.id
    return None


def _run_tests() -> None:
    """Tests solution."""
    assert count_overclaimed_squares(
        '#1 @ 1,3: 4x4\n#2 @ 3,1: 4x4\n#3 @ 5,5: 2x2') == 4
    assert get_intact_claim_id(
        '#1 @ 1,3: 4x4\n#2 @ 3,1: 4x4\n#3 @ 5,5: 2x2') == 3


def _print_answers(overclaimed_squares: int = None,
                   intact_claim_id: int = None) -> None:
    """Prints answers.

    Args:
        overclaimed_squares: The answer to the first part of the day's puzzle.
        intact_claim_id: The answer to the second part of the day's puzzle.
    """
    print('Answers for day 03:')
    print(f'  Overclaimed squares: {overclaimed_squares}')
    print(f'  Intact claim ID: {intact_claim_id}')


def main() -> None:
    """Runs tests and prints answers to day's puzzle."""
    _run_tests()
    input_string = utils.read_input(3)
    overclaimed_squares = count_overclaimed_squares(input_string)
    intact_claim_id = get_intact_claim_id(input_string)
    _print_answers(overclaimed_squares, intact_claim_id)


if __name__ == '__main__':
    main()
