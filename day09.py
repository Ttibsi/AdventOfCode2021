# Part 1: Find all of the low points on your heightmap. What is the sum of the
# risk levels of all low points on your heightmap?
# Part 2: What do you get if you multiply together the sizes of the three
# largest basins?
from collections import defaultdict

import pyperclip as pyp  # type: ignore
import pytest


def parse_data(rawData: list[str]) -> list[list[int]]:
    data_map: list[list[int]] = []

    for item in rawData:
        row = [int(i) for i in item if i != "\n"]
        data_map.append(row)

    return data_map


def build_dict(data_map: list[list[int]]) -> dict[tuple[int, int], int]:
    world_map = defaultdict(lambda: 9)

    for row, line in enumerate(data_map):
        for col, val in enumerate(line):
            world_map[(row, col)] = val

    return world_map


def direction_checks(
    world_map: dict[tuple[int, int], int], coords: tuple[int, int], val: int
) -> bool:
    x, y = coords
    checks = []

    checks.append(True if world_map[(x + 1, y)] > val else False)
    checks.append(True if world_map[(x - 1, y)] > val else False)
    checks.append(True if world_map[(x, y + 1)] > val else False)
    checks.append(True if world_map[(x, y - 1)] > val else False)

    return all(checks)


def calculate_risk_level(rawData: list[str]) -> tuple[int, list[tuple[int, int]]]:

    total_risk_lvl = 0
    minimas: list[tuple[int, int]] = []
    data_map: list[list[int]] = parse_data(rawData)
    world_map = build_dict(data_map)

    # Turn it into a tuple to avoid a runtimeError
    for (x, y), n in tuple(world_map.items()):
        if direction_checks(world_map, (x, y), n):
            minimas.append((x, y))
            total_risk_lvl += 1 + n

    return (total_risk_lvl, minimas)


def find_basins(
    world_map: dict[tuple[int, int], int], minimas: list[tuple[int, int]]
) -> list[int]:
    basins: list[int] = []

    for (x, y) in minimas:
        traversed = set()
        items: list[tuple[int, int]] = [(x, y)]

        while items:
            x, y = items.pop()
            traversed.add((x, y))

            if world_map[(x + 1, y)] != 9 and (x + 1, y) not in traversed:
                items.append((x + 1, y))
            if world_map[(x - 1, y)] != 9 and (x - 1, y) not in traversed:
                items.append((x - 1, y))
            if world_map[(x, y + 1)] != 9 and (x, y + 1) not in traversed:
                items.append((x, y + 1))
            if world_map[(x, y - 1)] != 9 and (x, y - 1) not in traversed:
                items.append((x, y - 1))

        basins.append(len(traversed))

    return basins


def avoidance_zones(rawData: list[str], minimas: list[tuple[int, int]]) -> int:
    total_value = 0
    data_map: list[list[int]] = parse_data(rawData)
    world_map: dict[tuple[int, int], int] = build_dict(data_map)

    list_of_basins = find_basins(world_map, minimas)
    list_of_basins.sort(reverse=True)
    print(list_of_basins)

    total_value = list_of_basins[0] * list_of_basins[1] * list_of_basins[2]

    return total_value


def main(filename: str) -> int:
    with open(filename) as inputData:
        rawData = inputData.readlines()

    if "sri" in filename:
        print("Browser: Safari")
    elif "ff" in filename:
        print("Browser: Firefox")

    p1 = calculate_risk_level(rawData)
    pyp.copy(p1[0])
    print(f"Part 1: {p1[0]}")

    p2 = avoidance_zones(rawData, p1[1])
    pyp.copy(p2)
    print(f"Part 2: {p2}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main("input_ff/day09.txt"))
    # raise SystemExit(main("input_sri/day09.txt"))


# Tests
test_data = [
    "2199943210",
    "3987894921",
    "9856789892",
    "8767896789",
    "9899965678",
]

test_minimas = [
    (0, 1),
    (0, 9),
    (2, 2),
    (4, 6),
]


# Part 1 test
@pytest.mark.parametrize(
    ("input_data", "expected"),
    [
        (test_data, 15),
    ],
)
def test_calculate_risk_level(input_data: list[str], expected: int) -> None:
    assert calculate_risk_level(input_data)[0] == expected


# Part 2 test
@pytest.mark.parametrize(
    ("input_data", "minimas", "expected"),
    [
        (test_data, test_minimas, 1134),
    ],
)
def test_avoidance_zones(
    input_data: list[str], minimas: list[tuple[int, int]], expected: int
) -> None:
    assert avoidance_zones(input_data, minimas) == expected
