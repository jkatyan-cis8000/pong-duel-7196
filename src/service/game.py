"""Game logic and collision detection for Pong."""

from src.config import (
    GAME_HEIGHT,
    GAME_WIDTH,
    INITIAL_BALL_SPEED,
    MAX_BALL_SPEED,
    PADDLE_MARGIN,
    PADDLE_WIDTH,
    SPEED_INCREMENT,
)
from src.types import Ball, GameState, Paddle, Player, Point, Velocity
from src.utils import clamp


def update_ball(ball: Ball, paddle1: Paddle, paddle2: Paddle) -> Ball:
    """
    Update ball position and detect collisions.
    
    Returns new ball state with updated position and velocity.
    """
    x, y = ball.position
    vx, vy = ball.velocity
    
    # Move ball
    new_x = x + vx
    new_y = y + vy
    
    # Top and bottom wall collisions
    if new_y <= 0:
        new_y = 0
        vy = -vy
    elif new_y >= GAME_HEIGHT - 1:
        new_y = GAME_HEIGHT - 1
        vy = -vy
    
    # Paddle collisions
    # Player 1 paddle (left)
    if (
        new_x <= paddle1.x + PADDLE_WIDTH
        and paddle1.y <= new_y <= paddle1.y + paddle1.height
    ):
        new_x = paddle1.x + PADDLE_WIDTH
        vx = abs(vx) + SPEED_INCREMENT if vx > 0 else vx
        vx = min(vx, MAX_BALL_SPEED)
        # Add spin based on where ball hit the paddle
        hit_pos = (new_y - (paddle1.y + paddle1.height / 2)) / (paddle1.height / 2)
        vy += hit_pos * 0.5
    
    # Player 2 paddle (right)
    if (
        new_x >= paddle2.x - PADDLE_WIDTH
        and paddle2.y <= new_y <= paddle2.y + paddle2.height
    ):
        new_x = paddle2.x - PADDLE_WIDTH
        vx = -abs(vx) - SPEED_INCREMENT if vx < 0 else vx
        vx = max(vx, -MAX_BALL_SPEED)
        # Add spin based on where ball hit the paddle
        hit_pos = (new_y - (paddle2.y + paddle2.height / 2)) / (paddle2.height / 2)
        vy += hit_pos * 0.5
    
    # Check if ball went out of bounds (scoring)
    if new_x < 0 or new_x > GAME_WIDTH:
        return None, vy  # Signal for scoring
    
    return Ball(Point((new_x, new_y)), Velocity((vx, vy))), None


def update_paddle(paddle: Paddle, move: str, height: float) -> Paddle:
    """Update paddle position based on movement command."""
    y = paddle.y
    if move == "up":
        y -= 1
    elif move == "down":
        y += 1
    
    # Clamp to game boundaries
    y = clamp(y, 0, GAME_HEIGHT - height)
    
    return Paddle(paddle.x, y, paddle.width, paddle.height)


def reset_ball() -> Ball:
    """Reset ball to center with initial velocity."""
    from src.types import Point, Velocity
    return Ball(
        Point((GAME_WIDTH / 2, GAME_HEIGHT / 2)),
        Velocity((INITIAL_BALL_SPEED, INITIAL_BALL_SPEED * 0.5))
    )


def check_game_over(player1_score: int, player2_score: int) -> str | None:
    """Check if game is over and who won."""
    from src.config import WINNING_SCORE
    if player1_score >= WINNING_SCORE:
        return "player1"
    elif player2_score >= WINNING_SCORE:
        return "player2"
    return None
