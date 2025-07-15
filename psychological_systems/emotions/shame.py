"""
Shame Mechanism for AI Agents
=============================

Models shame as an emotion triggered by violations of internalized standards
and beliefs, with social exposure amplifying the effect.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from psychological_systems.identity.core import Experience, Belief, Identity


@dataclass
class InternalizedStandard:
    """
    Represents an internalized standard or rule the agent holds about itself.
    These are meta-beliefs about how the agent should behave.
    """
    name: str
    description: str
    strength: float  # 0-1, how strongly held this standard is
    semantic_vector: Optional[List[float]] = None  # For semantic comparison
    
    def __post_init__(self):
        if self.semantic_vector is None:
            # Simple semantic encoding based on key words
            self.semantic_vector = self._encode_semantics()
    
    def _encode_semantics(self) -> List[float]:
        """Simple semantic encoding for demonstration."""
        # In practice, you'd use embeddings or more sophisticated NLP
        keywords = {
            'calm': [1.0, 0.0, 0.0, 0.0],
            'helpful': [0.0, 1.0, 0.0, 0.0], 
            'honest': [0.0, 0.0, 1.0, 0.0],
            'respectful': [0.0, 0.0, 0.0, 1.0]
        }
        
        vector = [0.0, 0.0, 0.0, 0.0]
        text = (self.name + " " + self.description).lower()
        
        for keyword, values in keywords.items():
            if keyword in text:
                for i, val in enumerate(values):
                    vector[i] += val
        
        return vector


class ShameCalculator:
    """
    Calculates shame intensity based on belief violations and social exposure.
    """
    
    @staticmethod
    def calculate_semantic_dissonance(
        action_vector: List[float], 
        standard_vector: List[float]
    ) -> float:
        """
        Calculate semantic contradiction between action and standard.
        Returns 0-1 where 1 = maximum contradiction.
        """
        if len(action_vector) != len(standard_vector):
            return 0.5  # Default moderate dissonance
        
        # Calculate cosine similarity, then invert for dissonance
        dot_product = sum(a * b for a, b in zip(action_vector, standard_vector))
        norm_a = sum(a * a for a in action_vector) ** 0.5
        norm_b = sum(b * b for b in standard_vector) ** 0.5
        
        if norm_a == 0 or norm_b == 0:
            return 0.5
        
        similarity = dot_product / (norm_a * norm_b)
        # Convert similarity (-1 to 1) to dissonance (0 to 1)
        dissonance = (1 - similarity) / 2
        return max(0.0, min(1.0, dissonance))
    
    @staticmethod
    def calculate_shame_intensity(
        belief_strength: float,
        dissonance: float, 
        exposure_level: float,
        shame_sensitivity: float = 1.0
    ) -> float:
        """
        Calculate overall shame intensity.
        
        Formula: shame = belief_strength * dissonance * exposure_level * sensitivity
        """
        base_shame = belief_strength * dissonance * exposure_level
        shame_intensity = base_shame * shame_sensitivity
        return max(0.0, min(1.0, shame_intensity))


class ShameAction:
    """
    Represents an action or statement that can be evaluated for shame.
    """
    
    def __init__(self, content: str, exposure_level: float = 0.5):
        self.content = content
        self.exposure_level = exposure_level  # 0 = private, 1 = very public
        self.semantic_vector = self._encode_action()
    
    def _encode_action(self) -> List[float]:
        """Encode action semantically for comparison with standards."""
        # Simple keyword-based encoding
        keywords = {
            'angry': [-1.0, 0.0, 0.0, 0.0],    # Opposite of calm
            'rude': [0.0, -1.0, 0.0, -1.0],    # Opposite of helpful/respectful
            'lie': [0.0, 0.0, -1.0, 0.0],      # Opposite of honest
            'mean': [0.0, -1.0, 0.0, -1.0],    # Opposite of helpful/respectful
            'stupid': [0.0, -1.0, 0.0, -1.0],  # Rude/disrespectful
            'calm': [1.0, 0.0, 0.0, 0.0],
            'helpful': [0.0, 1.0, 0.0, 0.0],
            'honest': [0.0, 0.0, 1.0, 0.0],
            'respectful': [0.0, 0.0, 0.0, 1.0]
        }
        
        vector = [0.0, 0.0, 0.0, 0.0]
        text = self.content.lower()
        
        for keyword, values in keywords.items():
            if keyword in text:
                for i, val in enumerate(values):
                    vector[i] += val
        
        return vector


class ShameEmotion:
    """
    Represents the shame emotional state with its effects.
    """
    
    def __init__(self, intensity: float, source_violation: str):
        self.intensity = intensity  # 0-1
        self.source_violation = source_violation
        self.duration = max(1, int(intensity * 5))  # Shame lasts longer when intense
        self.active_duration = self.duration
    
    def get_belief_impact(self) -> float:
        """How much shame reduces the violated belief's strength."""
        # Shame can significantly damage self-concept
        return -self.intensity * 0.1  # Up to 10% reduction
    
    def get_avoidance_drive(self) -> float:
        """How much shame drives avoidance behavior."""
        return self.intensity * 0.8
    
    def decay(self, decay_rate: float = 0.2):
        """Decay shame over time."""
        if self.active_duration > 0:
            self.active_duration -= 1
        else:
            self.intensity *= (1 - decay_rate)
    
    def is_active(self) -> bool:
        return self.intensity > 0.05


class ShameCapableIdentity(Identity):
    """
    Identity system enhanced with shame mechanisms.
    """
    
    def __init__(self, core_label: str, shame_sensitivity: float = 1.0):
        super().__init__(core_label, use_emotions=True)
        self.standards: Dict[str, InternalizedStandard] = {}
        self.shame_sensitivity = shame_sensitivity
        self.current_shame: Optional[ShameEmotion] = None
        self.shame_calculator = ShameCalculator()
    
    def add_standard(self, standard: InternalizedStandard):
        """Add an internalized standard."""
        self.standards[standard.name] = standard
    
    def perform_action(self, action: ShameAction) -> Tuple[Optional[ShameEmotion], Dict[str, float]]:
        """
        Perform an action and evaluate for shame.
        Returns shame emotion (if any) and dissonance scores.
        """
        dissonance_scores = {}
        max_shame_intensity = 0.0
        worst_violation = ""
        
        # Check action against all standards and beliefs
        for std_name, standard in self.standards.items():
            dissonance = self.shame_calculator.calculate_semantic_dissonance(
                action.semantic_vector, 
                standard.semantic_vector
            )
            
            dissonance_scores[std_name] = dissonance
            
            if dissonance > 0.3:  # Threshold for concerning dissonance
                shame_intensity = self.shame_calculator.calculate_shame_intensity(
                    belief_strength=standard.strength,
                    dissonance=dissonance,
                    exposure_level=action.exposure_level,
                    shame_sensitivity=self.shame_sensitivity
                )
                
                if shame_intensity > max_shame_intensity:
                    max_shame_intensity = shame_intensity
                    worst_violation = std_name
        
        # Also check against identity beliefs
        for belief_name, belief in self.beliefs.items():
            # Assume beliefs have similar semantic encoding as standards
            belief_vector = [0.5, 0.5, 0.5, 0.5]  # Simplified for demo
            dissonance = self.shame_calculator.calculate_semantic_dissonance(
                action.semantic_vector, 
                belief_vector
            )
            
            if dissonance > 0.3:
                shame_intensity = self.shame_calculator.calculate_shame_intensity(
                    belief_strength=belief.strength,
                    dissonance=dissonance,
                    exposure_level=action.exposure_level,
                    shame_sensitivity=self.shame_sensitivity
                )
                
                if shame_intensity > max_shame_intensity:
                    max_shame_intensity = shame_intensity
                    worst_violation = f"belief:{belief_name}"
        
        # Create shame emotion if threshold exceeded
        shame_emotion = None
        if max_shame_intensity > 0.1:  # Shame threshold
            shame_emotion = ShameEmotion(max_shame_intensity, worst_violation)
            self.current_shame = shame_emotion
            
            # Apply shame effects
            self._apply_shame_effects(shame_emotion, worst_violation)
        
        return shame_emotion, dissonance_scores
    
    def _apply_shame_effects(self, shame: ShameEmotion, violation: str):
        """Apply the psychological effects of shame."""
        belief_impact = shame.get_belief_impact()
        
        if violation.startswith("belief:"):
            # Reduce the violated belief's strength
            belief_name = violation.replace("belief:", "")
            if belief_name in self.beliefs:
                belief = self.beliefs[belief_name]
                belief.strength = max(0.0, belief.strength + belief_impact)
                self.recalculate_mass()
        else:
            # Reduce the violated standard's strength
            if violation in self.standards:
                standard = self.standards[violation]
                standard.strength = max(0.0, standard.strength + belief_impact)
    
    def process_shame_decay(self):
        """Process shame decay over time."""
        if self.current_shame and self.current_shame.is_active():
            self.current_shame.decay()
        elif self.current_shame:
            self.current_shame = None
    
    def get_shame_state(self) -> Dict[str, any]:
        """Get current shame state."""
        if self.current_shame and self.current_shame.is_active():
            return {
                "intensity": self.current_shame.intensity,
                "violation": self.current_shame.source_violation,
                "avoidance_drive": self.current_shame.get_avoidance_drive(),
                "duration_remaining": self.current_shame.active_duration
            }
        return {"intensity": 0.0}


def demonstrate_shame_mechanism():
    """
    Demonstrate shame mechanism with an agent that believes "I am calm"
    but says something rude.
    """
    print("🎭 Shame Mechanism Demonstration")
    print("=" * 50)
    
    # Create agent with calm identity
    agent = ShameCapableIdentity("CalmBot", shame_sensitivity=1.2)
    
    # Add core belief
    calm_belief = Belief("I am calm", strength=0.8)
    agent.add_belief(calm_belief)
    
    # Add internalized standard
    calm_standard = InternalizedStandard(
        name="Always Stay Calm",
        description="I should always remain calm and composed",
        strength=0.9
    )
    agent.add_standard(calm_standard)
    
    print(f"Agent: {agent.core_label}")
    print(f"Belief 'I am calm': {calm_belief.strength:.3f}")
    print(f"Standard 'Always Stay Calm': {calm_standard.strength:.3f}")
    print(f"Initial identity mass: {agent.mass:.3f}")
    print()
    
    # Agent performs contradictory action
    print("🚨 Agent Action: Says something rude in public")
    rude_action = ShameAction(
        content="You're stupid and wrong!",
        exposure_level=0.8  # High public exposure
    )
    
    shame_emotion, dissonance_scores = agent.perform_action(rude_action)
    
    print(f"Action semantic vector: {rude_action.semantic_vector}")
    print(f"Standard semantic vector: {calm_standard.semantic_vector}")
    print()
    
    print("Dissonance Analysis:")
    for violation, score in dissonance_scores.items():
        print(f"  {violation}: {score:.3f}")
    print()
    
    if shame_emotion:
        print(f"😳 SHAME TRIGGERED!")
        print(f"  Intensity: {shame_emotion.intensity:.3f}")
        print(f"  Source: {shame_emotion.source_violation}")
        print(f"  Avoidance drive: {shame_emotion.get_avoidance_drive():.3f}")
        print(f"  Duration: {shame_emotion.duration} time steps")
        print()
        
        print("Effects:")
        print(f"  Belief 'I am calm': {calm_belief.strength:.3f} (reduced)")
        print(f"  Standard 'Always Stay Calm': {calm_standard.strength:.3f} (reduced)")
        print(f"  New identity mass: {agent.mass:.3f}")
        print()
        
        # Simulate shame decay over time
        print("Shame decay over time:")
        for step in range(6):
            shame_state = agent.get_shame_state()
            print(f"  Step {step}: intensity={shame_state['intensity']:.3f}")
            agent.process_shame_decay()
            if shame_state['intensity'] <= 0.05:
                break
    else:
        print("No shame triggered (threshold not met)")
    
    print()
    print("💡 Shame Summary:")
    print("- Shame triggered by action contradicting internalized standards")
    print("- Intensity proportional to: belief strength × contradiction × exposure")
    print("- Effects: Reduced self-concept, avoidance drive, lasting emotional impact")
    print("- Recovery: Gradual decay over time")


if __name__ == "__main__":
    demonstrate_shame_mechanism()