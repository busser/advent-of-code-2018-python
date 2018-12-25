"""Solution to day 08 of the Advent of Code.

Reading input:
    The input is a series of integers spearated by spaces. Using Python's
    string.split and int functions we can build a list of integers. See
    _read_numbers function.

Representing nodes:
    To represent the nodes of our tree, we can define a simple class. This class
    will conveniently store a node's header, children, and metadata. The node's
    children are represented as a list of other instances of our class. See Node
    class.

Building a node from numbers:
    We need to read the numbers provided as input and build the corresponding
    tree of nodes. The first node will start at the beginning of our list of
    numbers, but to build that node's children we will need to read from where
    we left off. A recursive function is great for this. See Node.load method.

Building the tree:
    Building the tree is only a question of building the root node of our tree.
    All the other nodes in the tree will be built by our recursive build method.
    See _build_tree function.

Summing metadata:
    We can sum all the metadata values in our tree with a simple recursive
    function. See _sum_metadata function.

Part 1:
    All we need to do to solve the first part of the day's puzzle is to read
    the numbers from our input, build the corresponding tree, and sum all the
    metadata of that tree. See get_metadata_sum function.

A node's value:
    If a node has no children, its value can be computed with Python's sum
    function. If it has children, we can sum the value of each of the child
    nodes that match the parent node's metadata. A simple recursive approach
    works well here. See _get_node_value function.

Part 2:
    To solve the second part of the puzzle, we need to read the numbers in our
    input, build the corresponding tree, and compute the value of the root node.
    See get_root_value function.
"""

from typing import List

import utils


class Node:  # pylint: disable=R0903
    """Represents a node of a tree.

    Attributes:
        header: A pair of numbers representing the quantity of child nodes and
            the quantity of metadata entries.
        children: A list of child nodes.
        metadata: A list of metadata entries represented as numbers.
    """

    def __init__(self) -> None:
        self.header = [0, 0]
        self.children = []
        self.metadata = []

    def load(self, numbers: List[int], start_index: int = 0) -> int:
        """Loads a node from the given list of numbers.

        Initialises the node based on the numbers starting at start_index. If
        the node contains other nodes, it will load them as well.

        Args:
            numbers: A list of numbers representing a node tree.
            start_index: The index of the first number representing the node.

        Returns:
            The start index of the next node.
        """
        index = start_index
        self.header = numbers[index:index + 2]
        index += 2
        for _ in range(self.header[0]):
            child = Node()
            index = child.load(numbers, index)
            self.children.append(child)
        self.metadata = numbers[index:index + self.header[1]]
        index += self.header[1]
        return index


def _read_numbers(input_string: str) -> List[int]:
    """Reads numbers from a given input string.

    Args:
        input_string: A string containing the day's input.

    Returns:
        A list of numbers.
    """
    return [int(n) for n in input_string.split()]


def _build_tree(numbers: List[int]) -> Node:
    """Builds a tree of nodes from a given list of numbers.

    Args:
        numbers: A list of numbers representing an encoded node tree.

    Returns:
        The parent node of the tree (contains all other nodes).
    """
    tree = Node()
    tree.load(numbers)
    return tree


def _sum_metadata(tree: Node) -> int:
    """Sums the metadata values of all nodes in the tree.

    Args:
        tree: The parent node of the tree.

    Returns:
        The sum of all metadata in the tree.
    """
    return sum(tree.metadata) + sum(
        [_sum_metadata(child) for child in tree.children])


def _get_node_value(node: Node) -> int:
    """Sums the values of all nodes in the tree.

    Args:
        node: The parent node of the tree.

    Returns:
        The sum of all node values in the tree.
    """
    if not node.children:
        return sum(node.metadata)
    return sum([
        _get_node_value(node.children[index - 1])
        for index in node.metadata
        if 0 <= index - 1 < len(node.children)
    ])


def get_metadata_sum(input_string: str) -> int:
    """Computes the sum of all metadata in all nodes.

    Args:
        input_string: The puzzle input.

    Returns:
        An integer representing the sum of all metadata in the node tree.
    """
    numbers = _read_numbers(input_string)
    tree = _build_tree(numbers)
    metadata_sum = _sum_metadata(tree)
    return metadata_sum


def get_root_value(input_string: str) -> int:
    """Computes the value of the root node.

    Args:
        input_string: The puzzle input.

    Returns:
        An integer representing the value of the root node.
    """
    numbers = _read_numbers(input_string)
    tree = _build_tree(numbers)
    root_value = _get_node_value(tree)
    return root_value


def _run_tests() -> None:
    """Tests solution."""
    assert get_metadata_sum('2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2') == 138
    assert get_root_value('2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2') == 66


def _print_answers(metadata_sum: int, root_value: int) -> None:
    """Prints answers."""
    print('Answers for day 08:')
    print(f'  Metadata sum: {metadata_sum}')
    print(f'  Root node value: {root_value}')


def main() -> None:
    """Runs tests and prints answers to day's puzzle."""
    _run_tests()
    input_string = utils.read_input(8)
    metadata_sum = get_metadata_sum(input_string)
    root_value = get_root_value(input_string)
    _print_answers(metadata_sum, root_value)


if __name__ == '__main__':
    main()
