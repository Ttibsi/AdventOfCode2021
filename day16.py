# Part 1: Decode the structure of your hexadecimal-encoded BITS transmission;
# what do you get if you add up the version numbers in all packets?
import pprint as p
from collections import Counter
from collections import defaultdict

import pyperclip as pyp  # type: ignore
import pytest


TRANSLATION_TABLE = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def hex_to_bin(msg: str) -> str:
    new_msg = ""
    for char in msg.strip():
        new_msg += TRANSLATION_TABLE[char]

    # while new_msg[-1] == "0":
    #    new_msg = new_msg[:-1]

    return new_msg


def get_header(msg: str) -> tuple[int, int]:
    version = [k for k, v in TRANSLATION_TABLE.items() if v == f"0{msg[:3]}"]
    type_id = [k for k, v in TRANSLATION_TABLE.items() if v == f"0{msg[4:7]}"]
    return int(version[0]), int(type_id[0])


def get_length_type(msg: str) -> tuple[int, str]:
    return int(msg[0]), msg[1:]


def bin_to_den(msg: str) -> int:
    return int(msg, 2)


# Part 1
def packet_decoder(data: str) -> int:
    version_total = 0

    binary_string = hex_to_bin(data)

    """
    get header
        if type is 4
            add every chunk of 5 to a list until chunk[0] == 0
            drop the leading number on each chunk
            make one binary string
            convert that to a number
            any other type
            get next bit (length type ID)
                if 0
                    get next 15 bits
                    convert to denary
                    this is the total length in bits of the sub-packet
                if 1
                    get next 11 bits
                    convert to denary
                    this is the quantity of sub-packets

    add up all version numbers
    """

    header = get_header(binary_string)
    binary_string = binary_string[7:]
    version_total += header[0]

    while binary_string:
        if header[1] == 4:
            packet_value = bin_to_den(binary_string)
        else:
            # operator packets
            length_type, binary_string = get_length_type(binary_string)

            if length_type:
                num_of_sub_packets = bin_to_den(binary_string[:12])
                binary_string = binary_string[12]
            else:
                sub_packet_len = bin_to_den(binary_string[:16])
                binary_string = binary_string[16]

    return version_total


def main(filename: str) -> int:
    with open(filename) as input_data:
        raw_data = input_data.read()

    if "sri" in filename:
        print("Browser: Safari")
    elif "ff" in filename:
        print("Browser: Firefox")

    p1 = packet_decoder(raw_data)
    pyp.copy(p1)
    print(f"Part 1: {p1}")

    # p2 = 0
    # pyp.copy(p2)
    # print(f"Part 2: {p2}")

    return 0


if __name__ == "__main__":
    # raise SystemExit(main("input_ff/day16.txt"))
    raise SystemExit(main("input_sri/day16.txt"))


# Tests
# Part 1 test
@pytest.mark.parametrize(
    ("input_data", "expected"),
    [
        ("8A004A801A8002F478", 16),
        ("620080001611562C8802118E34", 12),
        ("C0015000016115A2E0802F182340", 23),
        ("A0016C880162017C3686B18A3D4780", 31),
    ],
)
def test_packet_decoder(input_data, expected):
    assert packet_decoder(input_data) == expected


bin_test_data_2 = "00111000000000000110111101000101001010010001001000000000"


@pytest.mark.parametrize(
    ("input_data", "expected"),
    [
        ("D2FE28", "110100101111111000101000"),
        ("38006F45291200", bin_test_data_2),
    ],
)
def test_hex_to_bin(input_data, expected):
    assert hex_to_bin(input_data) == expected


# Part 2 test
"""
@pytest.mark.parametrize(
    ("input_data", "expected"),
    [
        (test_data, 0),
    ]
)
def test_f(input_data, expected):
    assert f(input_data) == expected
"""
