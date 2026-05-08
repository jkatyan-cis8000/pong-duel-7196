"""Game state management and orchestration."""

from src.config import GAME_HEIGHT, GAME_WIDTH, INITIAL_BALL_SPEED, PADDLE_HEIGHT, PADDLE_MARGIN
from src.providers.input import parse_input
from src.service.game import reset_ball, update_paddle, check_game_over
from src.types import Ball, GameState, Paddle, Player, Point, Velocity


def create_initial_state() -> GameState:
    """Create the initial game state."""
    paddle1 = Paddle(PADDLE_MARGIN, GAME_HEIGHT / 2 - PADDLE_HEIGHT / 2, 2, PADDLE_HEIGHT)
    paddle2 = Paddle(GAME_WIDTH - PADDLE_MARGIN - 2, GAME_HEIGHT / 2 - PADDLE_HEIGHT / 2, 2, PADDLE_HEIGHT)
    
    return GameState(
        ball=reset_ball(),
        paddle1=paddle1,
        paddle2=paddle2,
        player1=Player(1, 0),
        player2=Player(2, 0),
        status=None  # Will be set after first score
    )


def update_game_state(
    state: GameState, input1: str, input2: str
) -> tuple[GameState, str | None]:
    """
    Update game state based on player inputs.
    
    Returns new game state and any scoring event ("player1", "player2", or None).
    """
    from src.service.game import update_ball
    
    # Update paddles
    new_paddle1 = update_paddle(state.paddle1, input1, state.paddle1.height)
    new_paddle2 = update_paddle(state.paddle2, input2, state.paddle2.height)
    
    # Update ball
    result = update_ball(state.ball, new_paddle1, new_paddle2)
    
    if result is None:
        # Ball went out - scoring event
        return state, None
    
    new_ball, score_direction = result
    
    # Check for scoring
    if new_ball.position[0] < 0:
        # Player 2 scores
        new_player2 = Player(2, state.player2.score + 1)
        new_ball = reset_ball()
        winner = check_game_over(state.player1.score, new_player2.score)
        if winner:
            from src.types import GameStatus
            return GameState(
                ball=new_ball,
                paddle1=new_paddle1,
                paddle2=new_paddle2,
                player1=state.player1,
                player2=new_player2,
                status=GameStatus.PLAYER_2_WINS,
            ), "player2"
        return GameState(
            ball=new_ball,
            paddle1=new_paddle1,
            paddle2=new_paddle2,
            player1=state.player1,
            player2=new_player2,
            status=None,
        ), "player2"
    
    if new_ball.position[0] > GAME_WIDTH:
        # Player 1 scores
        new_player1 = Player(1, state.player1.score + 1)
        new_ball = reset_ball()
        winner = check_game_over(new_player1.score, state.player2.score)
        if winner:
            from src.types import GameStatus
            return GameState(
                ball=new_ball,
                paddle1=new_paddle1,
                paddle2=new_paddle2,
                player1=new_player1,
                player2=state.player2,
                status=GameStatus.PLAYER_1_WINS,
            ), "player1"
        return GameState(
            ball=new_ball,
            paddle1=new_paddle1,
            paddle2=new_paddle2,
            player1=new_player1,
            player2=state.player2,
            status=None,
        ), "player1"
    
    return GameState(
        ball=new_ball,
        paddle1=new_paddle1,
        paddle2=new_paddle2,
        player1=state.player1,
        player2=state.player2,
        status=None,
    ), None
