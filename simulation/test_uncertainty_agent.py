import sys
sys.path.append('.')
from agents.uncertainty_agent import respond

print("Uncertainty Agent - Interactive Test")
print("Type 'quit' or 'exit' to end")
print("=" * 40)

while True:
    try:
        user_input = input(">> ")
        if user_input.lower() in ['quit', 'exit']:
            print("Goodbye!")
            break
        response = respond(user_input)
        print(response)
        print()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        break
    except Exception as e:
        print(f"Error: {e}")
        print()
