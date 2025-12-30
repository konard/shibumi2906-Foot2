"""AI Bot with Finite State Machine (FSM)."""

from enum import Enum, auto
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FIELD_MARGIN,
    GOAL_WIDTH, AI_ACCEL, AI_KICK_DISTANCE
)


class AIState(Enum):
    """AI behavior states."""
    ATTACK = auto()    # Ball on AI's side - move to ball and kick toward player's goal
    DEFENSE = auto()   # Ball on player's side - position between ball and own goal
    RETREAT = auto()   # Ball behind AI - circle around to avoid own goal


class AIBot:
    """AI controller for computer-controlled player."""

    def __init__(self, player_ref, field_bounds) -> None:
        """Initialize the AI bot.

        Args:
            player_ref: Reference to the Player entity this AI controls
            field_bounds: Reference to FieldBounds for field information
        """
        self.player = player_ref
        self.field = field_bounds
        self.state = AIState.DEFENSE
        self.target_pos = pygame.Vector2(0, 0)

        # AI's goal is on the left side
        self.own_goal_x = FIELD_MARGIN
        self.own_goal_center = pygame.Vector2(FIELD_MARGIN, SCREEN_HEIGHT // 2)

        # Target goal (player's goal) is on the right side
        self.target_goal_center = pygame.Vector2(SCREEN_WIDTH - FIELD_MARGIN, SCREEN_HEIGHT // 2)

        # Field center for determining sides
        self.field_center_x = SCREEN_WIDTH // 2

    def update_state(self, ball_pos: pygame.Vector2) -> None:
        """Update AI state based on ball position.

        Args:
            ball_pos: Current position of the ball
        """
        # Determine which side the ball is on
        ball_on_ai_side = ball_pos.x < self.field_center_x

        # Check if ball is behind the AI (closer to AI's goal than AI is)
        ball_behind_ai = ball_pos.x < self.player.pos.x - 30

        if ball_behind_ai and ball_on_ai_side:
            self.state = AIState.RETREAT
        elif ball_on_ai_side:
            self.state = AIState.ATTACK
        else:
            self.state = AIState.DEFENSE

    def calculate_target(self, ball_pos: pygame.Vector2) -> pygame.Vector2:
        """Calculate target position based on current state.

        Args:
            ball_pos: Current position of the ball

        Returns:
            Target position for the AI to move toward
        """
        if self.state == AIState.ATTACK:
            # Move toward the ball to kick it
            return self._get_attack_position(ball_pos)
        elif self.state == AIState.DEFENSE:
            # Position between ball and own goal
            return self._get_defense_position(ball_pos)
        else:  # RETREAT
            # Circle around the ball to avoid own goal
            return self._get_retreat_position(ball_pos)

    def _get_attack_position(self, ball_pos: pygame.Vector2) -> pygame.Vector2:
        """Get position for attacking (moving toward ball).

        The AI positions itself to kick the ball toward the player's goal.

        Args:
            ball_pos: Current ball position

        Returns:
            Target position
        """
        # Position behind the ball relative to target goal
        direction_to_target = (self.target_goal_center - ball_pos)
        if direction_to_target.length() > 0:
            direction_to_target = direction_to_target.normalize()
        else:
            direction_to_target = pygame.Vector2(1, 0)

        # Stand behind the ball to kick it toward the goal
        offset_distance = AI_KICK_DISTANCE
        target = ball_pos - direction_to_target * offset_distance

        return target

    def _get_defense_position(self, ball_pos: pygame.Vector2) -> pygame.Vector2:
        """Get defensive position between ball and own goal.

        Args:
            ball_pos: Current ball position

        Returns:
            Target position
        """
        # Calculate position on line between ball and own goal center
        direction = (ball_pos - self.own_goal_center)
        if direction.length() > 0:
            direction = direction.normalize()
        else:
            direction = pygame.Vector2(1, 0)

        # Stay about 1/3 of the way from goal to ball
        distance_to_ball = self.own_goal_center.distance_to(ball_pos)
        defense_distance = min(distance_to_ball * 0.4, 200)

        target = self.own_goal_center + direction * defense_distance

        # Clamp to reasonable field position
        target.x = max(FIELD_MARGIN + 50, min(self.field_center_x - 50, target.x))
        target.y = max(FIELD_MARGIN + 30, min(SCREEN_HEIGHT - FIELD_MARGIN - 30, target.y))

        return target

    def _get_retreat_position(self, ball_pos: pygame.Vector2) -> pygame.Vector2:
        """Get retreat position to circle around ball avoiding own goal.

        Args:
            ball_pos: Current ball position

        Returns:
            Target position
        """
        # Determine if we should go above or below the ball
        if self.player.pos.y < ball_pos.y:
            # AI is above the ball, go further up and around
            arc_offset = pygame.Vector2(50, -80)
        else:
            # AI is below the ball, go further down and around
            arc_offset = pygame.Vector2(50, 80)

        # Target position is to the side and slightly in front of the ball
        target = ball_pos + arc_offset

        # Clamp to field bounds
        target.x = max(FIELD_MARGIN + 30, min(SCREEN_WIDTH - FIELD_MARGIN - 30, target.x))
        target.y = max(FIELD_MARGIN + 30, min(SCREEN_HEIGHT - FIELD_MARGIN - 30, target.y))

        return target

    def get_movement_direction(self, ball_pos: pygame.Vector2) -> pygame.Vector2:
        """Get the direction the AI should move.

        Args:
            ball_pos: Current ball position

        Returns:
            Normalized direction vector for movement
        """
        # Update state based on ball position
        self.update_state(ball_pos)

        # Calculate target position
        self.target_pos = self.calculate_target(ball_pos)

        # Calculate direction to target
        direction = self.target_pos - self.player.pos

        if direction.length() < 5:
            # Close enough to target
            return pygame.Vector2(0, 0)

        return direction.normalize()

    def should_kick(self, ball_pos: pygame.Vector2) -> bool:
        """Determine if the AI should kick the ball.

        Args:
            ball_pos: Current ball position

        Returns:
            True if AI should kick
        """
        # Only kick if in attack mode and close enough to ball
        if not self.player.can_kick(ball_pos):
            return False

        # In attack mode, always kick when possible
        if self.state == AIState.ATTACK:
            return True

        # In defense mode, kick if ball is very close and heading toward own goal
        if self.state == AIState.DEFENSE:
            distance = self.player.pos.distance_to(ball_pos)
            if distance < AI_KICK_DISTANCE * 0.8:
                return True

        return False
