"""Types for Pong game."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import NewType

# Basic 2D types
Point = NewType("Point", tuple[float, float])
Velocity = NewType("Velocity", tuple[float, float])


@dataclass(frozen=True)
class Ball:
    """Represents the ball with position and velocity."""
    position: Point
    velocity: Velocity


@dataclass(frozen=True)
class Paddle:
    """Represents a paddle with position and dimensions."""
    x: float
    y: float
    width: float
    height: float


@dataclass(frozen=True)
class Player:
    """Represents a player with identifier and score."""
    id: int
    score: int


class GameStatus(Enum):
    """Current state of the game."""
    RUNNING = auto()
    PLAYER_1_WINS = auto()
    PLAYER_2_WINS = auto()


@dataclass(frozen=True)
class GameState:
    """Complete game state."""
    ball: Ball
    paddle1: Paddle
    paddle2: Paddle
    player1: Player
    player2: Player
    status: GameStatus
