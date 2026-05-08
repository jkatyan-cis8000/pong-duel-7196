"""Pure utility functions for Pong game."""


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Constrain value within bounds."""
    return max(min_val, min(value, max_val))


def sign(value: float) -> int:
    """Returns the sign of a number: 1 for positive, -1 for negative, 0 for zero."""
    if value > 0:
        return 1
    elif value < 0:
        return -1
    return 0


def distance_squared(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """Calculate squared distance between two points (avoids sqrt for performance)."""
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
