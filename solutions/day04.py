"""Solution to day 04 of the Advent of Code.

Reading input:
    Each line in the input is effectively a log with a timestamp. We can store
    each timestamp as a date and store the rest as a string. Once we have all
    the records, we can sort them by date. See _read_records function.

Mapping the records to each guard:
    Once the records are sorted, we can easily map them to the corresponding
    guard. This allows us to build a dictionary where each key is a guard's ID
    (an integer) and each value is the list of records pertaining to the guard.
    See _map_records_to_guards function.

Total time spent sleeping:
    A day's logs always start with the guard beginning their shift, and after
    that logs come in pairs: the guard falls asleep and later on wakes up. For
    each pair we can get the difference between both dates (stored as a
    timedelta in Python). Summing those differences for all log pairs of a given
    guard gives us the total time they spent sleeping. See _compute_sleep_total
    function.

Guard that slept the most:
    Finding the guard that slept the most is a question of computing how much
    each guard has slept and finding the maximum. See _get_guard_with_most_sleep
    function.

Favorite minute:
    Finding the minute a guard has slept through the most can be done by
    counting how many times they slept through each minute and finding the
    maximum. See _get_favorite_minute function.

Part 1:
    Once we have the ID of the guard that slept the most and their favorite
    minute to sleep through, all we need to do is multiply those two integers.
    See get_strategy_1 function.

Sneakiest minute:
    The best minute to sneak into the prototype suit manufacturing lab is the
    minute that is most slept through by any one guard. To find it, we can find
    each guard's favorite minute and how many times they've slept through it.
    Once we have that, all we need is to find the maximum. See
    _get_sneakiest_minute function.

Part 2:
    Once we have the sneakiest minute and the ID of the guard who's favorite
    minute it is, we just need to multiply those two integers. See
    get_strategy_2 function.
"""

import datetime
import re
from typing import Dict, List, NamedTuple, Tuple

import utils


class Record(NamedTuple):  # pylint: disable=R0903
    """Represents a record of guard activity.

    Attributes:
        date: The date and time the record was taken.
        content: The record's content.
    """
    date: datetime.datetime
    content: str


def _read_records(input_string: str) -> List[Record]:
    """Reads records of guard activity from a given input string and sorts them.

    Args:
        input_string: A string containing the day's input.

    Returns:
        A list of records sorted by date.
    """
    records = []
    for line in input_string.split('\n'):
        search = re.search('^\\[(.*)\\] (.*)$', line)
        record = Record(
            datetime.datetime.strptime(search.group(1), '%Y-%m-%d %H:%M'),
            search.group(2))
        records.append(record)
    return sorted(records)


def _map_records_to_guards(records: List[Record]) -> Dict[int, List[Record]]:
    """Maps each record to the guard the record is about.

    Args:
        records: A list of records of guard activity sorted by date.

    Returns:
        A dictionary where the keys are guards IDs and the values are lists of
        records sorted by date.
    """
    guard_records = {}
    guard_id = None
    for record in records:
        if record.content.startswith('Guard'):
            guard_id = int(re.findall('[0-9]+', record.content)[0])
            if guard_id not in guard_records.keys():
                guard_records[guard_id] = []
        guard_records[guard_id].append(record)
    return guard_records


def _compute_sleep_total(records: List[Record]) -> datetime.timedelta:
    """Computes how long a guard has slept based on their records.

    Args:
        records: A list of records for a single guard.

    Returns:
        The total amount of time the guard has slept.
    """
    time_slept = datetime.timedelta(0)
    fell_asleep_at = None
    for record in records:
        if record.content == 'falls asleep':
            fell_asleep_at = record.date
        elif record.content == 'wakes up':
            time_slept += record.date - fell_asleep_at
    return time_slept


def _get_guard_with_most_sleep(guard_records: Dict[int, List[Record]]) -> int:
    guard_total_sleep_times = {
        guard_id: _compute_sleep_total(records)
        for guard_id, records in guard_records.items()
    }
    return max(guard_total_sleep_times, key=guard_total_sleep_times.get)


def _get_favorite_minute(
        records: List[Record]) -> Tuple[int, datetime.timedelta]:
    """Finds which minute a guard was most asleep based on their records.

    Args:
        records: A list of records for a single guard.

    Returns:
        The minute where the guard was most asleep, as well as how many times
        they slept through this minute.
    """
    minute_count = {i: 0 for i in range(60)}
    for record in records:
        if record.content == 'falls asleep':
            fell_asleep_at = record.date
        elif record.content == 'wakes up':
            for minute in range(fell_asleep_at.minute, record.date.minute):
                minute_count[minute] += 1
    favorite_minute = max(minute_count, key=minute_count.get)
    return (favorite_minute, minute_count[favorite_minute])


def _get_sneakiest_minute(
        guard_records: Dict[int, List[Record]]) -> Tuple[int, int]:
    """Finds the minute most slept by any one guard based on all records.

    Args:
        guard_records: A dictionary containing the records of each guard.

    Returns:
        The minute most slept through by any one guard, as well as the guard in
        question.
    """
    sleepy_guard_id, max_times_slept, favorite_minute = None, 0, None
    for guard_id, records in guard_records.items():
        minute, times_slept = _get_favorite_minute(records)
        if times_slept > max_times_slept:
            max_times_slept = times_slept
            favorite_minute = minute
            sleepy_guard_id = guard_id
    return (favorite_minute, sleepy_guard_id)


def get_strategy_1(input_string: str) -> int:
    """Find the guard with the most minutes asleep and their most slept minute.

    Args:
        input_string: The puzzle input.

    Returns:
        The product of the guard's ID and the minute they slept through the
        most.
    """
    records = _read_records(input_string)
    guard_records = _map_records_to_guards(records)
    sleepy_guard_id = _get_guard_with_most_sleep(guard_records)
    favorite_minute, _ = _get_favorite_minute(guard_records[sleepy_guard_id])
    return sleepy_guard_id * favorite_minute


def get_strategy_2(input_string: str) -> int:
    """Find the guard most frequently asleep on the same minute.

    Args:
        input_string: The puzzle input.

    Returns:
        The product of the guard's ID and the minute they slept through the
        most.
    """
    records = _read_records(input_string)
    guard_records = _map_records_to_guards(records)
    favorite_minute, sleepy_guard_id = _get_sneakiest_minute(guard_records)
    return sleepy_guard_id * favorite_minute


def _run_tests() -> None:
    """Tests solution."""
    assert get_strategy_1('[1518-11-01 00:00] Guard #10 begins shift\n'
                          '[1518-11-01 00:05] falls asleep\n'
                          '[1518-11-01 00:25] wakes up\n'
                          '[1518-11-01 00:30] falls asleep\n'
                          '[1518-11-01 00:55] wakes up\n'
                          '[1518-11-01 23:58] Guard #99 begins shift\n'
                          '[1518-11-02 00:40] falls asleep\n'
                          '[1518-11-02 00:50] wakes up\n'
                          '[1518-11-03 00:05] Guard #10 begins shift\n'
                          '[1518-11-03 00:24] falls asleep\n'
                          '[1518-11-03 00:29] wakes up\n'
                          '[1518-11-04 00:02] Guard #99 begins shift\n'
                          '[1518-11-04 00:36] falls asleep\n'
                          '[1518-11-04 00:46] wakes up\n'
                          '[1518-11-05 00:03] Guard #99 begins shift\n'
                          '[1518-11-05 00:45] falls asleep\n'
                          '[1518-11-05 00:55] wakes up') == 240
    assert get_strategy_2('[1518-11-01 00:00] Guard #10 begins shift\n'
                          '[1518-11-01 00:05] falls asleep\n'
                          '[1518-11-01 00:25] wakes up\n'
                          '[1518-11-01 00:30] falls asleep\n'
                          '[1518-11-01 00:55] wakes up\n'
                          '[1518-11-01 23:58] Guard #99 begins shift\n'
                          '[1518-11-02 00:40] falls asleep\n'
                          '[1518-11-02 00:50] wakes up\n'
                          '[1518-11-03 00:05] Guard #10 begins shift\n'
                          '[1518-11-03 00:24] falls asleep\n'
                          '[1518-11-03 00:29] wakes up\n'
                          '[1518-11-04 00:02] Guard #99 begins shift\n'
                          '[1518-11-04 00:36] falls asleep\n'
                          '[1518-11-04 00:46] wakes up\n'
                          '[1518-11-05 00:03] Guard #99 begins shift\n'
                          '[1518-11-05 00:45] falls asleep\n'
                          '[1518-11-05 00:55] wakes up') == 4455


def _print_answers(strategy_1: int = None, strategy_2: int = None) -> None:
    """Prints answers.

    Args:
        strategy_1: The result of the first strategy.
        strategy_2: The result of the second strategy."""
    print('Answers for day 04:')
    print(f'  Strategy 1: {strategy_1}')
    print(f'  Strategy 2: {strategy_2}')


def main() -> None:
    """Runs tests and prints answers to day's puzzle."""
    _run_tests()
    input_string = utils.read_input(4)
    strategy_1 = get_strategy_1(input_string)
    strategy_2 = get_strategy_2(input_string)
    _print_answers(strategy_1, strategy_2)


if __name__ == '__main__':
    main()
