# Part 1: What do you get if you take the quantity of the most common element
# and subtract the quantity of the least common element?
import copy
import pprint as p
from collections import Counter

import pyperclip as pyp  # type: ignore
import pytest


def parse_input(rawData: str) -> tuple[str, dict[str, str]]:
    lines = rawData.splitlines()
    polymer = lines[0].strip()
    data = {}

    for item in lines[2:]:
        vals = item.split(" -> ")
        data[vals[0]] = vals[1]

    return polymer, data


def get_score(poly: str) -> int:
    char_count: dict[str, int] = Counter()

    for char in poly:
        char_count[char] += 1

    most_common = max(char_count.values())
    least_common = min(char_count.values())
    score = most_common - least_common

    print(char_count)
    return score


def print_data(a, b, c):
    print(f"Polymer={a}, new_val={b}, inst[0]={c[0]}")


def get_previous_letters(poly: str, extra: bool = False) -> str:
    if not extra:
        return poly[-2:]
    else:
        return poly[-3] + poly[-1]


def poly_growth(polymer: str, data: dict[str, str], steps: int) -> str:
    for _ in range(steps):
        new_polymer = ""
        is_extra = False

        for letter in polymer:
            new_polymer += letter

            if len(new_polymer) < 2:
                continue

            sample = get_previous_letters(new_polymer, is_extra)

            if sample in data.keys():
                new_polymer += data[sample]
                is_extra = True
            else:
                is_extra = False

        polymer = new_polymer

    return polymer


# Part 1
def form_polymers(rawData: str, steps: int) -> int:
    polymer, data = parse_input(rawData)
    poly = poly_growth(polymer, data, steps)
    score = get_score(poly)
    return score


def main(filename: str) -> int:
    with open(filename) as inputData:
        rawData = inputData.read()

    if "sri" in filename:
        print("Browser: Safari")
    elif "ff" in filename:
        print("Browser: Firefox")

    p1 = form_polymers(rawData, 10)
    pyp.copy(p1)
    print(f"Part 1: {p1}")

    # p2 = 0
    # pyp.copy(p2)
    # print(f"Part 2: {p2}")

    return 0


if __name__ == "__main__":
    # raise SystemExit(main("input_ff/day14.txt"))
    raise SystemExit(main("input_sri/day14.txt"))


# Tests
test_data = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""


# Part 1 test
@pytest.mark.parametrize(
    ("input_data", "steps", "expected"),
    [
        (test_data, 10, 1588),
    ],
)
def test_form_polymers(input_data, steps, expected):
    assert form_polymers(input_data, steps) == expected


@pytest.mark.parametrize(
    ("input_", "steps", "expected"),
    (
        (test_data, 0, "NNCB"),
        (test_data, 1, "NCNBCHB"),
        (test_data, 2, "NBCCNBBBCBHCB"),
        (test_data, 3, "NBBBCNCCNBBNBNBBCHBHHBCHB"),
        (test_data, 4, "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"),
    ),
)
def test_poly_growth(input_, steps, expected):
    poly, data = parse_input(input_)
    assert poly_growth(poly, data, steps) == expected


# Part 2 test
"""
@pytest.mark.parametrize(
    ("input_data", "expected"),
    [
        (test_data, 0),
    ]
)
def test_f(input_data: list[int], expected: int) -> None:
    assert f(input_data) == expected
"""
