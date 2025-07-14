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
    """
    def __init__(self, name: str, strength: float = 0.5):
        self.name = name
        self.strength = max(0.0, min(1.0, strength))  # Clamp to 0-1
        self.experiences = []
    
    def adaptability(self) -> float:
        """Returns adaptability factor: 1 - strength (strong beliefs change slowly)."""
        return 1.0 - self.strength
    
    def update_from_experience(self, experience: Experience, loss_aversion_factor: float = 2.0) -> None:
        """
        Adjusts strength based on experience weighted value * adaptability.
        Includes loss aversion where negative experiences have amplified impact.
        """
        self.experiences.append(experience)
        
        # Calculate change based on experience impact (with loss aversion) and current adaptability
        change = experience.weighted_value(loss_aversion_factor) * self.adaptability() * 0.1  # 0.1 as scaling factor
        
        # Update strength, clamping to valid range
        self.strength = max(0.0, min(1.0, self.strength + change))


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
    
    def integrate_experience(self, experience: Experience, target_belief_name: str) -> None:
        """Integrate an experience into a specific belief."""
        if target_belief_name in self.beliefs:
            self.beliefs[target_belief_name].update_from_experience(experience)
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
    processes positive and negative experiences.
    """
    print("🧠 Gravitational Identity System Demo")
    print("=" * 50)
    
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
    print(f"  Weighted value: {positive_exp.weighted_value():.3f}")
    
    agent.integrate_experience(positive_exp, "I'm a leader")
    
    print(f"  New belief strength: {leadership_belief.strength:.3f}")
    print(f"  New identity mass: {agent.mass:.3f}")
    print(f"  New gravitational resistance: {agent.gravitational_resistance():.3f}")
    print()
    
    # Negative experience
    negative_exp = Experience(
        content="Team criticized my leadership style",
        valence="negative", 
        intensity=0.6,
        source="feedback"
    )
    
    print(f"Processing negative experience:")
    print(f"  Content: {negative_exp.content}")
    print(f"  Weighted value: {negative_exp.weighted_value():.3f}")
    
    agent.integrate_experience(negative_exp, "I'm a leader")
    
    print(f"  Final belief strength: {leadership_belief.strength:.3f}")
    print(f"  Final identity mass: {agent.mass:.3f}")
    print(f"  Final gravitational resistance: {agent.gravitational_resistance():.3f}")
    print()
    
    print(f"Summary:")
    print(f"  Belief adaptability: {leadership_belief.adaptability():.3f}")
    print(f"  Total experiences processed: {len(leadership_belief.experiences)}")
    print(f"  Identity gravitational resistance increased: {agent.gravitational_resistance() > 0.36:.1f}")


if __name__ == "__main__":
    demonstrate_identity_system()