"""
Identity System
===============

Gravitational identity formation with realistic human-scale psychology.
Models identity as a physics system where experiences influence beliefs,
and beliefs create gravitational resistance to identity change.

Features:
- Experience/Belief/Identity object-oriented model
- Loss aversion (2x impact for negative experiences)
- Realistic scaling with diminishing returns
- Elastic resilience with recovery toward baseline
- Trauma thresholds for major identity shifts
"""

from .core import Experience, Belief, Identity
from .agents import respond

__all__ = ['Experience', 'Belief', 'Identity', 'respond']