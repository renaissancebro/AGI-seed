#!/usr/bin/env python3
"""
Pride Mechanism Demonstration
=============================

Demonstrates the pride mechanism with both neurodivergent (mandatory aspirations)
and neurotypical (optional aspirations) integration styles.
"""

import sys
import os
sys.path.append('.')

from psychological_systems.emotions.pride import (
    PrideCapableIdentity,
    Aspiration,
    PrideAction,
    demonstrate_pride_mechanism
)

def run_pride_demo():
    """
    Run the full pride mechanism demonstration showing both integration styles.
    """
    demonstrate_pride_mechanism()

def run_basic_demo():
    """Run a basic pride demo with a single agent."""
    print("🎭 Basic Pride Mechanism Demo")
    print("=" * 40)
    print()
    
    # Create agent with optional aspirations (neurotypical style)
    agent = PrideCapableIdentity("DemoBot", integration_style="optional")
    
    # Add aspiration
    learning_aspiration = Aspiration(
        name="Continuous Learning",
        description="I strive to keep learning and improving",
        domain_vector=[0.3, 0.8, 0.5, 0.2],  # Focus on mastery
        strength=0.7,
        integration_style="optional"
    )
    agent.add_aspiration(learning_aspiration)
    
    print(f"Agent: {agent.core_label}")
    print(f"Aspiration: '{learning_aspiration.name}' (strength: {learning_aspiration.strength:.3f})")
    print()
    
    # Achievement that aligns well with aspiration
    achievement = PrideAction(
        content="Successfully learned a new programming language",
        domain_vector=[0.2, 0.9, 0.4, 0.1],  # High mastery achievement
        recognition_type="peer"
    )
    
    print("🎯 Achievement: Successfully learned a new programming language")
    pride, alignments, effects = agent.achieve_action(achievement)
    
    print(f"Alignment score: {alignments.get('Continuous Learning', 0):.3f}")
    if pride:
        print(f"Pride intensity: {pride.intensity:.3f}")
        print(f"Effects: {effects}")
    else:
        print("No pride triggered")
    
    print(f"Updated aspiration strength: {learning_aspiration.strength:.3f}")

def run_comparison_demo():
    """Run a side-by-side comparison of integration styles."""
    print("🧠 Integration Style Comparison Demo")
    print("=" * 45)
    print()
    
    # Test both styles with same aspiration type
    for style_name, style in [("Neurotypical", "optional"), ("Neurodivergent", "mandatory")]:
        print(f"--- {style_name} Agent ({style} aspirations) ---")
        
        agent = PrideCapableIdentity(f"{style_name}Bot", integration_style=style)
        
        aspiration = Aspiration(
            name="Code Quality",
            description="Write clean, efficient code",
            domain_vector=[0.1, 0.9, 0.7, 0.2],
            strength=0.8,
            integration_style=style
        )
        agent.add_aspiration(aspiration)
        
        # Well-aligned action
        good_action = PrideAction(
            content="Wrote elegant, well-tested code",
            domain_vector=[0.0, 0.8, 0.6, 0.1],
            recognition_type="authority"
        )
        
        pride, alignments, effects = agent.achieve_action(good_action)
        print(f"Good code - Pride: {pride.intensity:.3f if pride else 0:.3f}")
        
        # Poorly aligned action  
        bad_action = PrideAction(
            content="Wrote messy, rushed code",
            domain_vector=[0.0, 0.2, 0.1, 0.0],
            recognition_type="self"
        )
        
        pride2, alignments2, effects2 = agent.achieve_action(bad_action)
        print(f"Bad code - Effects: {effects2 if effects2 else 'None'}")
        print()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--basic":
            run_basic_demo()
        elif sys.argv[1] == "--comparison":
            run_comparison_demo()
        elif sys.argv[1] == "--full":
            run_pride_demo()
        else:
            print("Available options:")
            print("  --basic       Simple pride demonstration")
            print("  --comparison  Compare integration styles")
            print("  --full        Complete demonstration with all features")
            print("  (no args)     Run full demonstration")
    else:
        run_pride_demo()