"""Collision detection and physics calculations."""

import pygame


def check_circle_collision(pos1: pygame.Vector2, radius1: float,
                           pos2: pygame.Vector2, radius2: float) -> bool:
    """Check if two circles are colliding.

    Args:
        pos1: Center position of first circle
        radius1: Radius of first circle
        pos2: Center position of second circle
        radius2: Radius of second circle

    Returns:
        True if circles are overlapping, False otherwise
    """
    distance = pos1.distance_to(pos2)
    return distance < (radius1 + radius2)


def reflect_velocity(velocity: pygame.Vector2, normal: pygame.Vector2,
                     bounce_factor: float = 1.0) -> pygame.Vector2:
    """Reflect a velocity vector off a surface.

    Uses the formula: v_new = v_old - 2 * (v_old · n) * n

    Args:
        velocity: Current velocity vector
        normal: Normal vector of the surface (should be normalized)
        bounce_factor: Energy loss factor (1.0 = no loss, 0.0 = full stop)

    Returns:
        Reflected velocity vector
    """
    normal = normal.normalize()
    dot_product = velocity.dot(normal)
    reflected = velocity - 2 * dot_product * normal
    return reflected * bounce_factor


def apply_damping(velocity: pygame.Vector2, damping: float) -> pygame.Vector2:
    """Apply damping (friction) to a velocity vector.

    Args:
        velocity: Current velocity vector
        damping: Damping coefficient (0.0 to 1.0)

    Returns:
        Damped velocity vector
    """
    return velocity * damping


def resolve_circle_collision(pos1: pygame.Vector2, vel1: pygame.Vector2, mass1: float,
                              pos2: pygame.Vector2, vel2: pygame.Vector2, mass2: float,
                              radius1: float, radius2: float) -> tuple[pygame.Vector2, pygame.Vector2]:
    """Resolve collision between two circles with elastic collision.

    Args:
        pos1, vel1, mass1: Position, velocity, and mass of first circle
        pos2, vel2, mass2: Position, velocity, and mass of second circle
        radius1, radius2: Radii of the circles

    Returns:
        Tuple of new velocities (vel1_new, vel2_new)
    """
    # Calculate normal and tangent vectors
    normal = (pos2 - pos1).normalize()

    # Calculate relative velocity
    relative_vel = vel1 - vel2

    # Calculate relative velocity along the normal
    vel_along_normal = relative_vel.dot(normal)

    # Do not resolve if velocities are separating
    if vel_along_normal < 0:
        return vel1, vel2

    # Calculate impulse scalar
    restitution = 0.8  # Bounciness
    impulse_scalar = -(1 + restitution) * vel_along_normal
    impulse_scalar /= (1 / mass1 + 1 / mass2)

    # Apply impulse
    impulse = impulse_scalar * normal
    vel1_new = vel1 + impulse / mass1
    vel2_new = vel2 - impulse / mass2

    return vel1_new, vel2_new


def separate_circles(pos1: pygame.Vector2, pos2: pygame.Vector2,
                     radius1: float, radius2: float) -> tuple[pygame.Vector2, pygame.Vector2]:
    """Separate two overlapping circles.

    Args:
        pos1, pos2: Positions of the circles
        radius1, radius2: Radii of the circles

    Returns:
        Tuple of new positions (pos1_new, pos2_new)
    """
    distance = pos1.distance_to(pos2)
    if distance == 0:
        # Circles are at the same position, push apart in arbitrary direction
        return pos1 + pygame.Vector2(1, 0), pos2 - pygame.Vector2(1, 0)

    overlap = (radius1 + radius2) - distance
    if overlap <= 0:
        return pos1, pos2

    # Calculate separation direction
    direction = (pos1 - pos2).normalize()

    # Move each circle apart by half the overlap
    pos1_new = pos1 + direction * (overlap / 2 + 0.5)
    pos2_new = pos2 - direction * (overlap / 2 + 0.5)

    return pos1_new, pos2_new
