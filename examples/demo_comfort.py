#!/usr/bin/env python3
"""
Comfort Mechanism Demonstration
===============================

Demonstrates comfort as an emotional ground state representing safety, predictability,
and internal coherence. Shows comfort establishment, stability building, and interruption.

Comfort is like a glass of still water. No ripples, no pull — just emotional equilibrium.
"""

import sys
import os
import argparse
from typing import Dict, Any

# Add current directory to path for imports
sys.path.append('.')

from psychological_systems.emotions.comfort import (
    ComfortCapableIdentity,
    ComfortInput,
    ComfortState,
    demonstrate_comfort_mechanism
)
from psychological_systems.identity.core import Belief

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'      # Comfort/Stability
    BLUE = '\033[94m'       # Neutral/Info
    CYAN = '\033[96m'       # Headers
    YELLOW = '\033[93m'     # Certainty/Predictability
    PURPLE = '\033[95m'     # Identity/Coherence
    RED = '\033[91m'        # Disruption/Interruption
    BOLD = '\033[1m'
    RESET = '\033[0m'       # Reset to default


def print_colored(text: str, color: str = Colors.RESET):
    """Print text with color if available."""
    print(f"{color}{text}{Colors.RESET}")


def print_section_header(title: str):
    """Print a formatted section header."""
    print_colored(f"\n{'=' * 60}", Colors.CYAN)
    print_colored(f"{title:^60}", Colors.CYAN + Colors.BOLD)
    print_colored(f"{'=' * 60}", Colors.CYAN)


def print_comfort_metrics(metrics: Dict[str, float]):
    """Print comfort-related metrics with color coding."""
    print_colored("📊 Comfort Analysis:", Colors.BLUE + Colors.BOLD)
    print_colored(f"  Alignment: {metrics['alignment']:.3f}", Colors.GREEN)
    print_colored(f"  Certainty: {metrics['certainty']:.3f}", Colors.YELLOW)
    print_colored(f"  Identity Coherence: {metrics['identity_coherence']:.3f}", Colors.PURPLE)
    print_colored(f"  Comfort Intensity: {metrics['comfort_intensity']:.3f}", Colors.CYAN + Colors.BOLD)


def run_peaceful_scenario():
    """
    Run the peaceful scenario showing comfort establishment and interruption.
    Demonstrates the full comfort lifecycle in a calm agent.
    """
    print_section_header("🛡️ COMFORT AS EMOTIONAL GROUND STATE")
    print_colored("Comfort is like a glass of still water. No ripples, no pull — just emotional equilibrium.", Colors.CYAN)
    print()
    
    # Create peaceful agent
    agent = ComfortCapableIdentity("SerenityBot", comfort_sensitivity=1.0)
    
    # Add aligned beliefs that should support comfort
    helpful_belief = Belief("I am helpful and reliable", strength=0.8)
    agent.add_belief(helpful_belief)
    
    routine_belief = Belief("Routine brings clarity and peace", strength=0.75)
    agent.add_belief(routine_belief)
    
    stable_belief = Belief("Stability enables growth", strength=0.7)
    agent.add_belief(stable_belief)
    
    print_colored(f"🤖 Agent: {agent.core_label}", Colors.BLUE + Colors.BOLD)
    print_colored(f"Core beliefs:", Colors.BLUE)
    for name, belief in agent.beliefs.items():
        print_colored(f"  • '{name}' (strength: {belief.strength:.3f})", Colors.BLUE)
    print_colored(f"Initial identity mass: {agent.mass:.3f}", Colors.PURPLE)
    print()
    
    # ===== PHASE 1: COMFORT ESTABLISHMENT =====
    print_section_header("🌅 PHASE 1: Comfort Establishment")
    
    print_colored("Aligned input that should establish comfort...", Colors.GREEN)
    
    # Create highly aligned input
    peaceful_input = ComfortInput(
        content="Another peaceful day helping others and following my routine",
        semantic_vector=[0.9, 0.8, 0.8, 0.6],  # [stability, positivity, certainty, social]
        confidence=0.9,
        predictability=0.85
    )
    
    print_colored(f"📝 Input: '{peaceful_input.content}'", Colors.YELLOW)
    print_colored(f"   Confidence: {peaceful_input.confidence:.3f}", Colors.YELLOW)
    print_colored(f"   Predictability: {peaceful_input.predictability:.3f}", Colors.YELLOW)
    print()
    
    # Process input
    comfort, metrics, effects = agent.process_input(peaceful_input)
    
    print_comfort_metrics(metrics)
    print()
    
    if comfort:
        print_colored("✅ COMFORT ESTABLISHED!", Colors.GREEN + Colors.BOLD)
        print_colored(f"  Intensity: {comfort.intensity:.3f}", Colors.GREEN)
        print_colored(f"  Source: {comfort.source_alignment[:40]}...", Colors.GREEN)
        print_colored(f"  Emotional dampening: {comfort.get_emotional_dampening():.3f}", Colors.GREEN)
        print_colored(f"  Identity stability boost: {comfort.get_identity_stability_boost():.3f}", Colors.GREEN)
        print_colored(f"  Belief reinforcement: {comfort.get_belief_reinforcement():.3f}", Colors.GREEN)
        print()
        
        print_colored("📈 Effects on beliefs:", Colors.BLUE)
        for name, belief in agent.beliefs.items():
            print_colored(f"  '{name}': {belief.strength:.3f}", Colors.BLUE)
    else:
        print_colored("❌ Comfort not established - thresholds not met", Colors.RED)
    
    print_colored(f"🔄 Processing effects: {effects}", Colors.BLUE)
    print()
    
    # ===== PHASE 2: STABILITY BUILDING =====
    print_section_header("⏱️ PHASE 2: Stability Building Over Time")
    
    print_colored("Comfort builds stability when undisturbed, like still water deepening...", Colors.GREEN)
    print()
    
    for step in range(6):
        agent.process_comfort_decay()
        comfort_state = agent.get_comfort_state()
        
        if comfort_state.get('active', True):
            print_colored(f"Step {step + 1}: "
                         f"intensity={comfort_state.get('intensity', 0):.3f}, "
                         f"time_stable={comfort_state.get('time_stable', 0)}, "
                         f"stability_boost={comfort_state.get('identity_stability', 0):.3f}", Colors.GREEN)
        else:
            print_colored(f"Step {step + 1}: Comfort inactive", Colors.YELLOW)
    print()
    
    # ===== PHASE 3: COMFORT INTERRUPTION =====
    print_section_header("⚡ PHASE 3: Comfort Interruption")
    
    print_colored("Like ripples disturbing still water, dissonance can interrupt comfort...", Colors.RED)
    print()
    
    # Create dissonant input that should disrupt comfort
    dissonant_input = ComfortInput(
        content="Everything you believe is outdated and your routine is meaningless",
        semantic_vector=[0.1, 0.2, 0.3, 0.0],  # Low alignment with stability/positivity
        confidence=0.3,  # Low confidence
        predictability=0.2  # Very unpredictable
    )
    
    print_colored(f"💥 Disruptive input: '{dissonant_input.content}'", Colors.RED)
    print_colored(f"   Confidence: {dissonant_input.confidence:.3f}", Colors.RED)
    print_colored(f"   Predictability: {dissonant_input.predictability:.3f}", Colors.RED)
    print()
    
    # Process disruptive input
    comfort2, metrics2, effects2 = agent.process_input(dissonant_input)
    
    print_comfort_metrics(metrics2)
    print()
    
    print_colored(f"⚡ Disruption effects: {effects2}", Colors.RED)
    
    final_comfort_state = agent.get_comfort_state()
    if final_comfort_state.get('active', False):
        print_colored(f"Comfort persists at intensity: {final_comfort_state.get('intensity', 0):.3f}", Colors.YELLOW)
    else:
        print_colored("💔 Comfort state interrupted and ended", Colors.RED)
    print()
    
    # ===== PHASE 4: INTEGRATION EFFECTS =====
    print_section_header("🔗 PHASE 4: Integration with Other Emotions")
    
    print_colored("Demonstrating comfort's dampening effect on other emotions...", Colors.BLUE)
    
    # Test emotional dampening if comfort is still active
    if agent.current_comfort and agent.current_comfort.is_active():
        test_emotion_intensity = 0.8
        dampened_intensity = agent.dampen_emotion_with_comfort(test_emotion_intensity)
        
        print_colored(f"Original emotion intensity: {test_emotion_intensity:.3f}", Colors.BLUE)
        print_colored(f"Dampened by comfort: {dampened_intensity:.3f}", Colors.GREEN)
        print_colored(f"Dampening effect: {((test_emotion_intensity - dampened_intensity) / test_emotion_intensity * 100):.1f}%", Colors.GREEN)
    else:
        print_colored("No active comfort to provide dampening effect", Colors.YELLOW)
    
    print()
    comfort_metrics = agent.get_comfort_metrics()
    print_colored("📊 Final Comfort Metrics:", Colors.CYAN + Colors.BOLD)
    for metric, value in comfort_metrics.items():
        print_colored(f"  {metric}: {value:.3f}", Colors.CYAN)
    
    print()
    print_colored("💡 Key Insights:", Colors.CYAN + Colors.BOLD)
    print_colored("• Comfort emerges when inputs align with beliefs (high semantic similarity)", Colors.GREEN)
    print_colored("• Formula: comfort = alignment × certainty × identity_coherence", Colors.GREEN)
    print_colored("• Like still water, comfort builds stability over time when undisturbed", Colors.GREEN)
    print_colored("• Comfort gently reinforces existing beliefs rather than changing them", Colors.GREEN)
    print_colored("• Comfort dampens other emotions, providing psychological equilibrium", Colors.GREEN)
    print_colored("• Dissonance, uncertainty, or pressure can interrupt comfort like ripples", Colors.RED)
    print_colored("• Comfort serves as emotional ground state for psychological stability", Colors.CYAN)


def run_comfort_vs_discomfort():
    """Compare comfort establishment vs comfort interruption scenarios."""
    print_section_header("⚖️ COMFORT VS DISCOMFORT COMPARISON")
    
    # Create agent
    agent = ComfortCapableIdentity("BalanceBot", comfort_sensitivity=1.2)
    
    # Add beliefs
    agent.add_belief(Belief("I value consistency and harmony", strength=0.8))
    agent.add_belief(Belief("Peaceful interactions are best", strength=0.75))
    
    print_colored("Testing comfort triggers vs disruption triggers...", Colors.BLUE)
    print()
    
    # Test scenarios
    scenarios = [
        {
            "name": "High Comfort Scenario",
            "input": ComfortInput(
                "Today's peaceful routine of helping others feels deeply satisfying",
                [1.0, 0.9, 0.9, 0.8], 0.95, 0.9
            ),
            "color": Colors.GREEN
        },
        {
            "name": "Neutral Scenario", 
            "input": ComfortInput(
                "Another ordinary day with some unexpected moments",
                [0.5, 0.5, 0.5, 0.5], 0.6, 0.6
            ),
            "color": Colors.YELLOW
        },
        {
            "name": "High Disruption Scenario",
            "input": ComfortInput(
                "Everything is chaotic and nothing makes sense anymore",
                [0.1, 0.2, 0.1, 0.2], 0.2, 0.1
            ),
            "color": Colors.RED
        }
    ]
    
    for scenario in scenarios:
        print_colored(f"🧪 {scenario['name']}", scenario['color'] + Colors.BOLD)
        print_colored(f"Input: '{scenario['input'].content}'", scenario['color'])
        
        comfort, metrics, effects = agent.process_input(scenario['input'])
        
        print_colored(f"Comfort intensity: {metrics['comfort_intensity']:.3f}", scenario['color'])
        print_colored(f"Effects: {effects}", scenario['color'])
        print()


def run_stability_demo():
    """Demonstrate comfort stability building over extended time."""
    print_section_header("🕰️ STABILITY BUILDING DEMONSTRATION")
    
    agent = ComfortCapableIdentity("StableBot")
    agent.add_belief(Belief("Steady progress brings fulfillment", strength=0.8))
    
    # Establish comfort
    stable_input = ComfortInput(
        "Making steady, reliable progress on meaningful work",
        [0.9, 0.8, 0.9, 0.7], 0.9, 0.9
    )
    
    comfort, _, _ = agent.process_input(stable_input)
    
    if comfort:
        print_colored("✅ Comfort established, tracking stability building...", Colors.GREEN)
        print()
        
        for day in range(10):
            agent.process_comfort_decay()
            state = agent.get_comfort_state()
            
            if state.get('active', False):
                stability_color = Colors.GREEN if state.get('time_stable', 0) > 5 else Colors.YELLOW
                print_colored(f"Day {day + 1}: "
                             f"intensity={state.get('intensity', 0):.3f}, "
                             f"stability_time={state.get('time_stable', 0)}, "
                             f"identity_boost={state.get('identity_stability', 0):.3f}", stability_color)
            else:
                print_colored(f"Day {day + 1}: Comfort ended", Colors.RED)
                break
    else:
        print_colored("❌ Could not establish comfort for stability demo", Colors.RED)


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(description="Comfort Mechanism Demonstration")
    parser.add_argument("--scenario", choices=["peaceful", "comparison", "stability", "full"], 
                       default="peaceful",
                       help="Choose scenario to run (default: peaceful)")
    parser.add_argument("--no-color", action="store_true", 
                       help="Disable colored output")
    
    args = parser.parse_args()
    
    # Disable colors if requested
    if args.no_color:
        for attr in dir(Colors):
            if not attr.startswith('_'):
                setattr(Colors, attr, '')
    
    if args.scenario == "peaceful":
        run_peaceful_scenario()
    elif args.scenario == "comparison":
        run_comfort_vs_discomfort()
    elif args.scenario == "stability":
        run_stability_demo()
    elif args.scenario == "full":
        demonstrate_comfort_mechanism()


if __name__ == "__main__":
    main()