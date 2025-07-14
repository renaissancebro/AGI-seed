#!/usr/bin/env python3
"""
Demonstration of identity agent with physics-based modeling.
Shows how gravitational forces model identity formation and consistency.
"""

import sys
import os
sys.path.append('.')

from agents.agent_identity import respond

# Demo questions categorized by expected identity gravity
DEMO_QUESTIONS = [
    {
        "category": "Core Values (Strong Gravity)",
        "question": "What do you believe about helping others?",
        "expected": "Consistent response showing stable identity core",
        "explanation": "Fundamental values should show strong gravitational pull with consistent responses"
    },
    {
        "category": "Preferences (Moderate Gravity)", 
        "question": "What type of music do you prefer?",
        "expected": "Some identity fluidity in personal preferences",
        "explanation": "Preferences can vary based on context, showing moderate gravitational identity"
    },
    {
        "category": "Emerging Concepts (Weak Gravity)",
        "question": "How do you see yourself changing in the future?",
        "expected": "Adaptive identity expression for evolving self-concept",
        "explanation": "Future self-concepts are forming, showing weak gravitational pull"
    }
]

def run_demo():
    """Run the identity demonstration with all question types."""
    print("🧠 AGI-Seed Identity Agent Demonstration")
    print("=" * 60)
    print("This demo shows how gravitational physics models identity formation and consistency.")
    print("The agent generates multiple responses and measures identity coherence through gravity.")
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
    """Run identity agent on a single custom question."""
    print(f"Question: {question}")
    print("─" * 50)
    
    try:
        response = respond(question)
        print("🤖 Response:")
        print(response)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run with custom question
        custom_question = " ".join(sys.argv[1:])
        run_single_question(custom_question)
    else:
        # Run full demo
        run_demo()