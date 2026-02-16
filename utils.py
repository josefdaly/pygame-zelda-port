from __future__ import annotations
import math
import os
from typing import Any

import numpy
import numpy.typing as npt


TILESET_COLS = 20
TILESET_ROW_STRIDE = 18


def find_map_tile_location(
    n: int, columns: int, tile_height: int, tile_width: int
) -> tuple[int, int]:
    x = (n % columns) * tile_width
    y = math.floor(n / columns) * tile_height
    return y, x


def parse_overworld_data(file: str, split: str | None = None) -> npt.NDArray[Any]:
    if not os.path.exists(file):
        raise FileNotFoundError(f"Map file not found: {file}")

    matrix: list[list[str]] = []
    with open(file) as f:
        for line in f.readlines():
            if not split:
                matrix.append(list(line.strip()))
            else:
                matrix.append(line.strip().split(split))
    return numpy.array(matrix)


def blockshaped(arr: npt.NDArray[Any], nrows: int, ncols: int) -> npt.NDArray[Any]:
    """
    Return an array of shape (n, nrows, ncols) where
    n * nrows * ncols = arr.size

    If arr is a 2D array, the returned array should look like n subblocks with
    each subblock preserving the "physical" layout of arr.
    """
    h, w = arr.shape
    if h % nrows != 0:
        raise ValueError(f"{h} rows is not evenly divisible by {nrows}")
    if w % ncols != 0:
        raise ValueError(f"{w} cols is not evenly divisible by {ncols}")
    return (
        arr.reshape(h // nrows, nrows, -1, ncols)
        .swapaxes(1, 2)
        .reshape(-1, nrows, ncols)
    )


def hex_reference_to_integer(hex_str: str) -> int:
    try:
        i = int(hex_str, 16)
    except ValueError:
        raise ValueError(f"Invalid hex string: {hex_str}")
    row = i // TILESET_COLS
    col = i % TILESET_COLS
    return row * TILESET_ROW_STRIDE + col


def hex_reference_to_integer_from_int(value: int | str) -> int:
    """Convert a tile reference (hex string or int) to tileset index."""
    try:
        if isinstance(value, str):
            i = int(value, 16)
        else:
            i = int(value)
    except (ValueError, TypeError):
        raise ValueError(f"Cannot convert {value} to integer")
    row = i // TILESET_COLS
    col = i % TILESET_COLS
    return row * TILESET_ROW_STRIDE + col
