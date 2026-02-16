import numpy as np
import pytest
from unittest.mock import MagicMock, patch


class TestTilemap:
    @pytest.fixture
    def mock_tileset(self):
        tileset = MagicMock()
        tileset.tiles = [MagicMock() for _ in range(50)]
        return tileset

    @pytest.fixture
    def mock_tilemap_image(self):
        with patch("tilemap.pygame.Surface") as mock_surface:
            mock_image = MagicMock()
            mock_surface.return_value = mock_image
            yield mock_image

    def test_set_room_valid_data(self, mock_tileset, mock_tilemap_image):
        from tilemap import Tilemap

        tilemap = Tilemap(
            mock_tileset, size=(4, 4), tile_width=16, tile_height=16, map_offset=65
        )

        room = np.array(
            [
                [0, 0, 1, 1],
                [0, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
            ]
        )

        collision = np.array(
            [
                ["X", "X", " ", " "],
                ["X", " ", " ", " "],
                [" ", " ", " ", " "],
                [" ", " ", " ", " "],
            ]
        )

        tilemap.set_room(room, collision, convert_tile_reference=lambda x: int(x))

        assert tilemap.map.shape == (4, 4)
        assert len(tilemap.collision_rects) == 3

    def test_set_room_shape_mismatch(self, mock_tileset):
        from tilemap import Tilemap

        tilemap = Tilemap(
            mock_tileset, size=(4, 4), tile_width=16, tile_height=16, map_offset=65
        )

        room = np.array(
            [
                [0, 0],
                [0, 0],
            ]
        )

        collision = np.array(
            [
                [" ", " "],
                [" ", " "],
            ]
        )

        with pytest.raises(ValueError, match="does not match map size"):
            tilemap.set_room(room, collision)

    def test_tile_index_out_of_bounds(self, mock_tileset):
        from tilemap import Tilemap

        tilemap = Tilemap(
            mock_tileset, size=(2, 2), tile_width=16, tile_height=16, map_offset=65
        )

        room = np.array(
            [
                [999, 0],
                [0, 0],
            ]
        )

        collision = np.array(
            [
                [" ", " "],
                [" ", " "],
            ]
        )

        with pytest.raises(ValueError, match="out of range"):
            tilemap.set_room(room, collision, convert_tile_reference=lambda x: x)

    def test_empty_tileset_error(self):
        from tilemap import Tilemap

        mock_tileset = MagicMock()
        mock_tileset.tiles = []

        tilemap = Tilemap(
            mock_tileset, size=(2, 2), tile_width=16, tile_height=16, map_offset=65
        )

        room = np.array(
            [
                [0, 0],
                [0, 0],
            ]
        )

        collision = np.array(
            [
                [" ", " "],
                [" ", " "],
            ]
        )

        with pytest.raises(ValueError, match="no tiles loaded"):
            tilemap.set_room(room, collision)
