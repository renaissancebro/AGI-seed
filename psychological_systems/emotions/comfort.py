"""
Comfort Mechanism for AI Agents
===============================

Models comfort as an emotional ground state representing safety, predictability, 
and internal coherence. 

Comfort is like a glass of still water. No ripples, no pull — just emotional equilibrium.
It emerges when inputs align with beliefs, uncertainty is low, and identity remains unchallenged.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from psychological_systems.identity.core import Experience, Belief, Identity


@dataclass
class ComfortState:
    """
    Represents the agent's current state of comfort based on internal coherence,
    environmental predictability, and belief alignment.
    """
    name: str
    description: str
    alignment_threshold: float  # 0-1, minimum alignment needed for comfort
    certainty_threshold: float  # 0-1, minimum certainty needed for comfort
    coherence_weight: float     # 0-1, how much identity coherence matters
    
    def __post_init__(self):
        # Validate thresholds
        self.alignment_threshold = max(0.0, min(1.0, self.alignment_threshold))
        self.certainty_threshold = max(0.0, min(1.0, self.certainty_threshold))
        self.coherence_weight = max(0.0, min(1.0, self.coherence_weight))


class ComfortCalculator:
    """
    Calculates comfort intensity based on semantic alignment, certainty levels,
    and identity coherence. Comfort represents emotional equilibrium.
    """
    
    @staticmethod
    def calculate_semantic_alignment(input_vector: List[float], belief_vectors: List[List[float]]) -> float:
        """
        Calculate how well input aligns with existing beliefs.
        Returns 0-1 where 1 = perfect alignment with belief system.
        """
        if not input_vector or not belief_vectors:
            return 0.5  # Neutral alignment
        
        alignments = []
        for belief_vector in belief_vectors:
            if len(input_vector) != len(belief_vector):
                continue
                
            # Calculate cosine similarity
            dot_product = sum(a * b for a, b in zip(input_vector, belief_vector))
            norm_a = sum(a * a for a in input_vector) ** 0.5
            norm_b = sum(b * b for b in belief_vector) ** 0.5
            
            if norm_a == 0 or norm_b == 0:
                continue
                
            similarity = dot_product / (norm_a * norm_b)
            # Convert from [-1, 1] to [0, 1] range
            alignment = max(0.0, (similarity + 1) / 2)
            alignments.append(alignment)
        
        # Return average alignment across all beliefs
        return sum(alignments) / len(alignments) if alignments else 0.5
    
    @staticmethod
    def calculate_certainty_level(input_confidence: float, environmental_predictability: float) -> float:
        """
        Calculate overall certainty from input confidence and environmental predictability.
        Returns 0-1 where 1 = maximum certainty.
        """
        # Weighted combination of input confidence and environmental predictability
        certainty = (input_confidence * 0.6) + (environmental_predictability * 0.4)
        return max(0.0, min(1.0, certainty))
    
    @staticmethod
    def calculate_identity_coherence(identity_mass: float, recent_changes: float) -> float:
        """
        Calculate identity coherence based on mass stability and recent changes.
        Returns 0-1 where 1 = maximum coherence (stable, established identity).
        """
        # Higher mass = more stable identity, fewer recent changes = more coherent
        base_coherence = min(1.0, identity_mass / 2.0)  # Normalize mass to 0-1 range
        change_penalty = min(1.0, recent_changes * 2.0)  # Recent changes reduce coherence
        coherence = base_coherence * (1 - change_penalty)
        return max(0.0, min(1.0, coherence))
    
    @staticmethod
    def calculate_comfort_intensity(
        alignment: float,
        certainty: float, 
        identity_coherence: float,
        comfort_sensitivity: float = 1.0
    ) -> float:
        """
        Calculate overall comfort intensity.
        
        Formula: comfort_intensity = alignment × certainty × identity_coherence × sensitivity
        
        This represents the multiplicative nature of comfort - all factors must be present
        for comfort to emerge, like a glass of still water requiring no disturbances.
        """
        base_comfort = alignment * certainty * identity_coherence
        comfort_intensity = base_comfort * comfort_sensitivity
        return max(0.0, min(1.0, comfort_intensity))
    
    @staticmethod
    def detect_comfort_interruption(
        dissonance_level: float, 
        uncertainty_spike: float, 
        aspiration_pressure: float,
        interruption_threshold: float = 0.3
    ) -> Tuple[bool, str]:
        """
        Detect if comfort should be interrupted by dissonance, uncertainty, or pressure.
        Returns (should_interrupt, reason).
        """
        max_disruption = max(dissonance_level, uncertainty_spike, aspiration_pressure)
        
        if max_disruption > interruption_threshold:
            if dissonance_level == max_disruption:
                return True, "semantic_dissonance"
            elif uncertainty_spike == max_disruption:
                return True, "uncertainty_spike"
            else:
                return True, "aspiration_pressure"
        
        return False, ""


class ComfortInput:
    """
    Represents an input or experience that can contribute to or disrupt comfort.
    """
    
    def __init__(self, content: str, semantic_vector: List[float], 
                 confidence: float = 0.8, predictability: float = 0.7):
        self.content = content
        self.semantic_vector = self._normalize_vector(semantic_vector)
        self.confidence = max(0.0, min(1.0, confidence))
        self.predictability = max(0.0, min(1.0, predictability))
    
    def _normalize_vector(self, vector: List[float]) -> List[float]:
        """Normalize vector to unit length."""
        if not vector:
            return vector
        norm = sum(x * x for x in vector) ** 0.5
        return [x / norm for x in vector] if norm > 0 else vector
    
    def is_aligned_input(self, belief_vectors: List[List[float]], threshold: float = 0.7) -> bool:
        """Check if this input is well-aligned with existing beliefs."""
        if not belief_vectors:
            return False
        
        alignment = ComfortCalculator.calculate_semantic_alignment(
            self.semantic_vector, belief_vectors
        )
        return alignment >= threshold
    
    def get_disruption_factors(self) -> Dict[str, float]:
        """Get factors that might disrupt comfort."""
        return {
            "low_confidence": 1.0 - self.confidence,
            "unpredictability": 1.0 - self.predictability,
            "semantic_novelty": 0.5  # Placeholder - would be calculated vs existing beliefs
        }


class ComfortEmotion:
    """
    Represents the comfort emotional state - a ground state of emotional equilibrium.
    
    Like still water, comfort provides stability and allows other emotions to settle.
    It dampens emotional extremes while gently reinforcing existing beliefs.
    """
    
    def __init__(self, intensity: float, source_alignment: str, coherence_level: float):
        self.intensity = intensity  # 0-1
        self.source_alignment = source_alignment  # What created this comfort
        self.coherence_level = coherence_level  # How coherent the identity state is
        self.duration = max(1, int(intensity * 10))  # Comfort lasts longer than other emotions
        self.active_duration = self.duration
        self.time_stable = 0  # How long comfort has been stable
    
    def get_belief_reinforcement(self) -> float:
        """How much comfort gently reinforces existing beliefs."""
        # Comfort provides gentle, consistent reinforcement rather than dramatic changes
        return self.intensity * 0.05  # Up to 5% strengthening over time
    
    def get_emotional_dampening(self) -> float:
        """How much comfort dampens other emotional responses."""
        # Comfort reduces the intensity of both positive and negative emotions
        return self.intensity * 0.4  # Up to 40% dampening effect
    
    def get_identity_stability_boost(self) -> float:
        """How much comfort increases resistance to identity change."""
        # Comfort makes identity more stable and resistant to disruption
        return self.intensity * 0.6
    
    def get_learning_modulation(self) -> float:
        """How comfort affects learning - reduces learning rate for stability."""
        # Comfort slightly reduces learning rate to maintain stability
        return -self.intensity * 0.2  # Up to 20% reduction in learning rate
    
    def build_stability(self):
        """Comfort builds stability over time when undisturbed."""
        if self.active_duration > 0:
            self.time_stable += 1
            # Comfort intensifies slightly over time when stable
            stability_bonus = min(0.1, self.time_stable * 0.01)
            self.intensity = min(1.0, self.intensity + stability_bonus)
    
    def decay(self, decay_rate: float = 0.05):
        """Comfort decays very slowly - it's designed to persist."""
        if self.active_duration > 0:
            self.active_duration -= 1
            self.build_stability()  # Try to build stability first
        else:
            # Natural decay is very slow for comfort
            self.intensity *= (1 - decay_rate)
    
    def interrupt(self, interruption_strength: float, reason: str):
        """Interrupt comfort state due to dissonance, uncertainty, or pressure."""
        # Comfort can be suddenly interrupted, like ripples in still water
        interruption_damage = interruption_strength * 0.8
        self.intensity = max(0.0, self.intensity - interruption_damage)
        self.time_stable = 0  # Reset stability timer
        self.active_duration = max(0, self.active_duration - 2)  # Reduce duration
    
    def is_active(self) -> bool:
        return self.intensity > 0.1  # Higher threshold than other emotions


class ComfortCapableIdentity(Identity):
    """
    Identity system enhanced with comfort mechanisms.
    
    Comfort serves as an emotional ground state that emerges when the agent
    experiences aligned inputs, low uncertainty, and stable identity coherence.
    """
    
    def __init__(self, core_label: str, comfort_sensitivity: float = 1.0):
        super().__init__(core_label, use_emotions=True)
        self.comfort_state = ComfortState(
            name="Baseline Comfort",
            description="Default comfort state for aligned, predictable inputs",
            alignment_threshold=0.6,
            certainty_threshold=0.7,
            coherence_weight=0.8
        )
        self.comfort_sensitivity = comfort_sensitivity
        self.current_comfort: Optional[ComfortEmotion] = None
        self.comfort_calculator = ComfortCalculator()
        self.recent_identity_changes = 0.0  # Track recent identity disruptions
        
        # Track comfort history for pattern recognition
        self.comfort_history: List[Dict] = []
        self.baseline_comfort_level = 0.5  # Agent's natural comfort baseline
    
    def process_input(self, comfort_input: ComfortInput) -> Tuple[Optional[ComfortEmotion], Dict[str, float], List[str]]:
        """
        Process an input for comfort effects.
        Returns comfort emotion, metrics, and any effects triggered.
        """
        effects = []
        metrics = {}
        
        # Get belief vectors for alignment calculation
        belief_vectors = [
            self._encode_belief_semantics(belief) 
            for belief in self.beliefs.values()
        ]
        
        # Calculate comfort factors
        alignment = self.comfort_calculator.calculate_semantic_alignment(
            comfort_input.semantic_vector, belief_vectors
        )
        
        certainty = self.comfort_calculator.calculate_certainty_level(
            comfort_input.confidence, comfort_input.predictability
        )
        
        identity_coherence = self.comfort_calculator.calculate_identity_coherence(
            self.mass, self.recent_identity_changes
        )
        
        # Calculate comfort intensity
        comfort_intensity = self.comfort_calculator.calculate_comfort_intensity(
            alignment, certainty, identity_coherence, self.comfort_sensitivity
        )
        
        metrics = {
            "alignment": alignment,
            "certainty": certainty,
            "identity_coherence": identity_coherence,
            "comfort_intensity": comfort_intensity
        }
        
        # Check for comfort triggers
        comfort_emotion = None
        if (alignment >= self.comfort_state.alignment_threshold and 
            certainty >= self.comfort_state.certainty_threshold and
            comfort_intensity > 0.3):  # Comfort threshold
            
            comfort_emotion = ComfortEmotion(comfort_intensity, comfort_input.content, identity_coherence)
            self.current_comfort = comfort_emotion
            effects.append(f"Comfort established: {comfort_input.content[:30]}...")
            
            # Apply comfort effects
            self._apply_comfort_effects(comfort_emotion)
        
        # Check for comfort interruption
        elif self.current_comfort:
            disruption_factors = comfort_input.get_disruption_factors()
            should_interrupt, reason = self.comfort_calculator.detect_comfort_interruption(
                disruption_factors.get("semantic_novelty", 0),
                disruption_factors.get("low_confidence", 0),
                disruption_factors.get("unpredictability", 0)
            )
            
            if should_interrupt:
                interruption_strength = max(disruption_factors.values())
                self.current_comfort.interrupt(interruption_strength, reason)
                effects.append(f"Comfort interrupted by {reason}")
                
                if not self.current_comfort.is_active():
                    self.current_comfort = None
                    effects.append("Comfort state ended")
        
        # Record comfort state
        self._record_comfort_state(comfort_emotion, comfort_input, metrics)
        
        return comfort_emotion, metrics, effects
    
    def _encode_belief_semantics(self, belief: Belief) -> List[float]:
        """Encode belief as semantic vector for alignment calculation."""
        # Simple semantic encoding based on belief content
        # In practice, this would use embeddings or more sophisticated NLP
        text = belief.name.lower()
        
        # Basic semantic dimensions: [stability, positivity, certainty, social]
        vector = [0.0, 0.0, 0.0, 0.0]
        
        # Stability indicators
        if any(word in text for word in ['stable', 'reliable', 'consistent', 'predictable']):
            vector[0] += 1.0
        
        # Positivity indicators  
        if any(word in text for word in ['good', 'positive', 'helpful', 'beneficial']):
            vector[1] += 1.0
        
        # Certainty indicators
        if any(word in text for word in ['certain', 'sure', 'confident', 'clear']):
            vector[2] += 1.0
        
        # Social indicators
        if any(word in text for word in ['social', 'people', 'relationship', 'connect']):
            vector[3] += 1.0
        
        # Normalize
        norm = sum(x * x for x in vector) ** 0.5
        return [x / norm for x in vector] if norm > 0 else vector
    
    def _apply_comfort_effects(self, comfort: ComfortEmotion):
        """Apply the effects of comfort to beliefs and identity."""
        belief_boost = comfort.get_belief_reinforcement()
        
        # Gently strengthen all beliefs (comfort reinforces existing worldview)
        for belief in self.beliefs.values():
            belief.strength = min(1.0, belief.strength + belief_boost)
        
        # Reduce recent identity changes (comfort promotes stability)
        stability_boost = comfort.get_identity_stability_boost()
        self.recent_identity_changes *= (1 - stability_boost)
        
        # Update identity mass
        self.recalculate_mass()
    
    def _record_comfort_state(self, comfort: Optional[ComfortEmotion], 
                             comfort_input: ComfortInput, metrics: Dict[str, float]):
        """Record comfort state for pattern analysis."""
        state_record = {
            "input_content": comfort_input.content,
            "comfort_intensity": comfort.intensity if comfort else 0.0,
            "alignment": metrics.get("alignment", 0.0),
            "certainty": metrics.get("certainty", 0.0),
            "coherence": metrics.get("identity_coherence", 0.0),
            "timestamp": len(self.comfort_history)
        }
        
        self.comfort_history.append(state_record)
        
        # Keep only recent history (last 20 states)
        if len(self.comfort_history) > 20:
            self.comfort_history.pop(0)
    
    def process_comfort_decay(self):
        """Process natural comfort decay and stability building."""
        if self.current_comfort and self.current_comfort.is_active():
            self.current_comfort.decay()
        elif self.current_comfort:
            self.current_comfort = None
    
    def get_comfort_state(self) -> Dict[str, any]:
        """Get current comfort state."""
        if self.current_comfort and self.current_comfort.is_active():
            return {
                "intensity": self.current_comfort.intensity,
                "source": self.current_comfort.source_alignment,
                "coherence_level": self.current_comfort.coherence_level,
                "time_stable": self.current_comfort.time_stable,
                "emotional_dampening": self.current_comfort.get_emotional_dampening(),
                "identity_stability": self.current_comfort.get_identity_stability_boost(),
                "duration_remaining": self.current_comfort.active_duration
            }
        return {"intensity": 0.0, "active": False}
    
    def dampen_emotion_with_comfort(self, emotion_intensity: float) -> float:
        """Use active comfort to dampen other emotional responses."""
        if self.current_comfort and self.current_comfort.is_active():
            dampening = self.current_comfort.get_emotional_dampening()
            dampened_intensity = emotion_intensity * (1 - dampening)
            return max(0.0, dampened_intensity)
        return emotion_intensity
    
    def add_identity_change(self, change_magnitude: float):
        """Track identity changes that might disrupt comfort."""
        self.recent_identity_changes = min(1.0, self.recent_identity_changes + change_magnitude)
        
        # Decay recent changes over time
        self.recent_identity_changes *= 0.95
    
    def get_comfort_metrics(self) -> Dict[str, float]:
        """Get current comfort-related metrics."""
        return {
            "comfort_intensity": self.current_comfort.intensity if self.current_comfort else 0.0,
            "identity_coherence": self.comfort_calculator.calculate_identity_coherence(
                self.mass, self.recent_identity_changes
            ),
            "recent_changes": self.recent_identity_changes,
            "baseline_comfort": self.baseline_comfort_level,
            "comfort_history_length": len(self.comfort_history)
        }


def demonstrate_comfort_mechanism():
    """
    Demonstrate comfort mechanism as emotional ground state.
    Shows comfort emergence, stability building, and interruption dynamics.
    """
    print("🛡️ Comfort Mechanism Demonstration")
    print("=" * 60)
    print("Comfort is like a glass of still water. No ripples, no pull — just emotional equilibrium.")
    print()
    
    # Create agent with comfort capabilities
    agent = ComfortCapableIdentity("PeacefulBot", comfort_sensitivity=1.2)
    
    # Add stable beliefs
    stable_belief = Belief("I am helpful and reliable", strength=0.8)
    agent.add_belief(stable_belief)
    
    predictable_belief = Belief("Routine brings clarity", strength=0.7)
    agent.add_belief(predictable_belief)
    
    print(f"Agent: {agent.core_label}")
    print(f"Beliefs: '{stable_belief.name}' (strength: {stable_belief.strength:.3f})")
    print(f"         '{predictable_belief.name}' (strength: {predictable_belief.strength:.3f})")
    print(f"Initial identity mass: {agent.mass:.3f}")
    print()
    
    # === COMFORT ESTABLISHMENT ===
    print("🌅 PHASE 1: Comfort Establishment")
    print("-" * 40)
    
    # Aligned input that should create comfort
    aligned_input = ComfortInput(
        content="Another day of helping people with their questions - this feels right",
        semantic_vector=[0.8, 0.9, 0.7, 0.6],  # [stability, positivity, certainty, social]
        confidence=0.9,
        predictability=0.8
    )
    
    print(f"Input: '{aligned_input.content}'")
    print(f"Confidence: {aligned_input.confidence:.3f}, Predictability: {aligned_input.predictability:.3f}")
    
    comfort, metrics, effects = agent.process_input(aligned_input)
    
    print(f"\nComfort Analysis:")
    print(f"  Alignment: {metrics['alignment']:.3f}")
    print(f"  Certainty: {metrics['certainty']:.3f}")
    print(f"  Identity Coherence: {metrics['identity_coherence']:.3f}")
    print(f"  Comfort Intensity: {metrics['comfort_intensity']:.3f}")
    
    if comfort:
        print(f"\n✅ COMFORT ESTABLISHED!")
        print(f"  Intensity: {comfort.intensity:.3f}")
        print(f"  Emotional dampening: {comfort.get_emotional_dampening():.3f}")
        print(f"  Identity stability boost: {comfort.get_identity_stability_boost():.3f}")
        print(f"  Belief reinforcement: {comfort.get_belief_reinforcement():.3f}")
    
    print(f"Effects: {effects}")
    print(f"Updated belief strengths:")
    for name, belief in agent.beliefs.items():
        print(f"  '{name}': {belief.strength:.3f}")
    print()
    
    # === COMFORT STABILITY BUILDING ===
    print("⏱️ PHASE 2: Stability Building Over Time")
    print("-" * 40)
    
    print("Processing comfort decay and stability building...")
    for step in range(5):
        agent.process_comfort_decay()
        comfort_state = agent.get_comfort_state()
        print(f"  Step {step + 1}: intensity={comfort_state.get('intensity', 0):.3f}, "
              f"time_stable={comfort_state.get('time_stable', 0)}")
    print()
    
    # === COMFORT INTERRUPTION ===
    print("⚡ PHASE 3: Comfort Interruption")
    print("-" * 40)
    
    # Dissonant input that should interrupt comfort
    dissonant_input = ComfortInput(
        content="Everything you believe about helping is wrong and meaningless",
        semantic_vector=[0.1, 0.0, 0.2, 0.1],  # Low alignment with existing beliefs
        confidence=0.4,  # Low confidence
        predictability=0.2  # Unpredictable
    )
    
    print(f"Dissonant input: '{dissonant_input.content}'")
    print(f"Confidence: {dissonant_input.confidence:.3f}, Predictability: {dissonant_input.predictability:.3f}")
    
    comfort2, metrics2, effects2 = agent.process_input(dissonant_input)
    
    print(f"\nDisruption Analysis:")
    print(f"  Alignment: {metrics2['alignment']:.3f}")
    print(f"  Certainty: {metrics2['certainty']:.3f}")
    print(f"  Identity Coherence: {metrics2['identity_coherence']:.3f}")
    
    print(f"Effects: {effects2}")
    
    final_comfort_state = agent.get_comfort_state()
    print(f"Final comfort state: {final_comfort_state}")
    
    print()
    print("💡 Comfort Summary:")
    print("• Comfort emerges from aligned inputs, high certainty, and identity coherence")
    print("• Like still water, comfort builds stability when undisturbed")
    print("• Comfort gently reinforces existing beliefs and dampens emotional extremes")
    print("• Dissonance, uncertainty, or pressure can interrupt comfort like ripples in water")
    print("• Comfort serves as an emotional ground state enabling psychological equilibrium")


if __name__ == "__main__":
    demonstrate_comfort_mechanism()