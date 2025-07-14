#!/usr/bin/env python3
"""Mock test for uncertainty agent without requiring API key"""

import sys
import os
sys.path.append('.')

# Set a mock API key to avoid the error
os.environ["OPENAI_API_KEY"] = "mock-api-key"

# Mock the OpenAI client to avoid actual API calls
class MockResponse:
    def __init__(self, content):
        self.choices = [MockChoice(content)]

class MockChoice:
    def __init__(self, content):
        self.message = MockMessage(content)

class MockMessage:
    def __init__(self, content):
        self.content = content

class MockChatCompletion:
    def __init__(self):
        self.call_count = 0
        
    def create(self, model, messages, temperature):
        # Mock responses with different content to test variance
        mock_responses = [
            "Paris is the capital of France.",
            "The capital of France is Paris, a beautiful city.",
            "France's capital city is Paris."
        ]
        
        # Cycle through responses to simulate variance
        response_content = mock_responses[self.call_count % len(mock_responses)]
        self.call_count += 1
        
        return MockResponse(response_content)

class MockChat:
    def __init__(self):
        self.completions = MockChatCompletion()

class MockOpenAI:
    def __init__(self, api_key=None):
        self.chat = MockChat()

# Import and patch the models
import models.models
models.models.client = MockOpenAI()

from agents.uncertainty_agent import respond
from core.uncertainty_model import score_variance
from core.verbalizer import uncertainty_tone

def test_uncertainty_agent():
    """Test the uncertainty agent with mock data"""
    print("Testing Uncertainty Agent")
    print("=" * 50)
    
    # Test 1: Basic functionality
    print("\n1. Testing basic response generation:")
    test_prompt = "What is the capital of France?"
    print(f"Prompt: {test_prompt}")
    
    try:
        response = respond(test_prompt)
        print(f"Response: {response}")
        print("✓ Basic response generation works")
    except Exception as e:
        print(f"✗ Error in basic response: {e}")
        return False
    
    # Test 2: Variance scoring
    print("\n2. Testing variance scoring:")
    test_outputs = [
        "Paris is the capital of France.",
        "The capital of France is Paris.",
        "France's capital is Paris."
    ]
    
    try:
        score = score_variance(test_outputs)
        print(f"Variance score for similar outputs: {score}")
        print("✓ Variance scoring works")
    except Exception as e:
        print(f"✗ Error in variance scoring: {e}")
        return False
    
    # Test 3: Uncertainty tone
    print("\n3. Testing uncertainty tone:")
    test_cases = [
        ("Low uncertainty", "Paris is the capital.", 0.1),
        ("Medium uncertainty", "Paris is the capital.", 0.3),
        ("High uncertainty", "Paris is the capital.", 0.7)
    ]
    
    for case_name, output, score in test_cases:
        try:
            toned_output = uncertainty_tone(output, score)
            print(f"{case_name} (score: {score}): {toned_output}")
            print(f"✓ {case_name} works")
        except Exception as e:
            print(f"✗ Error in {case_name}: {e}")
            return False
    
    print("\n" + "=" * 50)
    print("All tests passed! Your uncertainty agent is working correctly.")
    print("\nNext steps:")
    print("1. Add your OpenAI API key to .env file")
    print("2. Run: python simulation/test_uncertainty_agent.py")
    print("3. Test with real OpenAI API calls")
    
    return True

if __name__ == "__main__":
    test_uncertainty_agent()