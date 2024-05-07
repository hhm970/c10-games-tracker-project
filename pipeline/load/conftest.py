"""A conftest file that defines functions used in test_load.py."""

import pytest


@pytest.fixture
def test_game_data() -> list[list[list]]:
    """Returns a list of video games, where each game is appropriately formatted."""
    return [["Stardew Valley", "A great game", 4.99, "ConcernedApe",
            "ConcernedApe", "2000-11-29 14:48:00", 5, 1,
             ["A", "Great", "Game"], [1, 2, 3]],
            ["Minecraft", "So blocky so cool", 25.01, "Mojang", "Notch",
             "2024-08-12 10:01:01", 2, 3, ["Herobrine", "Chicken"], [1, 2, 3]]
            ]


@pytest.fixture
def test_game_data2() -> list[list[list]]:
    """Returns a list with a singular video game embedded in it."""
    return [["Among Us", "A great game", 4.99, "Me",
            "Me", "2000-11-29 14:48:00", 5, 2,
             ["A", "Great", "Game"], [1]]
            ]
