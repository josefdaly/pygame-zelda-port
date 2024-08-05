import math
import numpy

def find_map_tile_location(n, columns, tile_height, tile_width):

    x = (n % columns) * tile_width
    y = math.floor(n / columns) * tile_height

    return y, x


def parse_overworld_data(file, split=None):
    matrix = []
    with open(file) as f:
        for line in f.readlines():
            if not split:
                matrix.append(list(line.strip()))
            else:
                matrix.append(line.strip().split(split))
    return numpy.array(matrix)


def blockshaped(arr, nrows, ncols):
    """
    Return an array of shape (n, nrows, ncols) where
    n * nrows * ncols = arr.size

    If arr is a 2D array, the returned array should look like n subblocks with
    each subblock preserving the "physical" layout of arr.
    """
    h, w = arr.shape
    assert h % nrows == 0, f"{h} rows is not evenly divisible by {nrows}"
    assert w % ncols == 0, f"{w} cols is not evenly divisible by {ncols}"
    return (arr.reshape(h//nrows, nrows, -1, ncols)
               .swapaxes(1,2)
               .reshape(-1, nrows, ncols))


def hex_reference_to_integer(hex):
    i = int(hex, 16)
    return int(((i - (i % 20))/20 * 18) + (i % 20))
