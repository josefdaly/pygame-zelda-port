import os
import tempfile
from unittest.mock import MagicMock, patch

import numpy as np
import pytest


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_map_data():
    return np.array(
        [
            ["3d", "3d", "2", "2"],
            ["3d", "2", "2", "2"],
            ["2", "2", "2", "2"],
            ["2", "2", "2", "2"],
        ]
    )


@pytest.fixture
def sample_collision_data():
    return np.array(
        [
            ["X", "X", " ", " "],
            ["X", " ", " ", " "],
            [" ", " ", " ", " "],
            [" ", " ", " ", " "],
        ]
    )


@pytest.fixture
def mock_pygame():
    with (
        patch("pygame.image.load") as mock_load,
        patch("pygame.Surface") as mock_surface,
        patch("pygame.transform.flip") as mock_flip,
    ):
        mock_surface_instance = MagicMock()
        mock_surface_instance.get_rect.return_value = MagicMock()
        mock_load.return_value = mock_surface_instance
        mock_flip.return_value = mock_surface_instance

        yield {
            "surface": mock_surface_instance,
            "load": mock_load,
            "flip": mock_flip,
        }
