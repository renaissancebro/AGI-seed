"""
Gravitational identity modeling system.
Models identity as a gravitational system where experiences influence beliefs,
and beliefs form the mass that creates gravitational resistance to identity change.
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
    """
    def __init__(self, core_label: str):
        self.core_label = core_label
        self.beliefs = {}  # dict of belief name to Belief
        self.mass = 0.0
    
    def add_belief(self, belief: Belief) -> None:
        """Add a belief to the identity system."""
        self.beliefs[belief.name] = belief
        self.recalculate_mass()
    
    def integrate_experience(self, experience: Experience, target_belief_name: str, loss_aversion_factor: float = 2.0) -> None:
        """
        Integrate an experience into a specific belief with loss aversion.
        Negative experiences have amplified impact on identity formation.
        """
        if target_belief_name in self.beliefs:
            self.beliefs[target_belief_name].update_from_experience(experience, loss_aversion_factor)
            self.recalculate_mass()
        else:
            raise ValueError(f"Belief '{target_belief_name}' not found in identity")
    
    def recalculate_mass(self) -> None:
        """Recalculate total identity mass from sum of belief strengths."""
        self.mass = sum(belief.strength for belief in self.beliefs.values())
    
    def gravitational_resistance(self) -> float:
        """Returns resistance to identity change (mass²)."""
        return self.mass ** 2


# Example usage demonstrating the gravitational identity system
def demonstrate_identity_system():
    """
    Example showing how an agent with "I'm a leader" belief 
    processes experiences with realistic scaling, loss aversion, and elastic resilience.
    """
    print("🧠 Gravitational Identity System Demo (Realistic Human Scale)")
    print("=" * 70)
    
    # Create an identity
    agent = Identity("Josh")
    
    # Add a belief about leadership
    leadership_belief = Belief("I'm a leader", strength=0.6)
    agent.add_belief(leadership_belief)
    
    print(f"Initial state:")
    print(f"  Identity: {agent.core_label}")
    print(f"  Belief: '{leadership_belief.name}' (strength: {leadership_belief.strength:.3f})")
    print(f"  Identity mass: {agent.mass:.3f}")
    print(f"  Gravitational resistance: {agent.gravitational_resistance():.3f}")
    print()
    
    # Positive experience
    positive_exp = Experience(
        content="Successfully led team through difficult project",
        valence="positive",
        intensity=0.8,
        source="work_experience"
    )
    
    print(f"Processing positive experience:")
    print(f"  Content: {positive_exp.content}")
    print(f"  Weighted value (no loss aversion): {positive_exp.weighted_value():.3f}")
    
    agent.integrate_experience(positive_exp, "I'm a leader")
    
    print(f"  New belief strength: {leadership_belief.strength:.3f}")
    print(f"  New identity mass: {agent.mass:.3f}")
    print(f"  New gravitational resistance: {agent.gravitational_resistance():.3f}")
    print()
    
    # Negative experience with same intensity to show loss aversion effect
    negative_exp = Experience(
        content="Team criticized my leadership style",
        valence="negative", 
        intensity=0.8,  # Same intensity as positive to show 2x effect
        source="feedback"
    )
    
    print(f"Processing negative experience (same intensity = 0.8):")
    print(f"  Content: {negative_exp.content}")
    print(f"  Weighted value (with 2x loss aversion): {negative_exp.weighted_value():.3f}")
    print(f"  Loss aversion factor: 2.0x (negative experiences hurt more)")
    
    agent.integrate_experience(negative_exp, "I'm a leader")
    
    print(f"  Final belief strength: {leadership_belief.strength:.3f}")
    print(f"  Final identity mass: {agent.mass:.3f}")
    print(f"  Final gravitational resistance: {agent.gravitational_resistance():.3f}")
    print()
    
    print(f"Realistic Scale Analysis:")
    print(f"  Positive experience weighted impact: +{positive_exp.weighted_value():.3f}")
    print(f"  Negative experience weighted impact: {negative_exp.weighted_value():.3f} (2x loss aversion)")
    print(f"  Experience weight (early experiences): {leadership_belief._calculate_experience_weight():.3f}")
    print(f"  Elastic resistance: {leadership_belief._calculate_elastic_resistance():.3f}")
    print(f"  Actual belief change: {leadership_belief.strength - 0.632:.6f} (tiny, realistic)")
    print(f"  Total experiences processed: {len(leadership_belief.experiences)}")
    
    # Demonstrate trauma threshold
    print()
    print("=" * 70)
    print("Demonstrating Trauma Threshold (intensity > 0.9)")
    
    trauma_exp = Experience(
        content="Publicly humiliated and fired as leader",
        valence="negative",
        intensity=0.95,  # Traumatic intensity
        source="major_failure"
    )
    
    strength_before_trauma = leadership_belief.strength
    print(f"Before trauma: {strength_before_trauma:.6f}")
    
    agent.integrate_experience(trauma_exp, "I'm a leader")
    
    print(f"After trauma (intensity=0.95): {leadership_belief.strength:.6f}")
    print(f"Trauma impact: {leadership_belief.strength - strength_before_trauma:.6f} (much larger)")
    
    # Demonstrate elastic recovery
    print()
    print("Demonstrating Elastic Recovery (healing over time):")
    for i in range(5):
        leadership_belief.apply_elastic_recovery()
        print(f"  Recovery step {i+1}: {leadership_belief.strength:.6f}")
    
    # Show accumulated experience diminishing returns
    print()
    print("=" * 70)
    print("Demonstrating Experience Diminishing Returns:")
    
    test_belief = Belief("Test belief", strength=0.5)
    
    # Add many small positive experiences
    for i in range(200):
        small_exp = Experience(f"Small positive {i}", "positive", 0.3, "routine")
        test_belief.update_from_experience(small_exp)
        
        if i in [9, 49, 99, 199]:  # Show key milestones
            weight = test_belief._calculate_experience_weight()
            print(f"  After {i+1} experiences: strength={test_belief.strength:.6f}, weight={weight:.3f}")
    
    print(f"\nFinal analysis:")
    print(f"  200 positive experiences only moved belief from 0.500 to {test_belief.strength:.6f}")
    print(f"  Demonstrates realistic human-scale resistance to change")


if __name__ == "__main__":
    demonstrate_identity_system()