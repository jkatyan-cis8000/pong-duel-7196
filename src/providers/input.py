"""Input provider for reading player movement commands."""

from typing import Literal

from src.types import Point


Input = Literal["up", "down", "none"]


def parse_input(key: str) -> Input:
    """Parse a raw key input into a movement command."""
    key = key.strip().lower()
    if key in ("w", "up", "k"):
        return "up"
    elif key in ("s", "down", "j"):
        return "down"
    return "none"
