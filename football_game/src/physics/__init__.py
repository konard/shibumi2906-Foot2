"""Physics module for collision detection and vector calculations."""

from .collision import check_circle_collision, reflect_velocity, apply_damping
from .field import FieldBounds

__all__ = ['check_circle_collision', 'reflect_velocity', 'apply_damping', 'FieldBounds']
