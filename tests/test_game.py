"""Unit tests for Pong game types and logic."""

from src.types import Ball, Paddle, Player, GameState, GameStatus, Point, Velocity
from src.config import GAME_WIDTH, GAME_HEIGHT, PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_MARGIN
from src.service.state import create_initial_state, update_game_state
from src.providers.input import parse_input


def test_initial_state():
    """Test initial game state creation."""
    state = create_initial_state()
    
    # Ball starts at center
    assert state.ball.position == Point((GAME_WIDTH / 2, GAME_HEIGHT / 2))
    
    # Paddles are centered vertically
    expected_y = (GAME_HEIGHT - PADDLE_HEIGHT) / 2
    assert state.paddle1.y == expected_y
    assert state.paddle2.y == expected_y
    
    # Paddles are at margins (using PADDLE_MARGIN from config)
    assert state.paddle1.x == PADDLE_MARGIN
    assert state.paddle2.x == GAME_WIDTH - PADDLE_MARGIN - PADDLE_WIDTH
    
    # Scores are zero
    assert state.player1.score == 0
    assert state.player2.score == 0
    
    # Game is running (status None means running, not set yet)
    assert state.status is None


def test_paddle_movement():
    """Test paddle movement updates."""
    state = create_initial_state()
    
    # Player 1 moves up
    state, _ = update_game_state(state, "up", "none")
    assert state.paddle1.y < (GAME_HEIGHT - PADDLE_HEIGHT) / 2
    
    # Player 2 moves down
    state, _ = update_game_state(state, "none", "down")
    assert state.paddle2.y > (GAME_HEIGHT - PADDLE_HEIGHT) / 2


def test_ball_movement():
    """Test ball moves forward."""
    state = create_initial_state()
    
    # Ball should move to the right initially
    initial_x = state.ball.position[0]
    for _ in range(5):
        state, _ = update_game_state(state, "none", "none")
    
    assert state.ball.position[0] > initial_x


def test_input_parsing():
    """Test input parsing function."""
    assert parse_input("w") == "up"
    assert parse_input("s") == "down"
    assert parse_input("x") == "none"
    assert parse_input("") == "none"


def test_scoring():
    """Test scoring when ball passes paddle."""
    state = create_initial_state()
    
    # Move ball to left side
    state_data = state
    for _ in range(100):
        state_data, scoring = update_game_state(state_data, "none", "none")
        if scoring:
            assert state_data.player2.score == 1
            assert state_data.player1.score == 0
            break
    
    # Ball should reset after scoring
    assert state_data.ball.position[0] == GAME_WIDTH / 2


def test_game_status():
    """Test game status updates."""
    state = create_initial_state()
    
    # Game status is None initially (not yet running)
    assert state.status is None
