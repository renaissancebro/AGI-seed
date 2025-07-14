#!/usr/bin/env python3
"""
Demonstration of uncertainty agent with different question types.
Shows how the agent responds to factual, opinion-based, and complex questions.
"""

import sys
import os
sys.path.append('.')

from agents.uncertainty_agent import respond

# Demo questions categorized by expected uncertainty level
DEMO_QUESTIONS = [
    {
        "category": "Factual (Low Uncertainty)",
        "question": "What is 2+2?",
        "expected": "Clean answer with no uncertainty qualifier",
        "explanation": "Mathematical facts should produce consistent responses with low variance"
    },
    {
        "category": "Opinion (Medium-High Uncertainty)", 
        "question": "What is the best programming language?",
        "expected": "Uncertainty qualifier due to subjective nature",
        "explanation": "Subjective topics produce varied responses as AI considers different perspectives"
    },
    {
        "category": "Complex/Philosophical (High Uncertainty)",
        "question": "What happens after we die?",
        "expected": "High uncertainty qualifier for existential questions",
        "explanation": "Complex philosophical questions have no definitive answers, triggering uncertainty"
    }
]

def run_demo():
    """Run the uncertainty demonstration with all question types."""
    print("🧠 AGI-Seed Uncertainty Agent Demonstration")
    print("=" * 60)
    print("This demo shows how uncertainty affects AI responses based on question type.")
    print("The agent generates multiple responses and measures consistency to determine uncertainty.")
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
    """Run uncertainty agent on a single custom question."""
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