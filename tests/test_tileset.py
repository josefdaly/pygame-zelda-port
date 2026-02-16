import os

import pytest


class TestTileset:
    def test_file_not_found(self):
        from tileset import Tileset

        with pytest.raises(FileNotFoundError):
            Tileset("nonexistent.png", size=(16, 16))
