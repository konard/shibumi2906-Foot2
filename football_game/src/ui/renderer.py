"""Game renderer for drawing field, entities, and HUD."""

import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FIELD_MARGIN,
    GREEN, DARK_GREEN, WHITE, CENTER_CIRCLE_RADIUS,
    GOAL_WIDTH
)


class GameRenderer:
    """Handles all game rendering."""

    def __init__(self, screen: pygame.Surface) -> None:
        """Initialize the renderer.

        Args:
            screen: Pygame surface to render on
        """
        self.screen = screen
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)

    def draw_field(self) -> None:
        """Draw the football field."""
        # Fill background with green
        self.screen.fill(GREEN)

        # Field boundaries
        field_rect = pygame.Rect(
            FIELD_MARGIN, FIELD_MARGIN,
            SCREEN_WIDTH - 2 * FIELD_MARGIN,
            SCREEN_HEIGHT - 2 * FIELD_MARGIN
        )
        pygame.draw.rect(self.screen, DARK_GREEN, field_rect, 3)

        # Center line
        center_x = SCREEN_WIDTH // 2
        pygame.draw.line(
            self.screen, DARK_GREEN,
            (center_x, FIELD_MARGIN),
            (center_x, SCREEN_HEIGHT - FIELD_MARGIN),
            3
        )

        # Center circle
        center_y = SCREEN_HEIGHT // 2
        pygame.draw.circle(
            self.screen, DARK_GREEN,
            (center_x, center_y),
            CENTER_CIRCLE_RADIUS, 3
        )

        # Center dot
        pygame.draw.circle(
            self.screen, DARK_GREEN,
            (center_x, center_y),
            5
        )

        # Goal areas (penalty areas)
        goal_area_width = 100
        goal_area_height = GOAL_WIDTH + 60

        # Left goal area
        left_goal_area = pygame.Rect(
            FIELD_MARGIN,
            center_y - goal_area_height // 2,
            goal_area_width,
            goal_area_height
        )
        pygame.draw.rect(self.screen, DARK_GREEN, left_goal_area, 3)

        # Right goal area
        right_goal_area = pygame.Rect(
            SCREEN_WIDTH - FIELD_MARGIN - goal_area_width,
            center_y - goal_area_height // 2,
            goal_area_width,
            goal_area_height
        )
        pygame.draw.rect(self.screen, DARK_GREEN, right_goal_area, 3)

    def draw_score(self, ai_score: int, player_score: int) -> None:
        """Draw the score display.

        Args:
            ai_score: AI's current score
            player_score: Human player's current score
        """
        # Score background
        score_bg = pygame.Rect(SCREEN_WIDTH // 2 - 80, 5, 160, 35)
        pygame.draw.rect(self.screen, (0, 0, 0, 128), score_bg)
        pygame.draw.rect(self.screen, WHITE, score_bg, 2)

        # Score text
        score_text = f"{ai_score}  -  {player_score}"
        text_surface = self.font_medium.render(score_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 22))
        self.screen.blit(text_surface, text_rect)

        # Team labels
        ai_label = self.font_small.render("AI", True, (220, 20, 60))
        player_label = self.font_small.render("YOU", True, (30, 144, 255))
        self.screen.blit(ai_label, (SCREEN_WIDTH // 2 - 120, 10))
        self.screen.blit(player_label, (SCREEN_WIDTH // 2 + 85, 10))

    def draw_goal_text(self, scorer: str, alpha: int = 255) -> None:
        """Draw goal celebration text.

        Args:
            scorer: Who scored ('ai' or 'player')
            alpha: Text transparency (0-255)
        """
        if scorer == 'player':
            text = "GOAL!"
            color = (30, 144, 255)
        else:
            text = "GOAL!"
            color = (220, 20, 60)

        # Create text surface with alpha
        text_surface = self.font_large.render(text, True, color)
        text_surface.set_alpha(alpha)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)

    def draw_game_over(self, winner: str, ai_score: int, player_score: int) -> None:
        """Draw game over screen.

        Args:
            winner: Who won ('ai' or 'player')
            ai_score: Final AI score
            player_score: Final player score
        """
        # Darken the background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))

        # Game Over text
        game_over_text = self.font_large.render("GAME OVER", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(game_over_text, game_over_rect)

        # Winner text
        if winner == 'player':
            winner_text = "YOU WIN!"
            color = (30, 144, 255)
        else:
            winner_text = "AI WINS!"
            color = (220, 20, 60)

        winner_surface = self.font_large.render(winner_text, True, color)
        winner_rect = winner_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(winner_surface, winner_rect)

        # Final score
        score_text = f"Final Score: {ai_score} - {player_score}"
        score_surface = self.font_medium.render(score_text, True, WHITE)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(score_surface, score_rect)

        # Restart instruction
        restart_text = "Press SPACE or ENTER to restart"
        restart_surface = self.font_small.render(restart_text, True, WHITE)
        restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
        self.screen.blit(restart_surface, restart_rect)

    def draw_controls_hint(self) -> None:
        """Draw controls hint at the bottom of the screen."""
        hint_text = "WASD/Arrows: Move | SPACE: Kick | ESC: Menu"
        hint_surface = self.font_small.render(hint_text, True, (200, 200, 200))
        hint_rect = hint_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 15))
        self.screen.blit(hint_surface, hint_rect)
