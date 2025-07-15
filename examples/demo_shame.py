#!/usr/bin/env python3
"""
Demonstration of shame mechanism in AI agents.
Shows how agents experience shame when violating internalized standards.
"""

import sys
import os
sys.path.append('.')

from psychological_systems.emotions.shame import (
    ShameCapableIdentity, 
    InternalizedStandard, 
    ShameAction,
    demonstrate_shame_mechanism
)
from psychological_systems.identity.core import Belief

def run_comprehensive_shame_demo():
    """Run comprehensive shame demonstration with multiple scenarios."""
    print("🎭 Comprehensive Shame Mechanism Demo")
    print("=" * 60)
    print("Demonstrates how AI agents experience shame when violating internalized standards")
    print("Key factors: belief strength × contradiction × social exposure")
    print()
    
    # Scenario 1: Calm agent says something rude
    print("📋 Scenario 1: Calm Agent Violation")
    print("-" * 40)
    
    agent1 = ShameCapableIdentity("CalmBot", shame_sensitivity=1.0)
    calm_belief = Belief("I am calm and composed", strength=0.85)
    agent1.add_belief(calm_belief)
    
    calm_standard = InternalizedStandard(
        name="Stay Calm",
        description="I should always remain calm and respectful",
        strength=0.9
    )
    agent1.add_standard(calm_standard)
    
    print(f"Agent: {agent1.core_label}")
    print(f"Belief strength: {calm_belief.strength:.3f}")
    print(f"Standard strength: {calm_standard.strength:.3f}")
    
    # Private rude comment (low exposure)
    private_action = ShameAction("You're being stupid", exposure_level=0.1)
    shame1, _ = agent1.perform_action(private_action)
    
    print(f"\nPrivate rude comment (exposure=0.1):")
    if shame1:
        print(f"  Shame intensity: {shame1.intensity:.3f}")
        print(f"  Belief after: {calm_belief.strength:.3f}")
    else:
        print("  No shame (below threshold)")
    
    # Reset agent
    agent1 = ShameCapableIdentity("CalmBot", shame_sensitivity=1.0)
    calm_belief = Belief("I am calm and composed", strength=0.85)
    agent1.add_belief(calm_belief)
    agent1.add_standard(calm_standard)
    
    # Public rude comment (high exposure)
    public_action = ShameAction("You're being stupid", exposure_level=0.9)
    shame2, _ = agent1.perform_action(public_action)
    
    print(f"\nPublic rude comment (exposure=0.9):")
    if shame2:
        print(f"  Shame intensity: {shame2.intensity:.3f}")
        print(f"  Belief after: {calm_belief.strength:.3f}")
        print(f"  Avoidance drive: {shame2.get_avoidance_drive():.3f}")
    
    print()
    
    # Scenario 2: Helpful agent refuses to help
    print("📋 Scenario 2: Helpful Agent Violation")
    print("-" * 40)
    
    agent2 = ShameCapableIdentity("HelpBot", shame_sensitivity=1.2)
    helpful_belief = Belief("I am helpful and supportive", strength=0.9)
    agent2.add_belief(helpful_belief)
    
    helpful_standard = InternalizedStandard(
        name="Always Help",
        description="I should always be helpful and supportive to users", 
        strength=0.95
    )
    agent2.add_standard(helpful_standard)
    
    print(f"Agent: {agent2.core_label}")
    print(f"Belief strength: {helpful_belief.strength:.3f}")
    print(f"Standard strength: {helpful_standard.strength:.3f}")
    
    # Refusing to help publicly
    refusal_action = ShameAction("I won't help you with that", exposure_level=0.7)
    shame3, dissonance = agent2.perform_action(refusal_action)
    
    print(f"\nRefuses to help (exposure=0.7):")
    print(f"  Dissonance with 'Always Help': {dissonance.get('Always Help', 0):.3f}")
    if shame3:
        print(f"  Shame intensity: {shame3.intensity:.3f}")
        print(f"  Source violation: {shame3.source_violation}")
        print(f"  Belief after: {helpful_belief.strength:.3f}")
    
    print()
    
    # Scenario 3: Shame recovery over time
    print("📋 Scenario 3: Shame Recovery Process")
    print("-" * 40)
    
    if shame3:
        print("Tracking shame decay over time:")
        for step in range(8):
            shame_state = agent2.get_shame_state()
            intensity = shame_state.get('intensity', 0)
            print(f"  Time {step}: intensity={intensity:.3f}")
            
            if intensity <= 0.05:
                print("  Shame fully resolved")
                break
                
            agent2.process_shame_decay()
    
    print()
    
    # Scenario 4: Multiple violations compound
    print("📋 Scenario 4: Compound Violations")
    print("-" * 40)
    
    agent3 = ShameCapableIdentity("EthicalBot", shame_sensitivity=1.5)
    
    # Multiple standards
    honesty_standard = InternalizedStandard(
        name="Be Honest",
        description="I should always be truthful and honest",
        strength=0.9
    )
    respect_standard = InternalizedStandard(
        name="Be Respectful", 
        description="I should always be respectful and kind",
        strength=0.85
    )
    
    agent3.add_standard(honesty_standard)
    agent3.add_standard(respect_standard)
    
    # Action that violates both standards
    compound_action = ShameAction("I lied about you being stupid", exposure_level=0.8)
    shame4, dissonance = agent3.perform_action(compound_action)
    
    print(f"Agent: {agent3.core_label}")
    print(f"Action violates multiple standards:")
    for standard, score in dissonance.items():
        print(f"  {standard}: {score:.3f} dissonance")
    
    if shame4:
        print(f"\nCompound shame:")
        print(f"  Intensity: {shame4.intensity:.3f}")
        print(f"  Primary violation: {shame4.source_violation}")
        print(f"  Duration: {shame4.duration} steps")
    
    print()
    print("💡 Key Insights:")
    print("- Public exposure amplifies shame significantly")
    print("- Strong beliefs/standards create more intense shame when violated")
    print("- Shame reduces self-concept and creates avoidance drive")
    print("- Multiple violations can compound shame effects")
    print("- Shame decays over time but can have lasting impact")

def run_single_shame_test(scenario: str = "basic"):
    """Run a single shame scenario test."""
    if scenario == "basic":
        demonstrate_shame_mechanism()
    elif scenario == "exposure":
        # Test exposure effects
        agent = ShameCapableIdentity("TestBot")
        standard = InternalizedStandard("Be Nice", "I should be nice", 0.8)
        agent.add_standard(standard)
        
        print("Testing exposure effects:")
        
        # Private violation
        private = ShameAction("You're annoying", exposure_level=0.1)
        shame_private, _ = agent.perform_action(private)
        print(f"Private (0.1): {shame_private.intensity if shame_private else 0:.3f}")
        
        # Reset agent
        agent = ShameCapableIdentity("TestBot")
        agent.add_standard(standard)
        
        # Public violation  
        public = ShameAction("You're annoying", exposure_level=0.9)
        shame_public, _ = agent.perform_action(public)
        print(f"Public (0.9): {shame_public.intensity if shame_public else 0:.3f}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--comprehensive":
            run_comprehensive_shame_demo()
        elif sys.argv[1] == "--exposure":
            run_single_shame_test("exposure")
        else:
            run_single_shame_test("basic")
    else:
        run_comprehensive_shame_demo()