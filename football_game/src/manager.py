"""Game state manager."""

from enum import Enum, auto
import time


class GameState(Enum):
    """Game state enumeration."""
    MENU = auto()
    PLAYING = auto()
    GOAL_CELEBRATION = auto()
    GAMEOVER = auto()


class GameStateManager:
    """Manages game states and transitions."""

    def __init__(self) -> None:
        """Initialize the state manager."""
        self.current_state = GameState.MENU
        self.previous_state = GameState.MENU

        # Score tracking
        self.ai_score = 0
        self.player_score = 0

        # Goal celebration timing
        self.celebration_start_time = 0.0
        self.celebration_duration = 2.0
        self.last_scorer = ''  # 'ai' or 'player'

        # Game settings
        self.winning_score = 5

    def change_state(self, new_state: GameState) -> None:
        """Change to a new game state.

        Args:
            new_state: The state to transition to
        """
        self.previous_state = self.current_state
        self.current_state = new_state

    def start_game(self) -> None:
        """Start a new game."""
        self.ai_score = 0
        self.player_score = 0
        self.last_scorer = ''
        self.change_state(GameState.PLAYING)

    def goal_scored(self, scorer: str) -> None:
        """Handle a goal being scored.

        Args:
            scorer: 'ai' or 'player'
        """
        if scorer == 'ai':
            self.ai_score += 1
        else:
            self.player_score += 1

        self.last_scorer = scorer
        self.celebration_start_time = time.time()
        self.change_state(GameState.GOAL_CELEBRATION)

    def update_celebration(self) -> bool:
        """Update celebration state.

        Returns:
            True if celebration is over
        """
        elapsed = time.time() - self.celebration_start_time
        if elapsed >= self.celebration_duration:
            # Check if game is over
            if self.ai_score >= self.winning_score or self.player_score >= self.winning_score:
                self.change_state(GameState.GAMEOVER)
            else:
                self.change_state(GameState.PLAYING)
            return True
        return False

    def get_celebration_progress(self) -> float:
        """Get celebration animation progress.

        Returns:
            Progress from 0.0 to 1.0
        """
        elapsed = time.time() - self.celebration_start_time
        return min(1.0, elapsed / self.celebration_duration)

    def get_winner(self) -> str:
        """Get the winner of the game.

        Returns:
            'ai' or 'player'
        """
        if self.ai_score >= self.winning_score:
            return 'ai'
        elif self.player_score >= self.winning_score:
            return 'player'
        return ''

    def return_to_menu(self) -> None:
        """Return to the main menu."""
        self.change_state(GameState.MENU)

    def is_playing(self) -> bool:
        """Check if game is in playing state.

        Returns:
            True if currently playing
        """
        return self.current_state == GameState.PLAYING

    def is_menu(self) -> bool:
        """Check if in menu state.

        Returns:
            True if in menu
        """
        return self.current_state == GameState.MENU

    def is_celebrating(self) -> bool:
        """Check if in goal celebration state.

        Returns:
            True if celebrating
        """
        return self.current_state == GameState.GOAL_CELEBRATION

    def is_game_over(self) -> bool:
        """Check if game is over.

        Returns:
            True if game over
        """
        return self.current_state == GameState.GAMEOVER
