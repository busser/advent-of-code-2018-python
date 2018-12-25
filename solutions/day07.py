"""Solution to day 07 of the Advent of Code."""

import heapq
import string
from typing import Any, Dict, List, Set, Tuple

import utils


class Graph:
    """Represents a graph.

    Attributes:
        adj_list: A dictionary that maps each vertex of the graph to the
            vertices it is connected to.
    """

    def __init__(self) -> None:
        self._adj_list = {}

    def add_vertex(self, vertex: Any) -> None:
        """Adds a vertex to the graph.

        Args:
            vertex: The vertex to add.
        """
        if vertex not in self._adj_list:
            self._adj_list[vertex] = []

    def add_edge(self, u: Any, v: Any) -> None:  # pylint: disable=C0103
        """Adds an edge to the graph.

        Args:
            u: The vertex the edge comes from.
            v: The vertex the edge goes to.
        """
        self.add_vertex(u)
        self.add_vertex(v)
        self._adj_list[u].append(v)

    def _topological_sort_worker(self, vertex: Any, visited: Set[Any],
                                 stack: List[Any]):
        """A recursive worker function use by topological sort.

        Applies a DFS-like search on the graph, starting at the given vertex.
        Once the search is complete for all of the vertex's children, the vertex
        is added to the shared stack.

        Args:
            vertex: The vertex to start the search from.
            visited: A set containing all vertices that have been visited.
            stack: A stack containing the vertices in reversed topological
                order.
        """
        visited.add(vertex)
        for child in self._adj_list[vertex]:
            if child not in visited:
                self._topological_sort_worker(child, visited, stack)
        stack.append(vertex)

    def topological_sort(self) -> List[Any]:
        """Provides the graph's vertices in topological order.

        There are no guarantees on which topological order will be provided.

        Returns:
            A list of vertices in topological order.
        """
        visited = set()
        stack = []
        for vertex, _ in self._adj_list.items():
            if vertex not in visited:
                self._topological_sort_worker(vertex, visited, stack)
        stack.reverse()
        return stack

    def specific_topological_sort(self) -> List[Any]:
        """Provides the graph's vertices in a very specific topological order.

        See https://adventofcode.com/2018/day/7 Part 1 for details.

        Returns:
            A list of vertices in topological order.
        """
        completed = []
        parent_count = {vertex: 0 for vertex, _ in self._adj_list.items()}
        for _, children in self._adj_list.items():
            for child in children:
                parent_count[child] += 1
        available = [
            vertex for vertex, count in parent_count.items() if count == 0
        ]
        heapq.heapify(available)
        while available:
            vertex = heapq.heappop(available)
            completed.append(vertex)
            for child in self._adj_list[vertex]:
                parent_count[child] -= 1
                if parent_count[child] == 0:
                    heapq.heappush(available, child)
        return completed

    def multiworker_step_sort(self, durations: Dict[Any, int],
                              workers: int = 5) -> List[Any]:
        """Provides the graph's vertices in a very specific topological order.

        See https://adventofcode.com/2018/day/7 Part 2 for details.

        Args:
            durations: A dictionary that maps each vertex to the amount of time
                required to complete the corresponding step.
            workers: The number of workers working on the steps.

        Returns:
            A list of vertices in topological-like order.
        """
        completed = []
        parent_count = {vertex: 0 for vertex, _ in self._adj_list.items()}
        for _, children in self._adj_list.items():
            for child in children:
                parent_count[child] += 1
        available = [
            vertex for vertex, count in parent_count.items() if count == 0
        ]
        progress = [None] * workers
        heapq.heapify(available)
        time_count = -1  # One extra iteration is required to get started.
        while len(completed) < len(self._adj_list):
            time_count += 1
            for worker, work in enumerate(progress):
                # Work on in-progress steps for 1 time unit
                if work is not None:
                    (step, time_left) = work
                    time_left -= 1

                    if time_left > 0:
                        progress[worker] = (step, time_left)
                        continue

                    completed.append(step)
                    for child in self._adj_list[step]:
                        parent_count[child] -= 1
                        if parent_count[child] == 0:
                            heapq.heappush(available, child)
                    progress[worker] = None

            for worker, work in enumerate(progress):
                # Assign steps to free workers
                if work is None:
                    if available:
                        step = heapq.heappop(available)
                        progress[worker] = (step, durations[step])
                    continue

        return completed, time_count


def _read_dependencies(input_string: str) -> List[Tuple[str, str]]:
    """Reads step dependencies from a given input string.

    Args:
        input_string: A string containing the day's input.

    Returns:
        A list of dependencies represented as tuples of step names. The first
        step must be completed before the second.
    """
    dependencies = []
    for line in input_string.split('\n'):
        words = line.split()
        dependencies.append((words[1], words[7]))
    return dependencies


def _build_dependency_graph(dependencies: List[Tuple[str, str]]) -> Graph:
    """Builds a directed acyclic graph from a list of dependencies.

    Args:
        dependencies: A list dependencies represented as pairs of step names.

    Returns:
        A directed acyclic graph representing the dependencies.
    """
    graph = Graph()
    for dependency in dependencies:
        graph.add_edge(*dependency)
    return graph


def _get_step_durations(  # pylint: disable=W0102
        steps: List[Any] = list(string.ascii_uppercase),
        offset: int = 61) -> Dict[Any, int]:
    return {step: offset + i for i, step in enumerate(steps)}


def get_step_order(input_string: str) -> str:
    """Finds the order the instructions should be completed in.

    Args:
        input_string: The puzzle input.

    Returns:
        A string with the step names written in order.
    """
    dependencies = _read_dependencies(input_string)
    graph = _build_dependency_graph(dependencies)
    return "".join(graph.specific_topological_sort())


def get_multiworker_total_time(input_string: str,
                               offset: int = 61,
                               workers: int = 5) -> str:
    """Finds the total time required by multiple workers to complete all steps.

    Args:
        input_string: The puzzle input.
        offset: The offset in seconds of the step durations. Step A will take
            offset seconds, step B offset+1, etc.
        workers: The number of workers working on the steps in parallel.

    Returns:
        An integer representing the total time required in seconds.
    """
    dependencies = _read_dependencies(input_string)
    graph = _build_dependency_graph(dependencies)
    step_durations = _get_step_durations(offset=offset)
    _, total_time = graph.multiworker_step_sort(step_durations, workers)
    return total_time


def _run_tests() -> None:
    """Tests solution."""
    assert get_step_order(
        'Step C must be finished before step A can begin.\n'
        'Step C must be finished before step F can begin.\n'
        'Step A must be finished before step B can begin.\n'
        'Step A must be finished before step D can begin.\n'
        'Step B must be finished before step E can begin.\n'
        'Step D must be finished before step E can begin.\n'
        'Step F must be finished before step E can begin.') == 'CABDFE'
    assert get_multiworker_total_time(
        'Step C must be finished before step A can begin.\n'
        'Step C must be finished before step F can begin.\n'
        'Step A must be finished before step B can begin.\n'
        'Step A must be finished before step D can begin.\n'
        'Step B must be finished before step E can begin.\n'
        'Step D must be finished before step E can begin.\n'
        'Step F must be finished before step E can begin.',
        offset=1,
        workers=2) == 15


def _print_answers(step_order: str, multiworker_total_time: str) -> None:
    """Prints answers.

    Args:
        step_order: The order to complete the instructions in.
        multiworker_total_time: The total number of seconds required to complete
            all steps with multiple workers.
    """
    print('Answers for day 07:')
    print(f'  Step order: {step_order}')
    print(f'  Multi-worker total time: {multiworker_total_time}')


def main() -> None:
    """Runs tests and prints answers to day's puzzle."""
    _run_tests()
    input_string = utils.read_input(7)
    step_order = get_step_order(input_string)
    multiworker_total_time = get_multiworker_total_time(input_string)
    _print_answers(step_order, multiworker_total_time)


if __name__ == '__main__':
    main()
