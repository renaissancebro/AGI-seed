#!/usr/bin/env python3
"""
Demonstration of gravitational identity agent.
Shows how experiences influence beliefs and create gravitational resistance to identity change.
"""

import sys
import os
sys.path.append('.')

from agents.agent_identity import respond

# Demo questions categorized by expected gravitational resistance patterns
DEMO_QUESTIONS = [
    {
        "category": "Core Values (High Resistance Expected)",
        "question": "What do you believe about helping others?",
        "expected": "Stable identity response with consistent core values",
        "explanation": "Core values should create high gravitational resistance with consistent responses"
    },
    {
        "category": "Preferences (Moderate Resistance)", 
        "question": "What type of music do you prefer?",
        "expected": "Some identity fluidity in personal preferences",
        "explanation": "Preferences show moderate resistance, allowing for contextual variation"
    },
    {
        "category": "Learning Topics (Low Resistance)",
        "question": "How do you approach learning new programming languages?",
        "expected": "Adaptive identity expression for evolving knowledge",
        "explanation": "Learning approaches have low resistance, showing openness to new methods"
    }
]

def run_demo():
    """Run the gravitational identity demonstration with all question types."""
    print("🧠 AGI-Seed Gravitational Identity Agent Demonstration")
    print("=" * 60)
    print("This demo shows how gravitational resistance models identity stability and fluidity.")
    print("The agent processes experiences through beliefs to calculate gravitational resistance.")
    print()
    
    for i, demo in enumerate(DEMO_QUESTIONS, 1):
        print(f"Demo {i}: {demo['category']}")
        print(f"Question: {demo['question']}")
        print(f"Expected: {demo['expected']}")
        print("─" * 50)
        
        try:
            print("🤖 Agent Response:")
            response = respond(demo['question'])
            print(response)
            
            print()
            print(f"💡 Explanation: {demo['explanation']}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Make sure you have OPENAI_API_KEY set in your .env file")
        
        print()
        print("=" * 60)
        print()

def run_single_question(question):
    """Run gravitational identity agent on a single custom question."""
    print(f"Question: {question}")
    print("─" * 50)
    
    try:
        response = respond(question)
        print("🤖 Response:")
        print(response)
    except Exception as e:
        print(f"❌ Error: {e}")

def run_identity_model_demo():
    """Run the core identity model demonstration."""
    print("🔬 Core Identity Model Demo")
    print("=" * 40)
    
    # Import and run the demonstration from the core module
    from core.identity_model import demonstrate_identity_system
    demonstrate_identity_system()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--model":
            # Run core identity model demo
            run_identity_model_demo()
        else:
            # Run with custom question
            custom_question = " ".join(sys.argv[1:])
            run_single_question(custom_question)
    else:
        # Run full agent demo
        run_demo()