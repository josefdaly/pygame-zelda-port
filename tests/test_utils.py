import os
import tempfile

import numpy as np
import pytest

from utils import (
    find_map_tile_location,
    parse_overworld_data,
    blockshaped,
    hex_reference_to_integer,
    hex_reference_to_integer_from_int,
)


class TestFindMapTileLocation:
    def test_center_tile(self):
        result = find_map_tile_location(117, 16, 16, 16)
        assert result == (112, 80)

    def test_first_tile(self):
        result = find_map_tile_location(0, 16, 16, 16)
        assert result == (0, 0)

    def test_second_row(self):
        result = find_map_tile_location(16, 16, 16, 16)
        assert result == (16, 0)

    def test_second_column(self):
        result = find_map_tile_location(1, 16, 16, 16)
        assert result == (0, 16)

    def test_last_tile_in_row(self):
        result = find_map_tile_location(15, 16, 16, 16)
        assert result == (0, 240)


class TestBlockshaped:
    def test_simple_reshape(self):
        arr = np.arange(16).reshape(4, 4)
        result = blockshaped(arr, 2, 2)
        assert result.shape == (4, 2, 2)

    def test_preserves_data(self):
        arr = np.array(
            [
                [1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12],
                [13, 14, 15, 16],
            ]
        )
        result = blockshaped(arr, 2, 2)
        assert result.shape == (4, 2, 2)
        np.testing.assert_array_equal(result[0], [[1, 2], [5, 6]])

    def test_invalid_rows(self):
        arr = np.array([[1, 2], [3, 4]])
        with pytest.raises(ValueError, match="not evenly divisible"):
            blockshaped(arr, 3, 2)

    def test_invalid_cols(self):
        arr = np.array([[1, 2], [3, 4]])
        with pytest.raises(ValueError, match="not evenly divisible"):
            blockshaped(arr, 2, 3)


class TestHexReferenceToInteger:
    def test_zero(self):
        assert hex_reference_to_integer("00") == 0

    def test_single_digit(self):
        assert hex_reference_to_integer("0f") == 15

    def test_double_digit(self):
        assert hex_reference_to_integer("14") == 18

    def test_first_tile(self):
        assert hex_reference_to_integer("3d") == 55

    def test_invalid_hex(self):
        with pytest.raises(ValueError, match="Invalid hex string"):
            hex_reference_to_integer("zz")


class TestHexReferenceToIntegerFromInt:
    def test_int_input(self):
        assert hex_reference_to_integer_from_int(0) == 0

    def test_int_20(self):
        assert hex_reference_to_integer_from_int(20) == 18

    def test_string_input(self):
        assert hex_reference_to_integer_from_int("00") == 0

    def test_string_14(self):
        assert hex_reference_to_integer_from_int("14") == 18

    def test_invalid_input(self):
        with pytest.raises(ValueError, match="Cannot convert"):
            hex_reference_to_integer_from_int(None)


class TestParseOverworldData:
    def test_with_split(self, temp_dir):
        filepath = os.path.join(temp_dir, "test.txt")
        with open(filepath, "w") as f:
            f.write("a b c\n")
            f.write("d e f\n")

        result = parse_overworld_data(filepath, " ")
        assert result.shape == (2, 3)
        assert result[0][0] == "a"
        assert result[1][2] == "f"

    def test_without_split(self, temp_dir):
        filepath = os.path.join(temp_dir, "test.txt")
        with open(filepath, "w") as f:
            f.write("abc\n")
            f.write("def\n")

        result = parse_overworld_data(filepath)
        assert result.shape == (2, 3)
        assert result[0][0] == "a"
        assert result[1][2] == "f"

    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            parse_overworld_data("nonexistent_file.txt")
