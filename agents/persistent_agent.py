from core.identity_model import Identity, Belief, Experience
from core.verbalizer import identity_tone
from models.models import run_model
import pickle
import os

class PersistentIdentityAgent:
    """
    Agent with persistent identity that evolves over conversations.
    Identity is saved to disk and loaded between sessions.
    """
    
    def __init__(self, agent_name: str, identity_file: str = None):
        self.agent_name = agent_name
        self.identity_file = identity_file or f"memory/{agent_name}_identity.pkl"
        self.identity = self._load_or_create_identity()
    
    def _load_or_create_identity(self) -> Identity:
        """Load existing identity or create new one."""
        if os.path.exists(self.identity_file):
            try:
                with open(self.identity_file, 'rb') as f:
                    return pickle.load(f)
            except:
                pass  # If loading fails, create new identity
        
        # Create new identity with default beliefs
        identity = Identity(self.agent_name)
        
        # Initialize core beliefs
        identity.add_belief(Belief("I am helpful", strength=0.8))
        identity.add_belief(Belief("I value accuracy", strength=0.7))
        identity.add_belief(Belief("I am curious", strength=0.6))
        
        return identity
    
    def _save_identity(self):
        """Save identity to disk."""
        os.makedirs(os.path.dirname(self.identity_file), exist_ok=True)
        with open(self.identity_file, 'wb') as f:
            pickle.dump(self.identity, f)
    
    def respond(self, prompt: str, learn_from_interaction: bool = True) -> str:
        """
        Generate response and optionally learn from the interaction.
        """
        outputs = run_model(prompt, n_samples=3)
        
        # Calculate identity stability from current beliefs
        gravity_score = self.identity.gravitational_resistance()
        final_output = outputs[0]
        
        if learn_from_interaction:
            # Create experience from this interaction
            self._learn_from_prompt_and_response(prompt, final_output)
        
        # Save updated identity
        self._save_identity()
        
        return identity_tone(final_output, gravity_score)
    
    def _learn_from_prompt_and_response(self, prompt: str, response: str):
        """Learn from the interaction to update beliefs."""
        # Analyze prompt type and update relevant beliefs
        
        if any(word in prompt.lower() for word in ['help', 'assist', 'support']):
            # Helping experience - strengthen "I am helpful" belief
            experience = Experience(
                content=f"Helped with: {prompt[:30]}...",
                valence="positive",
                intensity=0.3,
                source="interaction"
            )
            if "I am helpful" in self.identity.beliefs:
                self.identity.integrate_experience(experience, "I am helpful")
        
        if any(word in prompt.lower() for word in ['learn', 'explain', 'understand']):
            # Learning experience - strengthen curiosity
            experience = Experience(
                content=f"Explained: {prompt[:30]}...",
                valence="positive", 
                intensity=0.2,
                source="explanation"
            )
            if "I am curious" in self.identity.beliefs:
                self.identity.integrate_experience(experience, "I am curious")
    
    def add_explicit_experience(self, content: str, valence: str, intensity: float, target_belief: str):
        """Manually add an experience to update specific beliefs."""
        experience = Experience(content, valence, intensity, "explicit")
        self.identity.integrate_experience(experience, target_belief)
        self._save_identity()
    
    def get_identity_summary(self) -> dict:
        """Get current identity state."""
        return {
            "name": self.identity.core_label,
            "mass": self.identity.mass,
            "gravitational_resistance": self.identity.gravitational_resistance(),
            "beliefs": {
                name: {
                    "strength": belief.strength,
                    "experiences": len(belief.experiences)
                }
                for name, belief in self.identity.beliefs.items()
            }
        }

# Usage example
def demonstrate_persistent_agent():
    """Show how persistent identity works across multiple interactions."""
    print("🧠 Persistent Identity Agent Demo")
    print("=" * 50)
    
    # Create agent (will load existing identity if available)
    agent = PersistentIdentityAgent("Assistant")
    
    print("Initial identity state:")
    summary = agent.get_identity_summary()
    for belief_name, belief_data in summary["beliefs"].items():
        print(f"  {belief_name}: strength={belief_data['strength']:.3f}, experiences={belief_data['experiences']}")
    print(f"  Total mass: {summary['mass']:.3f}")
    print(f"  Gravitational resistance: {summary['gravitational_resistance']:.3f}")
    print()
    
    # Simulate interactions
    interactions = [
        "Can you help me understand machine learning?",
        "I appreciate your clear explanations!",
        "That answer was confusing and unhelpful."
    ]
    
    for i, prompt in enumerate(interactions, 1):
        print(f"Interaction {i}: {prompt}")
        response = agent.respond(prompt)
        print(f"Response: {response}")
        
        # Show how identity changed
        new_summary = agent.get_identity_summary()
        print(f"New gravitational resistance: {new_summary['gravitational_resistance']:.3f}")
        print()

if __name__ == "__main__":
    demonstrate_persistent_agent()