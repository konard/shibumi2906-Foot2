"""Menu system for the game."""

import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GREEN, BLACK


class Menu:
    """Main menu for the game."""

    def __init__(self, screen: pygame.Surface) -> None:
        """Initialize the menu.

        Args:
            screen: Pygame surface to render on
        """
        self.screen = screen
        self.font_title = pygame.font.Font(None, 96)
        self.font_option = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)

        self.options = ["Play Game", "Quit"]
        self.selected = 0

    def handle_input(self, event: pygame.event.Event) -> str | None:
        """Handle menu input.

        Args:
            event: Pygame event

        Returns:
            Action to take: 'play', 'quit', or None
        """
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.selected == 0:
                    return 'play'
                elif self.selected == 1:
                    return 'quit'

        return None

    def draw(self) -> None:
        """Draw the menu."""
        # Background
        self.screen.fill(GREEN)

        # Draw a simple field pattern in background
        for x in range(0, SCREEN_WIDTH, 50):
            pygame.draw.line(self.screen, (30, 120, 30),
                           (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 50):
            pygame.draw.line(self.screen, (30, 120, 30),
                           (0, y), (SCREEN_WIDTH, y), 1)

        # Title background
        title_bg = pygame.Rect(SCREEN_WIDTH // 2 - 250, 100, 500, 100)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), title_bg)
        pygame.draw.rect(self.screen, WHITE, title_bg, 3)

        # Title
        title_text = self.font_title.render("FOOTBALL", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)

        # Subtitle
        subtitle_text = self.font_small.render("Top-Down Football Game", True, (200, 200, 200))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(subtitle_text, subtitle_rect)

        # Menu options
        for i, option in enumerate(self.options):
            if i == self.selected:
                color = (255, 255, 0)  # Yellow for selected
                prefix = "> "
                suffix = " <"
            else:
                color = WHITE
                prefix = "  "
                suffix = "  "

            text = prefix + option + suffix
            option_surface = self.font_option.render(text, True, color)
            option_rect = option_surface.get_rect(
                center=(SCREEN_WIDTH // 2, 320 + i * 60)
            )

            # Draw selection background
            if i == self.selected:
                bg_rect = pygame.Rect(
                    option_rect.left - 20, option_rect.top - 5,
                    option_rect.width + 40, option_rect.height + 10
                )
                pygame.draw.rect(self.screen, (50, 50, 50), bg_rect)
                pygame.draw.rect(self.screen, (255, 255, 0), bg_rect, 2)

            self.screen.blit(option_surface, option_rect)

        # Controls info
        controls_text = [
            "Controls:",
            "WASD or Arrow Keys - Move",
            "SPACE - Kick",
            "ESC - Pause / Menu"
        ]

        y_offset = SCREEN_HEIGHT - 140
        for line in controls_text:
            line_surface = self.font_small.render(line, True, (180, 180, 180))
            line_rect = line_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(line_surface, line_rect)
            y_offset += 30

        # Version/credit
        credit_text = self.font_small.render("Python + pygame-ce", True, (100, 100, 100))
        credit_rect = credit_text.get_rect(bottomright=(SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10))
        self.screen.blit(credit_text, credit_rect)
