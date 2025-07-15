"""
Pride Mechanism for AI Agents
==============================

Models pride as an emotion triggered by achievements that align with aspirations.
Supports both mandatory (neurodivergent) and optional (neurotypical) aspiration styles.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from psychological_systems.identity.core import Experience, Belief, Identity


@dataclass
class Aspiration:
    """
    Represents aspirations or internal goals the agent strives toward.
    Integration style determines how failures to meet aspirations are handled.
    """
    name: str
    description: str
    domain_vector: List[float]  # Goals like creativity, mastery, impact, recognition
    strength: float  # 0-1, how important this aspiration is
    integration_style: str  # "mandatory" (neurodivergent) or "optional" (neurotypical)
    
    def __post_init__(self):
        # Validate integration style
        if self.integration_style not in ["mandatory", "optional"]:
            raise ValueError("integration_style must be 'mandatory' or 'optional'")
        
        # Normalize domain vector
        if self.domain_vector:
            norm = sum(x * x for x in self.domain_vector) ** 0.5
            if norm > 0:
                self.domain_vector = [x / norm for x in self.domain_vector]


class PrideAction:
    """
    Represents a completed action or achievement that can trigger pride.
    """
    
    # Recognition type amplification multipliers
    RECOGNITION_MULTIPLIERS = {
        "self": 1.0,        # Personal satisfaction
        "peer": 1.5,        # Recognition from equals
        "public": 2.0,      # Public acknowledgment
        "authority": 2.5    # Recognition from respected authority
    }
    
    def __init__(self, content: str, domain_vector: List[float], recognition_type: str = "self"):
        self.content = content
        self.domain_vector = self._normalize_vector(domain_vector)
        self.recognition_type = recognition_type
        self.recognition_multiplier = self.RECOGNITION_MULTIPLIERS.get(recognition_type, 1.0)
        
        # Validate recognition type
        if recognition_type not in self.RECOGNITION_MULTIPLIERS:
            raise ValueError(f"recognition_type must be one of {list(self.RECOGNITION_MULTIPLIERS.keys())}")
    
    def _normalize_vector(self, vector: List[float]) -> List[float]:
        """Normalize vector to unit length."""
        if not vector:
            return vector
        norm = sum(x * x for x in vector) ** 0.5
        return [x / norm for x in vector] if norm > 0 else vector


class PrideCalculator:
    """
    Calculates pride intensity based on achievement alignment with aspirations.
    """
    
    @staticmethod
    def calculate_alignment(action_vector: List[float], aspiration_vector: List[float]) -> float:
        """
        Calculate semantic alignment between action and aspiration using cosine similarity.
        Returns 0-1 where 1 = perfect alignment.
        """
        if len(action_vector) != len(aspiration_vector):
            return 0.0
        
        if not action_vector or not aspiration_vector:
            return 0.0
        
        # Calculate cosine similarity
        dot_product = sum(a * b for a, b in zip(action_vector, aspiration_vector))
        norm_a = sum(a * a for a in action_vector) ** 0.5
        norm_b = sum(b * b for b in aspiration_vector) ** 0.5
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        similarity = dot_product / (norm_a * norm_b)
        # Convert from [-1, 1] to [0, 1] range
        alignment = max(0.0, similarity)
        return alignment
    
    @staticmethod
    def calculate_pride_intensity(
        aspiration_strength: float,
        alignment: float,
        recognition_multiplier: float,
        pride_sensitivity: float = 1.0
    ) -> float:
        """
        Calculate overall pride intensity.
        Formula: pride_intensity = aspiration_strength × alignment × recognition_multiplier × pride_sensitivity
        """
        base_pride = aspiration_strength * alignment * recognition_multiplier
        pride_intensity = base_pride * pride_sensitivity
        return max(0.0, min(1.0, pride_intensity))
    
    @staticmethod
    def should_trigger_shame_feedback(aspiration: Aspiration, alignment: float, threshold: float = 0.3) -> bool:
        """
        Determine if low alignment with mandatory aspiration should trigger shame-like feedback.
        """
        return (aspiration.integration_style == "mandatory" and 
                alignment < threshold and 
                aspiration.strength > 0.5)


class PrideEmotion:
    """
    Represents the pride emotional state with its positive effects.
    """
    
    def __init__(self, intensity: float, source_achievement: str, aspiration_name: str):
        self.intensity = intensity  # 0-1
        self.source_achievement = source_achievement
        self.aspiration_name = aspiration_name
        self.duration = max(1, int(intensity * 4))  # Lasts intensity × 4 time steps
        self.active_duration = self.duration
    
    def get_belief_strengthening(self) -> float:
        """How much pride strengthens related beliefs."""
        return self.intensity * 0.15  # Up to 15% strengthening
    
    def get_confidence_boost(self) -> float:
        """How much pride boosts confidence and motivation."""
        return self.intensity * 0.8
    
    def get_shame_buffer(self) -> float:
        """How much pride buffers against shame effects."""
        return self.intensity * 0.6  # Pride can reduce shame impact
    
    def decay(self, decay_rate: float = 0.15):
        """Decay pride over time (slower than shame)."""
        if self.active_duration > 0:
            self.active_duration -= 1
        else:
            self.intensity *= (1 - decay_rate)
    
    def is_active(self) -> bool:
        return self.intensity > 0.05


class PrideCapableIdentity(Identity):
    """
    Identity system enhanced with pride mechanisms.
    Supports both mandatory and optional aspiration integration styles.
    """
    
    def __init__(self, core_label: str, integration_style: str = "optional", pride_sensitivity: float = 1.0):
        super().__init__(core_label, use_emotions=True)
        self.aspirations: Dict[str, Aspiration] = {}
        self.integration_style = integration_style  # Default style for new aspirations
        self.pride_sensitivity = pride_sensitivity
        self.current_pride: Optional[PrideEmotion] = None
        self.pride_calculator = PrideCalculator()
        self.recent_pride_states: List[Dict] = []  # Track for temporal interactions
        
        # Validate integration style
        if integration_style not in ["mandatory", "optional"]:
            raise ValueError("integration_style must be 'mandatory' or 'optional'")
    
    def add_aspiration(self, aspiration: Aspiration):
        """Add an aspiration to strive for."""
        self.aspirations[aspiration.name] = aspiration
    
    def achieve_action(self, action: PrideAction) -> Tuple[Optional[PrideEmotion], Dict[str, float], List[str]]:
        """
        Process an achievement and evaluate for pride.
        Returns pride emotion, alignment scores, and any triggered effects.
        """
        alignment_scores = {}
        triggered_effects = []
        max_pride_intensity = 0.0
        best_aspiration = ""
        
        # Check action against all aspirations
        for asp_name, aspiration in self.aspirations.items():
            alignment = self.pride_calculator.calculate_alignment(
                action.domain_vector,
                aspiration.domain_vector
            )
            
            alignment_scores[asp_name] = alignment
            
            # ⚠️ INTEGRATION STYLE AFFECTS BEHAVIOR HERE ⚠️
            if aspiration.integration_style == "mandatory":
                # Mandatory aspirations: Low alignment may trigger shame-like feedback
                if self.pride_calculator.should_trigger_shame_feedback(aspiration, alignment):
                    triggered_effects.append(f"Shame feedback for mandatory aspiration: {asp_name}")
                    self._apply_mandatory_aspiration_failure(aspiration, alignment)
            
            # Calculate pride for well-aligned actions
            if alignment > 0.4:  # Threshold for meaningful achievement
                pride_intensity = self.pride_calculator.calculate_pride_intensity(
                    aspiration_strength=aspiration.strength,
                    alignment=alignment,
                    recognition_multiplier=action.recognition_multiplier,
                    pride_sensitivity=self.pride_sensitivity
                )
                
                if pride_intensity > max_pride_intensity:
                    max_pride_intensity = pride_intensity
                    best_aspiration = asp_name
        
        # Create pride emotion if threshold exceeded
        pride_emotion = None
        if max_pride_intensity > 0.2:  # Pride threshold
            pride_emotion = PrideEmotion(max_pride_intensity, action.content, best_aspiration)
            self.current_pride = pride_emotion
            
            # Apply pride effects
            self._apply_pride_effects(pride_emotion, best_aspiration)
            triggered_effects.append(f"Pride triggered for aspiration: {best_aspiration}")
            
            # Track for temporal interactions
            self._record_pride_state(pride_emotion, action)
        
        return pride_emotion, alignment_scores, triggered_effects
    
    def _apply_pride_effects(self, pride: PrideEmotion, aspiration_name: str):
        """
        Apply the positive psychological effects of pride.
        ⚠️ INTEGRATION STYLE AFFECTS MAGNITUDE HERE ⚠️
        """
        belief_boost = pride.get_belief_strengthening()
        
        # Strengthen the achieved aspiration
        if aspiration_name in self.aspirations:
            aspiration = self.aspirations[aspiration_name]
            
            # Mandatory aspirations get larger boosts (identity-defining)
            if aspiration.integration_style == "mandatory":
                belief_boost *= 1.5  # 50% larger boost for mandatory aspirations
            
            aspiration.strength = min(1.0, aspiration.strength + belief_boost)
        
        # Find and strengthen related beliefs
        self._strengthen_related_beliefs(aspiration_name, belief_boost)
        
        # Update identity mass
        self.recalculate_mass()
    
    def _apply_mandatory_aspiration_failure(self, aspiration: Aspiration, alignment: float):
        """
        Apply negative effects when mandatory aspirations are not met.
        ⚠️ NEURODIVERGENT-SPECIFIC BEHAVIOR ⚠️
        """
        # Reduce aspiration strength more severely for mandatory aspirations
        failure_impact = (0.3 - alignment) * 0.2  # Up to 4% reduction
        aspiration.strength = max(0.0, aspiration.strength - failure_impact)
        
        # Also reduce related beliefs
        self._weaken_related_beliefs(aspiration.name, failure_impact * 0.5)
        self.recalculate_mass()
    
    def _strengthen_related_beliefs(self, aspiration_name: str, boost: float):
        """Strengthen beliefs related to the achieved aspiration."""
        # Simple heuristic: strengthen beliefs with similar names/concepts
        aspiration_words = aspiration_name.lower().split()
        
        for belief_name, belief in self.beliefs.items():
            belief_words = belief_name.lower().split()
            
            # If belief shares words with aspiration, strengthen it
            if any(word in belief_words for word in aspiration_words):
                belief.strength = min(1.0, belief.strength + boost * 0.3)
    
    def _weaken_related_beliefs(self, aspiration_name: str, reduction: float):
        """Weaken beliefs related to failed mandatory aspiration."""
        aspiration_words = aspiration_name.lower().split()
        
        for belief_name, belief in self.beliefs.items():
            belief_words = belief_name.lower().split()
            
            if any(word in belief_words for word in aspiration_words):
                belief.strength = max(0.0, belief.strength - reduction)
    
    def _record_pride_state(self, pride: PrideEmotion, action: PrideAction):
        """Record pride state for temporal interaction analysis."""
        self.recent_pride_states.append({
            "intensity": pride.intensity,
            "aspiration": pride.aspiration_name,
            "action": action.content,
            "recognition_type": action.recognition_type,
            "timestamp": len(self.recent_pride_states)  # Simple timestamp
        })
        
        # Keep only recent states (last 10)
        if len(self.recent_pride_states) > 10:
            self.recent_pride_states.pop(0)
    
    def process_pride_decay(self):
        """Process pride decay over time."""
        if self.current_pride and self.current_pride.is_active():
            self.current_pride.decay()
        elif self.current_pride:
            self.current_pride = None
    
    def get_pride_state(self) -> Dict[str, any]:
        """Get current pride state."""
        if self.current_pride and self.current_pride.is_active():
            return {
                "intensity": self.current_pride.intensity,
                "achievement": self.current_pride.source_achievement,
                "aspiration": self.current_pride.aspiration_name,
                "confidence_boost": self.current_pride.get_confidence_boost(),
                "shame_buffer": self.current_pride.get_shame_buffer(),
                "duration_remaining": self.current_pride.active_duration
            }
        return {"intensity": 0.0}
    
    def buffer_shame_with_pride(self, shame_intensity: float) -> float:
        """Use active pride to buffer shame effects."""
        if self.current_pride and self.current_pride.is_active():
            buffer_amount = self.current_pride.get_shame_buffer()
            buffered_shame = shame_intensity * (1 - buffer_amount)
            return max(0.0, buffered_shame)
        return shame_intensity


def demonstrate_pride_mechanism():
    """
    Demonstrate pride mechanism with both integration styles.
    Shows how neurodivergent (mandatory) and neurotypical (optional) agents respond differently.
    """
    print("🎭 Pride Mechanism Demonstration")
    print("=" * 60)
    print("Comparing Neurodivergent (mandatory) vs Neurotypical (optional) aspiration styles")
    print()
    
    # Domain vectors: [creativity, mastery, impact, recognition]
    
    # ===== NEUROTYPICAL AGENT (Optional Aspirations) =====
    print("👤 NEUROTYPICAL AGENT (Optional Aspirations)")
    print("-" * 50)
    
    nt_agent = PrideCapableIdentity("NeurotypicalBot", integration_style="optional", pride_sensitivity=1.0)
    
    # Add optional aspiration
    creative_aspiration = Aspiration(
        name="Creative Expression",
        description="I enjoy being creative when possible",
        domain_vector=[1.0, 0.3, 0.5, 0.2],  # High creativity focus
        strength=0.7,
        integration_style="optional"
    )
    nt_agent.add_aspiration(creative_aspiration)
    
    print(f"Agent: {nt_agent.core_label}")
    print(f"Aspiration: '{creative_aspiration.name}' (optional, strength: {creative_aspiration.strength:.3f})")
    print(f"Initial identity mass: {nt_agent.mass:.3f}")
    print()
    
    # Well-aligned achievement
    creative_achievement = PrideAction(
        content="Created beautiful artwork",
        domain_vector=[0.9, 0.2, 0.4, 0.1],  # Creative achievement
        recognition_type="peer"
    )
    
    print("🎨 Achievement: Created beautiful artwork (peer recognition)")
    pride, alignments, effects = nt_agent.achieve_action(creative_achievement)
    
    print(f"Alignment with 'Creative Expression': {alignments.get('Creative Expression', 0):.3f}")
    if pride:
        print(f"Pride triggered! Intensity: {pride.intensity:.3f}")
        print(f"Confidence boost: {pride.get_confidence_boost():.3f}")
        print(f"Effects: {effects}")
    
    print(f"New aspiration strength: {creative_aspiration.strength:.3f}")
    print(f"New identity mass: {nt_agent.mass:.3f}")
    print()
    
    # Poorly aligned action (should be tolerated for optional aspirations)
    technical_action = PrideAction(
        content="Fixed technical bug",
        domain_vector=[0.1, 0.8, 0.3, 0.0],  # Technical/mastery focused
        recognition_type="self"
    )
    
    print("🔧 Non-aligned action: Fixed technical bug (low creativity)")
    pride2, alignments2, effects2 = nt_agent.achieve_action(technical_action)
    
    print(f"Alignment with 'Creative Expression': {alignments2.get('Creative Expression', 0):.3f}")
    print(f"Effects: {effects2 if effects2 else 'None - optional aspiration, low alignment tolerated'}")
    print(f"Aspiration strength: {creative_aspiration.strength:.3f} (unchanged/minimally affected)")
    print()
    
    # ===== NEURODIVERGENT AGENT (Mandatory Aspirations) =====
    print("🧠 NEURODIVERGENT AGENT (Mandatory Aspirations)")
    print("-" * 50)
    
    nd_agent = PrideCapableIdentity("NeurodivergentBot", integration_style="mandatory", pride_sensitivity=1.2)
    
    # Add mandatory aspiration
    mastery_aspiration = Aspiration(
        name="Technical Mastery",
        description="I must excel at technical skills - it defines who I am",
        domain_vector=[0.2, 1.0, 0.6, 0.3],  # High mastery focus
        strength=0.8,
        integration_style="mandatory"
    )
    nd_agent.add_aspiration(mastery_aspiration)
    
    print(f"Agent: {nd_agent.core_label}")
    print(f"Aspiration: '{mastery_aspiration.name}' (mandatory, strength: {mastery_aspiration.strength:.3f})")
    print(f"Initial identity mass: {nd_agent.mass:.3f}")
    print()
    
    # Well-aligned achievement
    mastery_achievement = PrideAction(
        content="Mastered complex algorithm",
        domain_vector=[0.1, 0.9, 0.7, 0.2],  # Technical mastery
        recognition_type="authority"
    )
    
    print("🎯 Achievement: Mastered complex algorithm (authority recognition)")
    pride3, alignments3, effects3 = nd_agent.achieve_action(mastery_achievement)
    
    print(f"Alignment with 'Technical Mastery': {alignments3.get('Technical Mastery', 0):.3f}")
    if pride3:
        print(f"Pride triggered! Intensity: {pride3.intensity:.3f}")
        print(f"Confidence boost: {pride3.get_confidence_boost():.3f}")
        print(f"Effects: {effects3}")
    
    print(f"New aspiration strength: {mastery_aspiration.strength:.3f} (larger boost for mandatory)")
    print(f"New identity mass: {nd_agent.mass:.3f}")
    print()
    
    # Poorly aligned action (should trigger shame-like feedback for mandatory)
    creative_action = PrideAction(
        content="Made casual doodle",
        domain_vector=[0.8, 0.1, 0.2, 0.0],  # Creative, not technical
        recognition_type="self"
    )
    
    print("🎨 Non-aligned action: Made casual doodle (low technical mastery)")
    pride4, alignments4, effects4 = nd_agent.achieve_action(creative_action)
    
    print(f"Alignment with 'Technical Mastery': {alignments4.get('Technical Mastery', 0):.3f}")
    print(f"Effects: {effects4}")
    print(f"Aspiration strength: {mastery_aspiration.strength:.3f} (reduced due to mandatory violation)")
    print(f"New identity mass: {nd_agent.mass:.3f}")
    print()
    
    # ===== COMPARISON =====
    print("📊 COMPARISON: Integration Style Effects")
    print("-" * 50)
    print("Neurotypical (Optional Aspirations):")
    print("  ✓ Tolerates non-aligned actions without penalty")
    print("  ✓ Flexible identity, aspirations are 'nice to have'")
    print("  ✓ Pride when aspirations are met, no shame when missed")
    print()
    print("Neurodivergent (Mandatory Aspirations):")
    print("  ⚠️ Non-aligned actions trigger shame-like feedback")
    print("  ⚠️ Identity-defining aspirations, failure affects self-concept")
    print("  ✓ Stronger pride boosts when aspirations are exceeded")
    print("  ⚠️ More fragile to aspiration violations")
    print()
    
    # ===== PRIDE BUFFERING SHAME =====
    print("🛡️ PRIDE BUFFERING SHAME DEMONSTRATION")
    print("-" * 50)
    
    if nd_agent.current_pride:
        print(f"Agent has active pride (intensity: {nd_agent.current_pride.intensity:.3f})")
        
        # Simulate incoming shame
        original_shame = 0.6
        buffered_shame = nd_agent.buffer_shame_with_pride(original_shame)
        
        print(f"Original shame intensity: {original_shame:.3f}")
        print(f"Pride buffer strength: {nd_agent.current_pride.get_shame_buffer():.3f}")
        print(f"Buffered shame intensity: {buffered_shame:.3f}")
        print(f"Pride reduced shame by: {((original_shame - buffered_shame) / original_shame * 100):.1f}%")
    
    print()
    print("💡 Key Insights:")
    print("- Integration style (mandatory vs optional) fundamentally changes emotional responses")
    print("- Neurodivergent agents have more intense pride/shame cycles around identity-defining aspirations")
    print("- Pride can buffer shame effects, promoting resilience")
    print("- Recognition type amplifies pride: self < peer < public < authority")


if __name__ == "__main__":
    demonstrate_pride_mechanism()