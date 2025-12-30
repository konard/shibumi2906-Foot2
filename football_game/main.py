"""Main entry point for the football game."""

import sys
import pygame

# Add src to path for imports
sys.path.insert(0, '.')

from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
    FIELD_MARGIN, RED, BLUE, WINNING_SCORE
)
from src.entities import Player, Ball, Goal
from src.physics.field import FieldBounds
from src.physics.collision import (
    check_circle_collision, separate_circles,
    resolve_circle_collision
)
from src.ai import AIBot
from src.ui import GameRenderer, Menu
from src.manager import GameStateManager, GameState


class Game:
    """Main game class."""

    def __init__(self) -> None:
        """Initialize the game."""
        pygame.init()
        pygame.display.set_caption(TITLE)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize game components
        self.field = FieldBounds()
        self.state_manager = GameStateManager()
        self.renderer = GameRenderer(self.screen)
        self.menu = Menu(self.screen)

        # Game entities
        self.goals = [Goal('left'), Goal('right')]
        self._reset_entities()

    def _reset_entities(self) -> None:
        """Reset all game entities to starting positions."""
        field_center = self.field.get_field_center()

        # AI player on the left
        ai_start = pygame.Vector2(FIELD_MARGIN + 100, SCREEN_HEIGHT // 2)
        self.ai_player = Player(ai_start, RED, is_ai=True)

        # Human player on the right
        player_start = pygame.Vector2(SCREEN_WIDTH - FIELD_MARGIN - 100, SCREEN_HEIGHT // 2)
        self.human_player = Player(player_start, BLUE, is_ai=False)

        # Ball in the center
        self.ball = Ball(field_center)

        # AI controller
        self.ai_bot = AIBot(self.ai_player, self.field)

    def _reset_after_goal(self) -> None:
        """Reset positions after a goal is scored."""
        field_center = self.field.get_field_center()

        # Reset player positions
        self.ai_player.pos = pygame.Vector2(FIELD_MARGIN + 100, SCREEN_HEIGHT // 2)
        self.ai_player.vel = pygame.Vector2(0, 0)

        self.human_player.pos = pygame.Vector2(SCREEN_WIDTH - FIELD_MARGIN - 100, SCREEN_HEIGHT // 2)
        self.human_player.vel = pygame.Vector2(0, 0)

        # Reset ball
        self.ball.reset(field_center)

    def handle_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if self.state_manager.is_menu():
                action = self.menu.handle_input(event)
                if action == 'play':
                    self.state_manager.start_game()
                    self._reset_entities()
                elif action == 'quit':
                    self.running = False

            elif self.state_manager.is_game_over():
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.state_manager.start_game()
                        self._reset_entities()
                    elif event.key == pygame.K_ESCAPE:
                        self.state_manager.return_to_menu()

            elif self.state_manager.is_playing():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state_manager.return_to_menu()
                    elif event.key == pygame.K_SPACE:
                        # Human player kick
                        if self.human_player.can_kick(self.ball.pos):
                            impulse = self.human_player.kick_ball(self.ball.pos)
                            self.ball.apply_impulse(impulse)

    def handle_input(self) -> None:
        """Handle continuous keyboard input for player movement."""
        if not self.state_manager.is_playing():
            return

        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)

        # WASD and Arrow keys
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            direction.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            direction.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            direction.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            direction.x += 1

        self.human_player.apply_input(direction)

    def update_ai(self) -> None:
        """Update AI player behavior."""
        if not self.state_manager.is_playing():
            return

        # Get AI movement direction
        direction = self.ai_bot.get_movement_direction(self.ball.pos)
        self.ai_player.apply_input(direction)

        # Check if AI should kick
        if self.ai_bot.should_kick(self.ball.pos):
            impulse = self.ai_player.kick_ball(self.ball.pos)
            self.ball.apply_impulse(impulse)

    def update_physics(self) -> None:
        """Update all physics calculations."""
        if not self.state_manager.is_playing():
            return

        # Update entities
        self.human_player.update()
        self.ai_player.update()
        self.ball.update()

        # Check player-ball collisions
        self._handle_player_ball_collision(self.human_player)
        self._handle_player_ball_collision(self.ai_player)

        # Check player-player collision
        if check_circle_collision(
            self.human_player.pos, self.human_player.radius,
            self.ai_player.pos, self.ai_player.radius
        ):
            # Separate players
            self.human_player.pos, self.ai_player.pos = separate_circles(
                self.human_player.pos, self.ai_player.pos,
                self.human_player.radius, self.ai_player.radius
            )
            # Resolve collision
            self.human_player.vel, self.ai_player.vel = resolve_circle_collision(
                self.human_player.pos, self.human_player.vel, self.human_player.mass,
                self.ai_player.pos, self.ai_player.vel, self.ai_player.mass,
                self.human_player.radius, self.ai_player.radius
            )

        # Check field bounds for players
        self.human_player.pos = self.field.check_player_bounds(
            self.human_player.pos, self.human_player.radius
        )
        self.ai_player.pos = self.field.check_player_bounds(
            self.ai_player.pos, self.ai_player.radius
        )

        # Check ball bounds and goals
        self.ball.pos, self.ball.vel, goal_scored = self.field.check_ball_bounds(
            self.ball.pos, self.ball.vel, self.ball.radius
        )

        # Handle goal
        if goal_scored == 1:
            # Ball went into left goal (AI's goal) - point for human
            self.state_manager.goal_scored('player')
        elif goal_scored == 2:
            # Ball went into right goal (human's goal) - point for AI
            self.state_manager.goal_scored('ai')

    def _handle_player_ball_collision(self, player: Player) -> None:
        """Handle collision between a player and the ball.

        Args:
            player: The player to check collision with
        """
        if check_circle_collision(
            player.pos, player.radius,
            self.ball.pos, self.ball.radius
        ):
            # Separate ball and player
            _, self.ball.pos = separate_circles(
                player.pos, self.ball.pos,
                player.radius, self.ball.radius
            )

            # Apply some velocity transfer
            direction = (self.ball.pos - player.pos).normalize()
            push_strength = max(player.vel.length() * 0.5, 2.0)
            self.ball.vel += direction * push_strength

    def update(self) -> None:
        """Update game state."""
        if self.state_manager.is_celebrating():
            if self.state_manager.update_celebration():
                if not self.state_manager.is_game_over():
                    self._reset_after_goal()

    def render(self) -> None:
        """Render the game."""
        if self.state_manager.is_menu():
            self.menu.draw()
        else:
            # Draw field
            self.renderer.draw_field()

            # Draw goals
            for goal in self.goals:
                goal.draw(self.screen)

            # Draw entities
            self.ball.draw(self.screen)
            self.ai_player.draw(self.screen)
            self.human_player.draw(self.screen)

            # Draw score
            self.renderer.draw_score(
                self.state_manager.ai_score,
                self.state_manager.player_score
            )

            # Draw controls hint
            self.renderer.draw_controls_hint()

            # Draw celebration text
            if self.state_manager.is_celebrating():
                progress = self.state_manager.get_celebration_progress()
                # Pulsing alpha effect
                alpha = int(255 * (1 - abs(progress * 2 - 1)))
                self.renderer.draw_goal_text(
                    self.state_manager.last_scorer,
                    alpha
                )

            # Draw game over
            if self.state_manager.is_game_over():
                self.renderer.draw_game_over(
                    self.state_manager.get_winner(),
                    self.state_manager.ai_score,
                    self.state_manager.player_score
                )

        pygame.display.flip()

    def run(self) -> None:
        """Main game loop."""
        while self.running:
            self.handle_events()

            if self.state_manager.is_playing():
                self.handle_input()
                self.update_ai()
                self.update_physics()

            self.update()
            self.render()

            self.clock.tick(FPS)

        pygame.quit()


def main() -> None:
    """Entry point."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
