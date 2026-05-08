"""Main entry point for Pong game."""

from src.runtime.game_loop import GameLoop


def main() -> None:
    """Start the Pong game."""
    game = GameLoop()
    game.run()


if __name__ == "__main__":
    main()
