"""Player entity class."""

import pygame
from settings import (
    PLAYER_RADIUS, PLAYER_ACCEL, PLAYER_MAX_SPEED,
    PLAYER_DAMPING, KICK_RADIUS, KICK_POWER, BLUE, RED
)


class Player:
    """Represents a player (human or AI controlled)."""

    def __init__(self, pos: pygame.Vector2, color: tuple[int, int, int],
                 is_ai: bool = False) -> None:
        """Initialize the player.

        Args:
            pos: Starting position
            color: Player color (RGB tuple)
            is_ai: Whether this player is controlled by AI
        """
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(0, 0)
        self.color = color
        self.radius = PLAYER_RADIUS
        self.accel = PLAYER_ACCEL
        self.max_speed = PLAYER_MAX_SPEED
        self.damping = PLAYER_DAMPING
        self.kick_radius = KICK_RADIUS
        self.kick_power = KICK_POWER
        self.is_ai = is_ai
        self.mass = 1.0

    def apply_input(self, direction: pygame.Vector2) -> None:
        """Apply movement input to the player.

        Args:
            direction: Normalized direction vector for movement
        """
        if direction.length() > 0:
            direction = direction.normalize()
            self.vel += direction * self.accel

            # Limit to max speed
            if self.vel.length() > self.max_speed:
                self.vel = self.vel.normalize() * self.max_speed

    def update(self) -> None:
        """Update player position and apply damping."""
        # Apply velocity
        self.pos += self.vel

        # Apply damping (friction)
        self.vel *= self.damping

        # Stop completely if very slow
        if self.vel.length() < 0.1:
            self.vel = pygame.Vector2(0, 0)

    def can_kick(self, ball_pos: pygame.Vector2) -> bool:
        """Check if the player can kick the ball.

        Args:
            ball_pos: Position of the ball

        Returns:
            True if ball is within kicking range
        """
        distance = self.pos.distance_to(ball_pos)
        return distance < self.kick_radius

    def kick_ball(self, ball_pos: pygame.Vector2) -> pygame.Vector2:
        """Calculate kick impulse for the ball.

        Args:
            ball_pos: Position of the ball

        Returns:
            Impulse vector to apply to the ball
        """
        if not self.can_kick(ball_pos):
            return pygame.Vector2(0, 0)

        # Calculate direction from player to ball
        direction = (ball_pos - self.pos)
        if direction.length() > 0:
            direction = direction.normalize()
        else:
            # Ball is exactly on player, kick forward
            direction = pygame.Vector2(1, 0)

        return direction * self.kick_power

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the player on the screen.

        Args:
            screen: Pygame surface to draw on
        """
        # Draw player circle
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

        # Draw outline
        pygame.draw.circle(screen, (0, 0, 0), (int(self.pos.x), int(self.pos.y)), self.radius, 2)

        # Draw direction indicator (small circle in front)
        if self.vel.length() > 0.5:
            indicator_pos = self.pos + self.vel.normalize() * (self.radius - 5)
            pygame.draw.circle(screen, (255, 255, 255),
                             (int(indicator_pos.x), int(indicator_pos.y)), 5)
