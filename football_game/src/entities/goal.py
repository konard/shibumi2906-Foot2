"""Goal entity class."""

import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FIELD_MARGIN,
    GOAL_WIDTH, GOAL_DEPTH, WHITE, GRAY
)


class Goal:
    """Represents a goal area."""

    def __init__(self, side: str) -> None:
        """Initialize the goal.

        Args:
            side: 'left' or 'right' indicating which side of the field
        """
        self.side = side
        goal_center_y = SCREEN_HEIGHT // 2

        if side == 'left':
            self.x = FIELD_MARGIN - GOAL_DEPTH
            self.post_color = GRAY
        else:  # right
            self.x = SCREEN_WIDTH - FIELD_MARGIN
            self.post_color = GRAY

        self.y = goal_center_y - GOAL_WIDTH // 2
        self.width = GOAL_DEPTH
        self.height = GOAL_WIDTH

        # Goal rectangle
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Net area (inside the goal)
        if side == 'left':
            self.net_rect = pygame.Rect(0, self.y, FIELD_MARGIN, self.height)
        else:
            self.net_rect = pygame.Rect(
                SCREEN_WIDTH - FIELD_MARGIN, self.y,
                FIELD_MARGIN, self.height
            )

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the goal on the screen.

        Args:
            screen: Pygame surface to draw on
        """
        # Draw net background
        pygame.draw.rect(screen, (220, 220, 220), self.net_rect)

        # Draw net pattern
        net_spacing = 10
        if self.side == 'left':
            for x in range(0, FIELD_MARGIN, net_spacing):
                pygame.draw.line(screen, GRAY,
                               (x, self.y), (x, self.y + self.height), 1)
            for y in range(int(self.y), int(self.y + self.height), net_spacing):
                pygame.draw.line(screen, GRAY,
                               (0, y), (FIELD_MARGIN, y), 1)
        else:
            start_x = SCREEN_WIDTH - FIELD_MARGIN
            for x in range(start_x, SCREEN_WIDTH, net_spacing):
                pygame.draw.line(screen, GRAY,
                               (x, self.y), (x, self.y + self.height), 1)
            for y in range(int(self.y), int(self.y + self.height), net_spacing):
                pygame.draw.line(screen, GRAY,
                               (start_x, y), (SCREEN_WIDTH, y), 1)

        # Draw goal posts
        post_width = 6
        if self.side == 'left':
            # Top post
            pygame.draw.rect(screen, WHITE,
                           (FIELD_MARGIN - post_width, self.y - post_width,
                            post_width, post_width))
            # Bottom post
            pygame.draw.rect(screen, WHITE,
                           (FIELD_MARGIN - post_width, self.y + self.height,
                            post_width, post_width))
            # Crossbar
            pygame.draw.line(screen, WHITE,
                           (FIELD_MARGIN - post_width, self.y),
                           (FIELD_MARGIN - post_width, self.y + self.height), post_width)
        else:
            # Top post
            pygame.draw.rect(screen, WHITE,
                           (SCREEN_WIDTH - FIELD_MARGIN, self.y - post_width,
                            post_width, post_width))
            # Bottom post
            pygame.draw.rect(screen, WHITE,
                           (SCREEN_WIDTH - FIELD_MARGIN, self.y + self.height,
                            post_width, post_width))
            # Crossbar
            pygame.draw.line(screen, WHITE,
                           (SCREEN_WIDTH - FIELD_MARGIN, self.y),
                           (SCREEN_WIDTH - FIELD_MARGIN, self.y + self.height), post_width)
