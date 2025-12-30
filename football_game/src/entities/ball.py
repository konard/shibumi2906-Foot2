"""Ball entity class."""

import pygame
from settings import BALL_RADIUS, BALL_MAX_SPEED, BALL_DAMPING, YELLOW


class Ball:
    """Represents the football/soccer ball."""

    def __init__(self, pos: pygame.Vector2) -> None:
        """Initialize the ball.

        Args:
            pos: Starting position
        """
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(0, 0)
        self.radius = BALL_RADIUS
        self.max_speed = BALL_MAX_SPEED
        self.damping = BALL_DAMPING
        self.color = YELLOW
        self.mass = 0.3  # Lighter than player

    def apply_impulse(self, impulse: pygame.Vector2) -> None:
        """Apply an impulse to the ball.

        Args:
            impulse: Impulse vector to apply
        """
        self.vel += impulse

        # Limit to max speed
        if self.vel.length() > self.max_speed:
            self.vel = self.vel.normalize() * self.max_speed

    def update(self) -> None:
        """Update ball position and apply damping."""
        # Apply velocity
        self.pos += self.vel

        # Apply damping (friction)
        self.vel *= self.damping

        # Stop completely if very slow
        if self.vel.length() < 0.05:
            self.vel = pygame.Vector2(0, 0)

    def reset(self, pos: pygame.Vector2) -> None:
        """Reset ball to a position with zero velocity.

        Args:
            pos: New position for the ball
        """
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(0, 0)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the ball on the screen.

        Args:
            screen: Pygame surface to draw on
        """
        # Draw ball
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

        # Draw outline
        pygame.draw.circle(screen, (0, 0, 0), (int(self.pos.x), int(self.pos.y)), self.radius, 2)

        # Draw a pattern on the ball (pentagon pattern suggestion)
        pattern_radius = self.radius // 2
        pygame.draw.circle(screen, (200, 200, 0),
                          (int(self.pos.x), int(self.pos.y)), pattern_radius)
