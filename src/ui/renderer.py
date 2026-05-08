"""UI renderer for terminal-based Pong display."""

from src.config import GAME_WIDTH, GAME_HEIGHT, PADDLE_HEIGHT, BALL_SIZE
from src.types import Ball, GameState, GameStatus, Paddle, Player


def render_game(state: GameState) -> str:
    """Render the current game state as ASCII art."""
    # Create empty canvas
    canvas = [[" " for _ in range(GAME_WIDTH)] for _ in range(GAME_HEIGHT)]
    
    # Render border
    for x in range(GAME_WIDTH):
        canvas[0][x] = "-"
        canvas[GAME_HEIGHT - 1][x] = "-"
    for y in range(GAME_HEIGHT):
        canvas[y][0] = "|"
        canvas[y][GAME_WIDTH - 1] = "|"
    canvas[0][0] = "+"
    canvas[0][GAME_WIDTH - 1] = "+"
    canvas[GAME_HEIGHT - 1][0] = "+"
    canvas[GAME_HEIGHT - 1][GAME_WIDTH - 1] = "+"
    
    # Render center line
    center_x = GAME_WIDTH // 2
    for y in range(1, GAME_HEIGHT - 1, 2):
        canvas[y][center_x] = "."
    
    # Render score
    score_left = f"P1: {state.player1.score}"
    score_right = f"P2: {state.player2.score}"
    for i, ch in enumerate(score_left):
        if 1 + i < GAME_WIDTH - 1:
            canvas[1][1 + i] = ch
    for i, ch in enumerate(score_right):
        if GAME_WIDTH - 2 - i > 0:
            canvas[1][GAME_WIDTH - 2 - i] = ch
    
    # Render paddles
    render_paddle(canvas, state.paddle1, "#")
    render_paddle(canvas, state.paddle2, "#")
    
    # Render ball
    render_ball(canvas, state.ball)
    
    # Convert to string
    lines = []
    for row in canvas:
        lines.append("".join(row))
    
    # Add status if game over
    if state.status is not None:
        lines.append("")
        if state.status == GameStatus.PLAYER_1_WINS:
            lines.append("PLAYER 1 WINS!")
        else:
            lines.append("PLAYER 2 WINS!")
        lines.append("Press Ctrl+C to exit.")
    
    return "\n".join(lines)


def render_paddle(canvas: list[list[str]], paddle: Paddle, char: str) -> None:
    """Render a paddle on the canvas."""
    y = paddle.y
    height = paddle.height
    
    for i in range(int(height)):
        py = int(y + i)
        if 0 <= py < GAME_HEIGHT:
            px = int(paddle.x)
            if 0 <= px < GAME_WIDTH:
                canvas[py][px] = char


def render_ball(canvas: list[list[str]], ball: Ball) -> None:
    """Render the ball on the canvas."""
    x, y = ball.position
    bx, by = int(x), int(y)
    
    if 0 <= bx < GAME_WIDTH and 0 <= by < GAME_HEIGHT:
        canvas[by][bx] = "O"


def get_status_message(status: GameStatus | None) -> str:
    """Get the status message for the current game state."""
    if status is None:
        return ""
    if status.name == "PLAYER_1_WINS":
        return "PLAYER 1 WINS!"
    if status.name == "PLAYER_2_WINS":
        return "PLAYER 2 WINS!"
    return ""
