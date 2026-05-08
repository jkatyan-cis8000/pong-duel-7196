"""Runtime component that runs the game loop."""

import sys
import time
import tty
import termios

from src.config import INPUT_UPDATE_MS
from src.providers.input import parse_input
from src.service.state import create_initial_state, update_game_state
from src.types import GameStatus
from src.ui.renderer import render_game


def get_key() -> str:
    """Get a single keypress from stdin without waiting for newline."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        ch = sys.stdin.read(1)
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


class GameLoop:
    """Main game loop that coordinates game state and rendering."""
    
    def __init__(self):
        self.state = create_initial_state()
        self.running = True
        self.last_update = time.time()
        self.buffer = ""
    
    def run(self) -> None:
        """Run the game loop until game over."""
        try:
            while self.running:
                self._process_frame()
        except KeyboardInterrupt:
            print("\nGame interrupted.")
    
    def _process_frame(self) -> None:
        """Process one frame of the game."""
        # Check for game over
        if self.state.status is not None:
            self._handle_game_over()
            return
        
        # Get input
        input1, input2 = self._get_input()
        
        # Update game state
        self.state, scoring_player = update_game_state(self.state, input1, input2)
        
        # Render
        self._render()
        
        # Wait for next frame
        self._wait_for_frame()
    
    def _get_input(self) -> tuple[str, str]:
        """Get input from both players."""
        input1 = "none"
        input2 = "none"
        
        # Read available input
        import select
        while select.select([sys.stdin], [], [], 0)[0]:
            key = get_key()
            self.buffer += key
        
        # Parse buffered input - alternate between players
        # Player 1 uses W/S, Player 2 uses up/down arrow keys or other
        if len(self.buffer) >= 2:
            # Both players have made moves
            input1 = parse_input(self.buffer[0])
            input2 = parse_input(self.buffer[1])
            self.buffer = ""
        elif len(self.buffer) == 1:
            # Only one player has moved - use for both for now
            input1 = parse_input(self.buffer[0])
            input2 = input1  # Same for now
            self.buffer = ""
        
        return input1, input2
    
    def _wait_for_frame(self) -> None:
        """Wait until next frame update."""
        now = time.time()
        elapsed = (now - self.last_update) * 1000
        wait_time = INPUT_UPDATE_MS - elapsed
        if wait_time > 0:
            time.sleep(wait_time / 1000)
        self.last_update = time.time()
    
    def _render(self) -> None:
        """Render current game state."""
        import os
        os.system("clear" if os.name == "posix" else "cls")
        print(render_game(self.state))
        print("\nControls: W/S for paddle movement")
    
    def _handle_game_over(self) -> None:
        """Handle game over state."""
        winner = (
            "Player 1" if self.state.status == GameStatus.PLAYER_1_WINS else "Player 2"
        )
        import os
        os.system("clear" if os.name == "posix" else "cls")
        print(render_game(self.state))
        print(f"\n{winner} wins!")
        print("Press Ctrl+C to exit.")
