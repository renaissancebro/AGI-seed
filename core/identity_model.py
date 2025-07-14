"""
Gravitational identity modeling system.
Models identity as a gravitational system where experiences influence beliefs,
and beliefs form the mass that creates gravitational resistance to identity change.
Includes emotion templates for fear, shame, comfort, pride, and loneliness.
"""

class Experience:
    """
    Granular experiences that influence belief strength.
    """
    def __init__(self, content: str, valence: str, intensity: float, source: str):
        self.content = content
        self.valence = valence  # "positive" or "negative"
        self.intensity = intensity  # 0-1 float
        self.source = source
    
    def weighted_value(self, loss_aversion_factor: float = 2.0) -> float:
        """
        Returns a signed float based on valence * intensity with loss aversion.
        
        Loss aversion: negative experiences have 2x impact of positive ones
        (humans fear losing 2x more than gaining the same amount).
        """
        if self.valence == "positive":
            return self.intensity
        else:
            # Negative experiences have amplified impact due to loss aversion
            return -1.0 * self.intensity * loss_aversion_factor


class Belief:
    """
    Mid-level constructs updated through experience accumulation.
    Stronger beliefs resist change more than weaker ones.
    Uses realistic human-scale experience weighting and elastic resilience.
    """
    def __init__(self, name: str, strength: float = 0.5, experience_threshold: int = 1000):
        self.name = name
        self.strength = max(0.0, min(1.0, strength))  # Clamp to 0-1
        self.experiences = []
        self.experience_threshold = experience_threshold  # Target experiences for mature belief
        self.baseline_strength = strength  # For elastic recovery
    
    def adaptability(self) -> float:
        """Returns adaptability factor: 1 - strength (strong beliefs change slowly)."""
        return 1.0 - self.strength
    
    def update_from_experience(self, experience: Experience, loss_aversion_factor: float = 2.0) -> None:
        """
        Adjusts strength based on experience weighted value * adaptability.
        Includes loss aversion, realistic scaling, and elastic resilience.
        """
        self.experiences.append(experience)
        
        # Human-scale experience weighting: impacts decrease as experience count grows
        experience_weight = self._calculate_experience_weight()
        
        # Check for trauma threshold (high intensity negative experiences)
        is_traumatic = experience.valence == "negative" and experience.intensity > 0.9
        
        if is_traumatic:
            # Traumatic experiences can cause significant shifts
            scaling_factor = 0.05  # 5% potential change for trauma
        else:
            # Normal experiences: much smaller impact (0.1% typical)
            scaling_factor = 0.001
        
        # Calculate change with realistic scaling
        raw_change = experience.weighted_value(loss_aversion_factor) * self.adaptability() 
        change = raw_change * scaling_factor * experience_weight
        
        # Apply elastic resilience: resistance to moving too far from baseline
        elastic_resistance = self._calculate_elastic_resistance()
        change *= elastic_resistance
        
        # Update strength, clamping to valid range
        self.strength = max(0.0, min(1.0, self.strength + change))
    
    def _calculate_experience_weight(self) -> float:
        """
        Calculate how much new experiences matter based on accumulated experience.
        More experiences = less weight per new experience (diminishing returns).
        """
        current_experiences = len(self.experiences)
        
        # Early experiences matter more, then diminishing returns
        if current_experiences < 10:
            return 1.0  # First 10 experiences have full weight
        elif current_experiences < 100:
            return 0.5  # Next 90 experiences have half weight
        elif current_experiences < self.experience_threshold:
            return 0.2  # Building toward mature belief
        else:
            return 0.1  # Mature beliefs change very slowly
    
    def _calculate_elastic_resistance(self) -> float:
        """
        Calculate elastic resistance to moving too far from baseline.
        Like a rubber band - harder to stretch further from center.
        """
        distance_from_baseline = abs(self.strength - self.baseline_strength)
        
        # Elastic resistance increases exponentially with distance
        if distance_from_baseline < 0.1:
            return 1.0  # No resistance for small changes
        elif distance_from_baseline < 0.3:
            return 0.7  # Some resistance for moderate changes
        else:
            return 0.3  # Strong resistance for large changes
    
    def apply_elastic_recovery(self, recovery_factor: float = 0.01) -> None:
        """
        Apply gradual elastic recovery toward baseline over time.
        Call this periodically to simulate healing/normalization.
        """
        if abs(self.strength - self.baseline_strength) > 0.05:
            # Move slightly back toward baseline
            direction = 1 if self.baseline_strength > self.strength else -1
            recovery = direction * recovery_factor
            self.strength = max(0.0, min(1.0, self.strength + recovery))


class Identity:
    """
    High-level identity object with beliefs that create gravitational mass.
    Identity mass determines resistance to identity shifts.
    Can optionally include emotion system for enhanced processing.
    """
    def __init__(self, core_label: str, use_emotions: bool = False):
        self.core_label = core_label
        self.beliefs = {}  # dict of belief name to Belief
        self.mass = 0.0
        self.use_emotions = use_emotions
        self.emotion_system = None
        
        if use_emotions:
            try:
                from core.emotion_templates import EmotionSystem
                self.emotion_system = EmotionSystem()
            except ImportError:
                print("Warning: emotion_templates not available, proceeding without emotions")
    
    def add_belief(self, belief: Belief) -> None:
        """Add a belief to the identity system."""
        self.beliefs[belief.name] = belief
        self.recalculate_mass()
    
    def integrate_experience(self, experience: Experience, target_belief_name: str, loss_aversion_factor: float = 2.0) -> None:
        """
        Integrate an experience into a specific belief with loss aversion.
        Negative experiences have amplified impact on identity formation.
        Optionally processes through emotion system if enabled.
        """
        if target_belief_name not in self.beliefs:
            raise ValueError(f"Belief '{target_belief_name}' not found in identity")
        
        belief = self.beliefs[target_belief_name]
        
        # Process through emotions if system is available
        if self.use_emotions and self.emotion_system:
            emotion_mods = self.emotion_system.process_experience(experience, belief)
            # TODO: Apply emotion modifications to experience processing
            # For now, just log active emotions
            active_emotions = self.emotion_system.get_active_emotions()
            if active_emotions:
                # Emotions are processed but don't modify behavior yet (no principles added)
                pass
        
        belief.update_from_experience(experience, loss_aversion_factor)
        self.recalculate_mass()
    
    def get_emotional_state(self) -> dict:
        """Get current emotional state if emotion system is enabled."""
        if self.use_emotions and self.emotion_system:
            return self.emotion_system.get_active_emotions()
        return {}
    
    def recalculate_mass(self) -> None:
        """Recalculate total identity mass from sum of belief strengths."""
        self.mass = sum(belief.strength for belief in self.beliefs.values())
    
    def gravitational_resistance(self) -> float:
        """Returns resistance to identity change (mass²)."""
        return self.mass ** 2


# Example usage demonstrating the gravitational identity system
def demonstrate_identity_system():
    """
    Simple demonstration of key identity system features.
    """
    print("🧠 Identity System Demo")
    print("=" * 40)
    
    # Create agent with leadership belief
    agent = Identity("Josh")
    leadership_belief = Belief("I'm a leader", strength=0.600)
    agent.add_belief(leadership_belief)
    
    print(f"Starting belief strength: {leadership_belief.strength:.3f}")
    print()
    
    # Normal positive experience
    pos_exp = Experience("Led successful project", "positive", 0.8, "work")
    agent.integrate_experience(pos_exp, "I'm a leader")
    print(f"After positive experience: {leadership_belief.strength:.3f} (tiny change)")
    
    # Normal negative experience  
    neg_exp = Experience("Team criticized leadership", "negative", 0.8, "feedback")
    agent.integrate_experience(neg_exp, "I'm a leader")
    print(f"After negative experience: {leadership_belief.strength:.3f} (loss aversion 2x)")
    print()
    
    # Traumatic experience
    print("Trauma threshold demo:")
    trauma = Experience("Publicly fired as leader", "negative", 0.95, "trauma")
    before_trauma = leadership_belief.strength
    agent.integrate_experience(trauma, "I'm a leader")
    print(f"Before trauma: {before_trauma:.3f}")
    print(f"After trauma:  {leadership_belief.strength:.3f} (larger impact)")
    print()
    
    # Elastic recovery
    print("Healing over time:")
    for i in range(3):
        leadership_belief.apply_elastic_recovery()
        print(f"Recovery {i+1}: {leadership_belief.strength:.3f}")
    
    print()
    print("Key features demonstrated:")
    print("✓ Realistic small changes for normal experiences")
    print("✓ Loss aversion (negative impacts 2x positive)")  
    print("✓ Trauma threshold for major events")
    print("✓ Elastic recovery toward baseline")


if __name__ == "__main__":
    demonstrate_identity_system()