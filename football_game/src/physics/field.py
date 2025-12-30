"""Field boundaries and goal detection."""

import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FIELD_MARGIN,
    GOAL_WIDTH, GOAL_DEPTH, BALL_BOUNCE_FACTOR
)


class FieldBounds:
    """Manages field boundaries and goal areas."""

    def __init__(self) -> None:
        """Initialize field boundaries."""
        self.left = FIELD_MARGIN
        self.right = SCREEN_WIDTH - FIELD_MARGIN
        self.top = FIELD_MARGIN
        self.bottom = SCREEN_HEIGHT - FIELD_MARGIN

        # Goal positions (centered on each side)
        goal_center_y = SCREEN_HEIGHT // 2
        self.goal_top = goal_center_y - GOAL_WIDTH // 2
        self.goal_bottom = goal_center_y + GOAL_WIDTH // 2

        # Left goal (Player 1 / AI goal)
        self.left_goal_rect = pygame.Rect(
            0, self.goal_top,
            FIELD_MARGIN + GOAL_DEPTH, GOAL_WIDTH
        )

        # Right goal (Player 2 / Human goal)
        self.right_goal_rect = pygame.Rect(
            SCREEN_WIDTH - FIELD_MARGIN - GOAL_DEPTH, self.goal_top,
            FIELD_MARGIN + GOAL_DEPTH, GOAL_WIDTH
        )

    def check_ball_bounds(self, pos: pygame.Vector2, vel: pygame.Vector2,
                          radius: float) -> tuple[pygame.Vector2, pygame.Vector2, int]:
        """Check if ball is within field bounds and handle bouncing.

        Args:
            pos: Ball position
            vel: Ball velocity
            radius: Ball radius

        Returns:
            Tuple of (new_position, new_velocity, goal_scored)
            goal_scored: 0 = no goal, 1 = left goal (point for right), 2 = right goal (point for left)
        """
        new_pos = pygame.Vector2(pos)
        new_vel = pygame.Vector2(vel)
        goal_scored = 0

        # Check for goals
        ball_rect = pygame.Rect(pos.x - radius, pos.y - radius, radius * 2, radius * 2)

        if self.left_goal_rect.collidepoint(pos.x, pos.y):
            if self.goal_top < pos.y < self.goal_bottom:
                goal_scored = 1  # Point for right player (human)
                return new_pos, new_vel, goal_scored

        if self.right_goal_rect.collidepoint(pos.x, pos.y):
            if self.goal_top < pos.y < self.goal_bottom:
                goal_scored = 2  # Point for left player (AI)
                return new_pos, new_vel, goal_scored

        # Check horizontal bounds (with goal openings)
        if new_pos.x - radius < self.left:
            # Check if in goal area
            if not (self.goal_top < new_pos.y < self.goal_bottom):
                new_pos.x = self.left + radius
                new_vel.x = -new_vel.x * BALL_BOUNCE_FACTOR

        if new_pos.x + radius > self.right:
            # Check if in goal area
            if not (self.goal_top < new_pos.y < self.goal_bottom):
                new_pos.x = self.right - radius
                new_vel.x = -new_vel.x * BALL_BOUNCE_FACTOR

        # Check vertical bounds
        if new_pos.y - radius < self.top:
            new_pos.y = self.top + radius
            new_vel.y = -new_vel.y * BALL_BOUNCE_FACTOR

        if new_pos.y + radius > self.bottom:
            new_pos.y = self.bottom - radius
            new_vel.y = -new_vel.y * BALL_BOUNCE_FACTOR

        return new_pos, new_vel, goal_scored

    def check_player_bounds(self, pos: pygame.Vector2, radius: float) -> pygame.Vector2:
        """Keep player within field bounds.

        Args:
            pos: Player position
            radius: Player radius

        Returns:
            Constrained position
        """
        new_pos = pygame.Vector2(pos)

        new_pos.x = max(self.left + radius, min(self.right - radius, new_pos.x))
        new_pos.y = max(self.top + radius, min(self.bottom - radius, new_pos.y))

        return new_pos

    def get_field_center(self) -> pygame.Vector2:
        """Get the center of the field.

        Returns:
            Center position as Vector2
        """
        return pygame.Vector2(
            (self.left + self.right) / 2,
            (self.top + self.bottom) / 2
        )

    def is_ball_on_left_side(self, pos: pygame.Vector2) -> bool:
        """Check if ball is on the left side of the field.

        Args:
            pos: Ball position

        Returns:
            True if ball is on left side
        """
        center_x = (self.left + self.right) / 2
        return pos.x < center_x
