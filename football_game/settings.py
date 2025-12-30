"""Game settings and constants."""

# Window settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
FPS = 60
TITLE = "Football Game"

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)           # Field color
DARK_GREEN = (0, 100, 0)        # Field lines
RED = (220, 20, 60)             # Player 1 / AI
BLUE = (30, 144, 255)           # Player 2 / Human
YELLOW = (255, 255, 0)          # Ball
GRAY = (128, 128, 128)          # Goal posts

# Field dimensions
FIELD_MARGIN = 40
GOAL_WIDTH = 120
GOAL_DEPTH = 30
CENTER_CIRCLE_RADIUS = 80

# Player settings
PLAYER_RADIUS = 22
PLAYER_ACCEL = 0.5
PLAYER_MAX_SPEED = 7
PLAYER_DAMPING = 0.92           # Friction for player movement
KICK_RADIUS = 40                # Distance to kick the ball
KICK_POWER = 12                 # Impulse given to the ball

# Ball settings
BALL_RADIUS = 12
BALL_MAX_SPEED = 15
BALL_DAMPING = 0.985            # Friction coefficient for ball
BALL_BOUNCE_FACTOR = 0.7        # Energy loss on wall bounce

# AI settings
AI_ACCEL = 0.45
AI_RESPONSE_TIME = 0.1         # Seconds delay for AI decisions
AI_KICK_DISTANCE = 35

# Game states
GOAL_CELEBRATION_TIME = 2.0     # Seconds to celebrate after a goal
WINNING_SCORE = 5               # Score needed to win the game
