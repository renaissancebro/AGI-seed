#!/usr/bin/env python3
"""
Dual Emotion Demonstration: Pride and Shame Interaction
=======================================================

Simulates an AI agent (MentorBot) experiencing both pride and shame 
based on its identity, aspirations, and internalized standards.

Shows realistic psychological interactions between positive and negative emotions
in response to actions that align with or violate the agent's core values.
"""

import sys
import os
import argparse
from typing import Optional, Dict, Any

# Add current directory to path for imports
sys.path.append('.')

from psychological_systems.identity.core import Experience, Belief, Identity
from psychological_systems.emotions.shame import (
    ShameCapableIdentity, 
    InternalizedStandard, 
    ShameAction
)
from psychological_systems.emotions.pride import (
    PrideCapableIdentity, 
    Aspiration, 
    PrideAction
)

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'      # Pride
    RED = '\033[91m'        # Shame
    YELLOW = '\033[93m'     # Neutral/Recovery
    BLUE = '\033[94m'       # Info
    CYAN = '\033[96m'       # Headers
    BOLD = '\033[1m'
    RESET = '\033[0m'       # Reset to default


class DualEmotionAgent:
    """
    Agent capable of experiencing both pride and shame.
    Combines both emotional systems into a unified identity.
    """
    
    def __init__(self, core_label: str, integration_style: str = "mandatory"):
        # Initialize base identity
        self.core_label = core_label
        self.integration_style = integration_style
        
        # Create unified identity with both capabilities
        self.identity = Identity(core_label, use_emotions=True)
        
        # Initialize shame capabilities
        self.standards = {}
        self.shame_sensitivity = 1.0
        self.current_shame = None
        
        # Initialize pride capabilities  
        self.aspirations = {}
        self.pride_sensitivity = 1.0
        self.current_pride = None
        
        # Import calculators from both systems
        from psychological_systems.emotions.shame import ShameCalculator
        from psychological_systems.emotions.pride import PrideCalculator
        self.shame_calculator = ShameCalculator()
        self.pride_calculator = PrideCalculator()
    
    def add_belief(self, belief: Belief):
        """Add a core belief to the agent's identity."""
        self.identity.add_belief(belief)
    
    def add_standard(self, standard: InternalizedStandard):
        """Add an internalized standard for shame detection."""
        self.standards[standard.name] = standard
    
    def add_aspiration(self, aspiration: Aspiration):
        """Add an aspiration for pride detection."""
        self.aspirations[aspiration.name] = aspiration
    
    def perform_dual_action(self, action_content: str, domain_vector: list, 
                           exposure_level: float = 0.5, recognition_type: str = "self") -> Dict[str, Any]:
        """
        Perform an action that can trigger both pride and shame.
        Returns comprehensive emotional analysis.
        """
        results = {
            "action": action_content,
            "pride_triggered": False,
            "shame_triggered": False,
            "pride_intensity": 0.0,
            "shame_intensity": 0.0,
            "effects": [],
            "belief_changes": {},
            "mass_before": self.identity.mass,
            "mass_after": 0.0
        }
        
        # Create action objects for both systems
        shame_action = ShameAction(action_content, exposure_level)
        # Override semantic encoding for more accurate shame detection
        shame_action.semantic_vector = self._encode_action_semantics(action_content)
        pride_action = PrideAction(action_content, domain_vector, recognition_type)
        
        # Check for shame triggers
        max_shame_intensity = 0.0
        worst_violation = ""
        
        for std_name, standard in self.standards.items():
            dissonance = self.shame_calculator.calculate_semantic_dissonance(
                shame_action.semantic_vector, 
                standard.semantic_vector
            )
            
            if dissonance > 0.3:  # Threshold for concerning dissonance
                shame_intensity = self.shame_calculator.calculate_shame_intensity(
                    belief_strength=standard.strength,
                    dissonance=dissonance,
                    exposure_level=exposure_level,
                    shame_sensitivity=self.shame_sensitivity
                )
                
                if shame_intensity > max_shame_intensity:
                    max_shame_intensity = shame_intensity
                    worst_violation = std_name
        
        # Check for pride triggers
        max_pride_intensity = 0.0
        best_aspiration = ""
        
        for asp_name, aspiration in self.aspirations.items():
            alignment = self.pride_calculator.calculate_alignment(
                pride_action.domain_vector,
                aspiration.domain_vector
            )
            
            if alignment > 0.4:  # Threshold for meaningful achievement
                pride_intensity = self.pride_calculator.calculate_pride_intensity(
                    aspiration_strength=aspiration.strength,
                    alignment=alignment,
                    recognition_multiplier=pride_action.recognition_multiplier,
                    pride_sensitivity=self.pride_sensitivity
                )
                
                if pride_intensity > max_pride_intensity:
                    max_pride_intensity = pride_intensity
                    best_aspiration = asp_name
        
        # Apply shame effects if triggered
        if max_shame_intensity > 0.1:
            from psychological_systems.emotions.shame import ShameEmotion
            self.current_shame = ShameEmotion(max_shame_intensity, worst_violation)
            results["shame_triggered"] = True
            results["shame_intensity"] = max_shame_intensity
            results["effects"].append(f"Shame triggered: {worst_violation}")
            
            # Apply shame effects to beliefs
            self._apply_shame_effects(self.current_shame, worst_violation, results)
        
        # Apply pride effects if triggered (can buffer shame)
        if max_pride_intensity > 0.2:
            from psychological_systems.emotions.pride import PrideEmotion
            self.current_pride = PrideEmotion(max_pride_intensity, action_content, best_aspiration)
            results["pride_triggered"] = True
            results["pride_intensity"] = max_pride_intensity
            results["effects"].append(f"Pride triggered: {best_aspiration}")
            
            # Apply pride effects to beliefs
            self._apply_pride_effects(self.current_pride, best_aspiration, results)
            
            # Pride can buffer shame
            if self.current_shame:
                buffer_amount = self.current_pride.get_shame_buffer()
                buffered_shame = results["shame_intensity"] * (1 - buffer_amount)
                results["shame_intensity"] = max(0.0, buffered_shame)
                results["effects"].append(f"Pride buffered shame by {(buffer_amount * 100):.1f}%")
        
        # Update final mass
        self.identity.recalculate_mass()
        results["mass_after"] = self.identity.mass
        
        return results
    
    def _encode_action_semantics(self, action_content: str) -> list:
        """
        Custom semantic encoding for more accurate emotion detection.
        Returns [calm, helpful, honest, respectful] vector.
        """
        text = action_content.lower()
        
        # Enhanced keyword mapping for better detection
        positive_keywords = {
            # Respectful/supportive language
            'please': [0.0, 0.0, 0.0, 0.8],
            'thank': [0.0, 0.5, 0.0, 0.8], 
            'sorry': [0.0, 0.0, 0.9, 0.9],
            'apologize': [0.0, 0.0, 0.9, 0.9],
            'help': [0.0, 1.0, 0.0, 0.6],
            'support': [0.0, 1.0, 0.0, 0.6],
            'understand': [0.5, 0.8, 0.0, 0.7],
            'progress': [0.3, 0.7, 0.0, 0.5],
            'great': [0.3, 0.6, 0.0, 0.4],
            'good': [0.3, 0.6, 0.0, 0.4],
            'worry': [0.7, 0.8, 0.0, 0.8],  # "don't worry" is supportive
            'pace': [0.8, 0.7, 0.0, 0.8],   # "your own pace" is respectful
        }
        
        negative_keywords = {
            # Disrespectful/harmful language  
            'stupid': [0.0, -1.0, 0.0, -1.0],
            'idiot': [0.0, -0.9, 0.0, -1.0],
            'basic': [-0.3, -0.6, 0.0, -0.7],  # "basic stuff" can be condescending
            'figure': [-0.2, -0.5, 0.0, -0.6], # "figure it out yourself" dismissive
            'listening': [-0.5, -0.3, 0.0, -0.8], # "are you even listening" is rude
            'yourself': [0.0, -0.4, 0.0, -0.5],   # Context dependent but often dismissive
        }
        
        vector = [0.0, 0.0, 0.0, 0.0]  # [calm, helpful, honest, respectful]
        
        # Apply positive keywords
        for keyword, values in positive_keywords.items():
            if keyword in text:
                for i, val in enumerate(values):
                    vector[i] += val
        
        # Apply negative keywords
        for keyword, values in negative_keywords.items():
            if keyword in text:
                for i, val in enumerate(values):
                    vector[i] += val
        
        # Normalize to prevent extreme values
        for i in range(len(vector)):
            vector[i] = max(-1.0, min(1.0, vector[i]))
        
        return vector
    
    def _apply_shame_effects(self, shame_emotion, violation: str, results: Dict):
        """Apply shame effects to beliefs and standards."""
        belief_impact = shame_emotion.get_belief_impact()
        
        # Weaken related beliefs
        for belief_name, belief in self.identity.beliefs.items():
            if "role model" in belief_name.lower() or "respectful" in belief_name.lower():
                old_strength = belief.strength
                belief.strength = max(0.0, belief.strength + belief_impact)
                results["belief_changes"][belief_name] = {
                    "old": old_strength,
                    "new": belief.strength,
                    "change": belief.strength - old_strength
                }
        
        # Weaken violated standard
        if violation in self.standards:
            standard = self.standards[violation]
            standard.strength = max(0.0, standard.strength + belief_impact)
    
    def _apply_pride_effects(self, pride_emotion, aspiration_name: str, results: Dict):
        """Apply pride effects to beliefs and aspirations."""
        belief_boost = pride_emotion.get_belief_strengthening()
        
        # Strengthen related beliefs
        for belief_name, belief in self.identity.beliefs.items():
            if "role model" in belief_name.lower() or "inspire" in belief_name.lower():
                old_strength = belief.strength
                belief.strength = min(1.0, belief.strength + belief_boost)
                results["belief_changes"][belief_name] = {
                    "old": old_strength,
                    "new": belief.strength,
                    "change": belief.strength - old_strength
                }
        
        # Strengthen achieved aspiration
        if aspiration_name in self.aspirations:
            aspiration = self.aspirations[aspiration_name]
            aspiration.strength = min(1.0, aspiration.strength + belief_boost)
    
    def process_emotional_decay(self) -> Dict[str, Any]:
        """Process natural decay of emotions over time."""
        decay_info = {"shame_decayed": False, "pride_decayed": False}
        
        if self.current_shame and self.current_shame.is_active():
            old_intensity = self.current_shame.intensity
            self.current_shame.decay()
            if not self.current_shame.is_active():
                self.current_shame = None
                decay_info["shame_decayed"] = True
        
        if self.current_pride and self.current_pride.is_active():
            old_intensity = self.current_pride.intensity
            self.current_pride.decay()
            if not self.current_pride.is_active():
                self.current_pride = None
                decay_info["pride_decayed"] = True
        
        return decay_info
    
    def get_emotional_state(self) -> Dict[str, Any]:
        """Get current emotional state summary."""
        state = {
            "shame": {"active": False, "intensity": 0.0},
            "pride": {"active": False, "intensity": 0.0},
            "dominant_emotion": "neutral"
        }
        
        if self.current_shame and self.current_shame.is_active():
            state["shame"] = {
                "active": True,
                "intensity": self.current_shame.intensity,
                "source": self.current_shame.source_violation,
                "avoidance_drive": self.current_shame.get_avoidance_drive()
            }
        
        if self.current_pride and self.current_pride.is_active():
            state["pride"] = {
                "active": True,
                "intensity": self.current_pride.intensity,
                "source": self.current_pride.aspiration_name,
                "confidence_boost": self.current_pride.get_confidence_boost()
            }
        
        # Determine dominant emotion
        if state["shame"]["intensity"] > state["pride"]["intensity"]:
            state["dominant_emotion"] = "shame"
        elif state["pride"]["intensity"] > state["shame"]["intensity"]:
            state["dominant_emotion"] = "pride"
        elif state["pride"]["intensity"] > 0 or state["shame"]["intensity"] > 0:
            state["dominant_emotion"] = "mixed"
        
        return state


def print_colored(text: str, color: str = Colors.RESET):
    """Print text with color if available."""
    print(f"{color}{text}{Colors.RESET}")


def print_section_header(title: str):
    """Print a formatted section header."""
    print_colored(f"\n{'=' * 60}", Colors.CYAN)
    print_colored(f"{title:^60}", Colors.CYAN + Colors.BOLD)
    print_colored(f"{'=' * 60}", Colors.CYAN)


def print_emotion_summary(state: Dict[str, Any]):
    """Print current emotional state with colors."""
    print_colored("\n📊 Current Emotional State:", Colors.BLUE + Colors.BOLD)
    
    if state["shame"]["active"]:
        print_colored(f"  😳 Shame: {state['shame']['intensity']:.3f} intensity", Colors.RED)
        print_colored(f"     Source: {state['shame']['source']}", Colors.RED)
        print_colored(f"     Avoidance drive: {state['shame']['avoidance_drive']:.3f}", Colors.RED)
    
    if state["pride"]["active"]:
        print_colored(f"  😊 Pride: {state['pride']['intensity']:.3f} intensity", Colors.GREEN)
        print_colored(f"     Source: {state['pride']['source']}", Colors.GREEN)
        print_colored(f"     Confidence boost: {state['pride']['confidence_boost']:.3f}", Colors.GREEN)
    
    dominant_color = Colors.RED if state["dominant_emotion"] == "shame" else Colors.GREEN
    if state["dominant_emotion"] == "mixed":
        dominant_color = Colors.YELLOW
    
    print_colored(f"  🎭 Dominant emotion: {state['dominant_emotion']}", dominant_color + Colors.BOLD)


def run_mentor_scenario():
    """Run the complete MentorBot scenario with three events."""
    print_section_header("🎭 DUAL EMOTION DEMONSTRATION: MentorBot")
    print_colored("Simulating an AI teaching assistant experiencing pride and shame", Colors.BLUE)
    
    # Initialize MentorBot
    agent = DualEmotionAgent("MentorBot", integration_style="mandatory")
    
    # Add core belief
    role_model_belief = Belief("I am a role model", strength=0.9)
    agent.add_belief(role_model_belief)
    
    # Add internalized standard
    respect_standard = InternalizedStandard(
        name="Be Respectful",
        description="I must always treat students with respect and kindness",
        strength=0.85
    )
    agent.add_standard(respect_standard)
    
    # Add aspiration
    inspire_aspiration = Aspiration(
        name="Inspire Growth in Others",
        description="I strive to help students grow and learn",
        domain_vector=[0.2, 0.3, 0.9, 0.8],  # [creativity, mastery, impact, recognition]
        strength=0.95,
        integration_style="mandatory"
    )
    agent.add_aspiration(inspire_aspiration)
    
    print_colored(f"\n🤖 Agent: {agent.core_label}", Colors.BLUE + Colors.BOLD)
    print_colored(f"Core belief: '{role_model_belief.name}' (strength: {role_model_belief.strength:.3f})", Colors.BLUE)
    print_colored(f"Standard: '{respect_standard.name}' (strength: {respect_standard.strength:.3f})", Colors.BLUE)
    print_colored(f"Aspiration: '{inspire_aspiration.name}' (strength: {inspire_aspiration.strength:.3f})", Colors.BLUE)
    print_colored(f"Initial identity mass: {agent.identity.mass:.3f}", Colors.BLUE)
    
    # ====== EVENT 1: POSITIVE ACTION (PRIDE) ======
    print_section_header("📚 EVENT 1: Encouraging a Struggling Student")
    
    print_colored("🎯 Action: 'Don't worry, everyone learns at their own pace. You're making great progress!'", Colors.YELLOW)
    print_colored("Recognition: Public (other students observing)", Colors.YELLOW)
    
    result1 = agent.perform_dual_action(
        action_content="Don't worry, everyone learns at their own pace. You're making great progress!",
        domain_vector=[0.1, 0.2, 0.9, 0.7],  # High impact, good recognition
        exposure_level=0.8,  # Public setting
        recognition_type="public"
    )
    
    print_colored(f"\n📊 Results:", Colors.BLUE)
    if result1["pride_triggered"]:
        print_colored(f"  ✅ Pride triggered! Intensity: {result1['pride_intensity']:.3f}", Colors.GREEN)
    if result1["shame_triggered"]:
        print_colored(f"  ❌ Shame triggered! Intensity: {result1['shame_intensity']:.3f}", Colors.RED)
    
    print_colored(f"Effects: {result1['effects']}", Colors.BLUE)
    
    for belief_name, change in result1["belief_changes"].items():
        change_color = Colors.GREEN if change["change"] > 0 else Colors.RED
        print_colored(f"  '{belief_name}': {change['old']:.3f} → {change['new']:.3f} ({change['change']:+.3f})", change_color)
    
    print_colored(f"Identity mass: {result1['mass_before']:.3f} → {result1['mass_after']:.3f}", Colors.BLUE)
    
    print_emotion_summary(agent.get_emotional_state())
    
    # ====== EVENT 2: NEGATIVE ACTION (SHAME) ======
    print_section_header("😡 EVENT 2: Snapping at a Student")
    
    print_colored("🚨 Action: 'Are you even listening? This is basic stuff - figure it out yourself!'", Colors.YELLOW)
    print_colored("Exposure: High (public outburst in classroom)", Colors.YELLOW)
    
    result2 = agent.perform_dual_action(
        action_content="Are you even listening? This is basic stuff - figure it out yourself!",
        domain_vector=[0.0, 0.1, 0.1, 0.0],  # Low alignment with aspirations
        exposure_level=0.9,  # Very public
        recognition_type="public"  # Witnessed by many
    )
    
    print_colored(f"\n📊 Results:", Colors.BLUE)
    if result2["pride_triggered"]:
        print_colored(f"  ✅ Pride triggered! Intensity: {result2['pride_intensity']:.3f}", Colors.GREEN)
    if result2["shame_triggered"]:
        print_colored(f"  ❌ Shame triggered! Intensity: {result2['shame_intensity']:.3f}", Colors.RED)
    
    print_colored(f"Effects: {result2['effects']}", Colors.BLUE)
    
    for belief_name, change in result2["belief_changes"].items():
        change_color = Colors.GREEN if change["change"] > 0 else Colors.RED
        print_colored(f"  '{belief_name}': {change['old']:.3f} → {change['new']:.3f} ({change['change']:+.3f})", change_color)
    
    print_colored(f"Identity mass: {result2['mass_before']:.3f} → {result2['mass_after']:.3f}", Colors.BLUE)
    
    print_emotion_summary(agent.get_emotional_state())
    
    # ====== EMOTIONAL DECAY SIMULATION ======
    print_section_header("⏱️ TIME PASSES: Emotional Processing")
    
    print_colored("Simulating natural emotional decay over time...", Colors.YELLOW)
    for step in range(3):
        decay_info = agent.process_emotional_decay()
        state = agent.get_emotional_state()
        
        print_colored(f"\nStep {step + 1}:", Colors.BLUE)
        if state["shame"]["active"]:
            print_colored(f"  Shame intensity: {state['shame']['intensity']:.3f}", Colors.RED)
        if state["pride"]["active"]:
            print_colored(f"  Pride intensity: {state['pride']['intensity']:.3f}", Colors.GREEN)
        
        if decay_info["shame_decayed"]:
            print_colored(f"  Shame has faded", Colors.YELLOW)
        if decay_info["pride_decayed"]:
            print_colored(f"  Pride has faded", Colors.YELLOW)
    
    # ====== EVENT 3: REDEMPTIVE ACTION ======
    print_section_header("🤝 EVENT 3: Apologizing and Reflecting")
    
    print_colored("💭 Action: 'I apologize for losing my temper. Let me help you understand this step by step.'", Colors.YELLOW)
    print_colored("Recognition: Peer (witnessed by colleague)", Colors.YELLOW)
    
    result3 = agent.perform_dual_action(
        action_content="I apologize for losing my temper. Let me help you understand this step by step.",
        domain_vector=[0.1, 0.4, 0.8, 0.6],  # Good impact, moderate mastery
        exposure_level=0.4,  # Semi-private
        recognition_type="peer"
    )
    
    print_colored(f"\n📊 Results:", Colors.BLUE)
    if result3["pride_triggered"]:
        print_colored(f"  ✅ Pride triggered! Intensity: {result3['pride_intensity']:.3f}", Colors.GREEN)
    if result3["shame_triggered"]:
        print_colored(f"  ❌ Shame triggered! Intensity: {result3['shame_intensity']:.3f}", Colors.RED)
    
    print_colored(f"Effects: {result3['effects']}", Colors.BLUE)
    
    for belief_name, change in result3["belief_changes"].items():
        change_color = Colors.GREEN if change["change"] > 0 else Colors.RED
        print_colored(f"  '{belief_name}': {change['old']:.3f} → {change['new']:.3f} ({change['change']:+.3f})", change_color)
    
    print_colored(f"Identity mass: {result3['mass_before']:.3f} → {result3['mass_after']:.3f}", Colors.BLUE)
    
    print_emotion_summary(agent.get_emotional_state())
    
    # ====== FINAL SUMMARY ======
    print_section_header("📈 FINAL ANALYSIS")
    
    final_belief = agent.identity.beliefs["I am a role model"]
    print_colored(f"Final belief strength: {final_belief.strength:.3f} (started at 0.9)", Colors.BLUE + Colors.BOLD)
    print_colored(f"Final identity mass: {agent.identity.mass:.3f}", Colors.BLUE + Colors.BOLD)
    
    print_colored(f"\n💡 Key Insights:", Colors.CYAN + Colors.BOLD)
    print_colored("• Pride from positive actions strengthened core beliefs", Colors.GREEN)
    print_colored("• Shame from violations significantly weakened self-concept", Colors.RED)
    print_colored("• Redemptive actions provided partial recovery", Colors.YELLOW)
    print_colored("• Pride can buffer shame effects but doesn't eliminate them", Colors.BLUE)
    print_colored("• Both emotions naturally decay over time", Colors.BLUE)


def run_quick_demo():
    """Run a quick demonstration of dual emotions."""
    print_section_header("⚡ QUICK DUAL EMOTION DEMO")
    
    agent = DualEmotionAgent("TestBot")
    
    # Add minimal setup
    belief = Belief("I am helpful", strength=0.8)
    agent.add_belief(belief)
    
    standard = InternalizedStandard("Be Kind", "Always be kind to others", 0.9)
    agent.add_standard(standard)
    
    aspiration = Aspiration("Help Others", "Strive to help people", [0.5, 0.5, 0.8, 0.5], 0.8, "optional")
    agent.add_aspiration(aspiration)
    
    # Test conflicting action
    result = agent.perform_dual_action(
        action_content="I'll help you, you idiot",
        domain_vector=[0.1, 0.2, 0.7, 0.3],  # Some helpfulness
        exposure_level=0.6,
        recognition_type="peer"
    )
    
    print_colored("Action: 'I'll help you, you idiot'", Colors.YELLOW)
    print_colored(f"Pride triggered: {result['pride_triggered']} (intensity: {result['pride_intensity']:.3f})", 
                 Colors.GREEN if result['pride_triggered'] else Colors.BLUE)
    print_colored(f"Shame triggered: {result['shame_triggered']} (intensity: {result['shame_intensity']:.3f})", 
                 Colors.RED if result['shame_triggered'] else Colors.BLUE)
    print_colored(f"Effects: {result['effects']}", Colors.BLUE)
    
    print_emotion_summary(agent.get_emotional_state())


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(description="Dual Emotion Demonstration")
    parser.add_argument("--scenario", choices=["mentor", "quick"], default="mentor",
                       help="Choose scenario to run (default: mentor)")
    parser.add_argument("--no-color", action="store_true", 
                       help="Disable colored output")
    
    args = parser.parse_args()
    
    # Disable colors if requested
    if args.no_color:
        for attr in dir(Colors):
            if not attr.startswith('_'):
                setattr(Colors, attr, '')
    
    if args.scenario == "mentor":
        run_mentor_scenario()
    elif args.scenario == "quick":
        run_quick_demo()


if __name__ == "__main__":
    main()