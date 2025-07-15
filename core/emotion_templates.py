"""
Emotion template classes for identity system.
Each emotion is a template that can trigger from experiences and influence beliefs.
No specific principles added yet - just the framework structure.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from core.identity_model import Experience, Belief


class EmotionTemplate(ABC):
    """
    Base class for emotion templates.
    Emotions are triggered by experiences and can influence identity formation.
    """
    
    def __init__(self, name: str, intensity: float = 0.0):
        self.name = name
        self.intensity = intensity  # 0-1 scale
        self.triggers = []  # List of experience patterns that activate this emotion
        self.active_duration = 0  # How long emotion remains active
    
    @abstractmethod
    def check_trigger(self, experience: Experience) -> float:
        """
        Check if experience triggers this emotion.
        Returns intensity 0-1 if triggered, 0 if not.
        """
        pass
    
    @abstractmethod
    def influence_belief_update(self, belief: Belief, experience: Experience) -> Dict[str, Any]:
        """
        How this emotion modifies belief updating process.
        Returns dict with modifications to apply.
        """
        pass
    
    def activate(self, intensity: float, duration: int = 3):
        """Activate emotion with given intensity and duration."""
        self.intensity = max(self.intensity, intensity)  # Take strongest intensity
        self.active_duration = max(self.active_duration, duration)
    
    def decay(self, decay_rate: float = 0.3):
        """Decay emotion intensity over time."""
        if self.active_duration > 0:
            self.active_duration -= 1
            if self.active_duration <= 0:
                self.intensity *= (1 - decay_rate)
        else:
            # Always decay when not in active duration
            self.intensity *= (1 - decay_rate)
    
    def is_active(self) -> bool:
        """Check if emotion is currently active."""
        return self.intensity > 0.05  # Threshold for active emotion


class Fear(EmotionTemplate):
    """
    Fear emotion template - heightens threat perception and resistance to change.
    """
    
    def __init__(self):
        super().__init__("fear")
        
    def check_trigger(self, experience: Experience) -> float:
        """
        Fear triggers from high-intensity negative experiences or threat-related content.
        """
        if experience.valence == "negative" and experience.intensity > 0.7:
            # Only high-intensity negative experiences trigger fear
            fear_intensity = min((experience.intensity - 0.7) * 2.0, 1.0)
            
            # TODO: Add content analysis for threat keywords
            # fear_keywords = ["danger", "threat", "loss", "failure", "attack"]
            
            return fear_intensity
        return 0.0
    
    def influence_belief_update(self, belief: Belief, experience: Experience) -> Dict[str, Any]:
        """
        Fear increases resistance to change and amplifies negative experiences.
        """
        modifications = {}
        
        if self.is_active():
            # Fear makes negative experiences feel more intense
            if experience.valence == "negative":
                modifications["intensity_multiplier"] = 1.0 + (self.intensity * 0.5)
            
            # Fear increases resistance to positive changes (threat vigilance)
            modifications["resistance_multiplier"] = 1.0 + (self.intensity * 0.3)
        
        return modifications


class Shame(EmotionTemplate):
    """
    Shame emotion template - erodes self-worth beliefs and increases self-criticism.
    """
    
    def __init__(self):
        super().__init__("shame")
    
    def check_trigger(self, experience: Experience) -> float:
        """
        Shame triggers from experiences involving personal failure or judgment.
        """
        if experience.valence == "negative" and experience.intensity > 0.6:
            # TODO: Add content analysis for shame triggers
            # shame_keywords = ["failure", "embarrassment", "rejected", "criticized", "inadequate"]
            
            # Only moderate-to-high negative experiences trigger shame
            shame_intensity = min((experience.intensity - 0.6) * 1.5, 1.0)
            return shame_intensity
        return 0.0
    
    def influence_belief_update(self, belief: Belief, experience: Experience) -> Dict[str, Any]:
        """
        Shame amplifies negative self-related experiences and dampens positive ones.
        """
        modifications = {}
        
        if self.is_active():
            if experience.valence == "negative":
                # Shame amplifies negative self-experiences
                modifications["intensity_multiplier"] = 1.0 + (self.intensity * 0.7)
            else:
                # Shame dampens positive experiences (self-worth protection)
                modifications["intensity_multiplier"] = 1.0 - (self.intensity * 0.4)
        
        return modifications


class Comfort(EmotionTemplate):
    """
    Comfort emotion template - promotes stability and reduces stress responses.
    """
    
    def __init__(self):
        super().__init__("comfort")
    
    def check_trigger(self, experience: Experience) -> float:
        """
        Comfort triggers from positive, safe, or familiar experiences.
        """
        if experience.valence == "positive":
            # Gentle positive experiences trigger comfort
            comfort_intensity = experience.intensity * 0.6
            
            # TODO: Add content analysis for comfort triggers
            # comfort_keywords = ["safe", "peaceful", "familiar", "supported", "accepted"]
            
            return comfort_intensity
        return 0.0
    
    def influence_belief_update(self, belief: Belief, experience: Experience) -> Dict[str, Any]:
        """
        Comfort reduces resistance to change and promotes balanced processing.
        """
        modifications = {}
        
        if self.is_active():
            # Comfort reduces excessive emotional reactions
            modifications["emotional_dampening"] = self.intensity * 0.3
            
            # Comfort slightly enhances positive experiences
            if experience.valence == "positive":
                modifications["intensity_multiplier"] = 1.0 + (self.intensity * 0.2)
        
        return modifications


class Pride(EmotionTemplate):
    """
    Pride emotion template - reinforces achievement and competence beliefs.
    """
    
    def __init__(self):
        super().__init__("pride")
    
    def check_trigger(self, experience: Experience) -> float:
        """
        Pride triggers from high-achievement or recognition experiences.
        """
        if experience.valence == "positive":
            # High-intensity positive experiences more likely to trigger pride
            pride_intensity = min(experience.intensity * 1.1, 1.0)
            
            # TODO: Add content analysis for achievement keywords
            # pride_keywords = ["success", "achievement", "recognition", "accomplished", "excellent"]
            
            return pride_intensity
        return 0.0
    
    def influence_belief_update(self, belief: Belief, experience: Experience) -> Dict[str, Any]:
        """
        Pride amplifies positive experiences and builds confidence.
        """
        modifications = {}
        
        if self.is_active():
            if experience.valence == "positive":
                # Pride amplifies positive experiences
                modifications["intensity_multiplier"] = 1.0 + (self.intensity * 0.6)
            
            # Pride provides some resilience against negative experiences
            elif experience.valence == "negative":
                modifications["intensity_multiplier"] = 1.0 - (self.intensity * 0.2)
        
        return modifications


class Loneliness(EmotionTemplate):
    """
    Loneliness emotion template - affects social connection and belonging beliefs.
    """
    
    def __init__(self):
        super().__init__("loneliness")
    
    def check_trigger(self, experience: Experience) -> float:
        """
        Loneliness triggers from social rejection or isolation experiences.
        """
        # TODO: Add content analysis for loneliness triggers
        # loneliness_keywords = ["alone", "rejected", "isolated", "ignored", "excluded"]
        
        if experience.valence == "negative":
            # Social negative experiences can trigger loneliness
            loneliness_intensity = experience.intensity * 0.7
            return loneliness_intensity
        return 0.0
    
    def influence_belief_update(self, belief: Belief, experience: Experience) -> Dict[str, Any]:
        """
        Loneliness increases sensitivity to social experiences.
        """
        modifications = {}
        
        if self.is_active():
            # Loneliness makes social experiences more impactful
            # TODO: Add logic to detect social vs non-social experiences
            modifications["social_sensitivity"] = 1.0 + (self.intensity * 0.5)
            
            # Loneliness can amplify both positive and negative social experiences
            modifications["intensity_multiplier"] = 1.0 + (self.intensity * 0.3)
        
        return modifications


class EmotionSystem:
    """
    Manages multiple emotions and their interactions with identity formation.
    """
    
    def __init__(self):
        self.emotions = {
            "fear": Fear(),
            "shame": Shame(), 
            "comfort": Comfort(),
            "pride": Pride(),
            "loneliness": Loneliness()
        }
    
    def process_experience(self, experience: Experience, belief: Belief) -> Dict[str, Any]:
        """
        Process experience through all emotion templates and return combined modifications.
        """
        all_modifications = {}
        
        # Check each emotion for triggers
        for emotion in self.emotions.values():
            trigger_intensity = emotion.check_trigger(experience)
            if trigger_intensity > 0:
                emotion.activate(trigger_intensity)
        
        # Collect modifications from active emotions
        for emotion in self.emotions.values():
            if emotion.is_active():
                mods = emotion.influence_belief_update(belief, experience)
                # TODO: Add logic to combine multiple modifications
                all_modifications.update(mods)
        
        # Decay all emotions
        for emotion in self.emotions.values():
            emotion.decay()
        
        return all_modifications
    
    def get_active_emotions(self) -> Dict[str, float]:
        """Get currently active emotions and their intensities."""
        return {
            name: emotion.intensity 
            for name, emotion in self.emotions.items() 
            if emotion.is_active()
        }


# Example usage
def demonstrate_emotion_templates():
    """Simple demonstration of emotion template system."""
    print("🎭 Emotion Templates Demo")
    print("=" * 30)
    
    emotion_system = EmotionSystem()
    
    # Test experiences
    experiences = [
        Experience("Won a major award", "positive", 0.9, "achievement"),
        Experience("Failed public presentation", "negative", 0.8, "failure"),
        Experience("Received kind support", "positive", 0.6, "social"),
        Experience("Felt completely alone", "negative", 0.7, "isolation")
    ]
    
    test_belief = Belief("I am competent", strength=0.6)
    
    for exp in experiences:
        print(f"\nExperience: {exp.content}")
        mods = emotion_system.process_experience(exp, test_belief)
        active = emotion_system.get_active_emotions()
        
        if active:
            print(f"Active emotions: {list(active.keys())}")
        else:
            print("No emotions triggered")


if __name__ == "__main__":
    demonstrate_emotion_templates()