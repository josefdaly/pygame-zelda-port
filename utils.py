import math

def find_map_tile_location(n, columns, tile_height, tile_width):

    x = (n % columns) * tile_width
    y = math.floor(n / columns) * tile_height

    return y, x
