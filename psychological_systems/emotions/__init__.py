"""
Emotion Templates System
========================

Emotion detection and influence framework with templates for:
- Fear: Heightens threat perception, increases resistance to change
- Shame: Erodes self-worth, amplifies negative self-experiences  
- Comfort: Promotes stability, reduces stress responses
- Pride: Reinforces achievement, builds confidence
- Loneliness: Affects social connection beliefs

Framework ready for behavioral principles to be added.
"""

from .templates import (
    EmotionTemplate, 
    Fear, 
    Shame, 
    Comfort, 
    Pride, 
    Loneliness, 
    EmotionSystem,
    demonstrate_emotion_templates
)

__all__ = [
    'EmotionTemplate', 
    'Fear', 
    'Shame', 
    'Comfort', 
    'Pride', 
    'Loneliness', 
    'EmotionSystem',
    'demonstrate_emotion_templates'
]