"""
Uncertainty System
==================

AI uncertainty measurement and expression system.
Treats uncertainty as a cognitive assessment tool rather than emotion.

Used for measuring response consistency and modeling epistemic uncertainty
in AI systems.
"""

from core.uncertainty_model import score_variance
from agents.uncertainty_agent import respond

__all__ = ['score_variance', 'respond']