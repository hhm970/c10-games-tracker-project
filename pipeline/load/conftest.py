import pytest


@pytest.fixture
def test_game_data():
    return [["Stardew Valley", "A great game", 4.99, "ConcernedApe",
            "ConcernedApe", "2000-11-29 14:48:00", 5, 12,
             ["A", "Great", "Game"], [1, 2, 3]]]
