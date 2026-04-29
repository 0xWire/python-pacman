import pytest

from game.entities import Vec2

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    ("vector", "factor", "expected"),
    [
        (Vec2(2.0, -3.0), 0.5, Vec2(1.0, -1.5)),
        (Vec2(-4.0, 8.0), -0.25, Vec2(1.0, -2.0)),
    ],
)
def test_scaled_returns_scaled_copy(vector: Vec2, factor: float, expected: Vec2) -> None:
    assert vector.scaled(factor) == expected


@pytest.mark.parametrize(
    ("vector", "expected"),
    [
        (Vec2(0.0, 0.0), True),
        (Vec2(0.0, 1.0), False),
        (Vec2(-1.0, 0.0), False),
    ],
)
def test_is_zero_detects_only_zero_vector(vector: Vec2, expected: bool) -> None:
    assert vector.is_zero() is expected
