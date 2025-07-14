from core.identity_model import Identity, Belief, Experience
from core.verbalizer import identity_tone
from models.models import run_model
import json
import os
from datetime import datetime

class ConversationalIdentityAgent:
    """
    Agent that builds identity through conversational history.
    Learns about itself through user interactions and feedback.
    """
    
    def __init__(self, agent_name: str, conversation_file: str = None):
        self.agent_name = agent_name
        self.conversation_file = conversation_file or f"memory/{agent_name}_conversations.json"
        self.identity = Identity(agent_name)
        self.conversation_history = []
        
        # Initialize with basic beliefs
        self.identity.add_belief(Belief("I communicate clearly", strength=0.5))
        self.identity.add_belief(Belief("I understand users", strength=0.5))
        self.identity.add_belief(Belief("I am knowledgeable", strength=0.5))
        
        self._load_conversation_history()
        self._rebuild_identity_from_history()
    
    def _load_conversation_history(self):
        """Load previous conversation history."""
        if os.path.exists(self.conversation_file):
            try:
                with open(self.conversation_file, 'r') as f:
                    self.conversation_history = json.load(f)
            except:
                self.conversation_history = []
    
    def _save_conversation(self, interaction: dict):
        """Save conversation to history."""
        self.conversation_history.append(interaction)
        os.makedirs(os.path.dirname(self.conversation_file), exist_ok=True)
        with open(self.conversation_file, 'w') as f:
            json.dump(self.conversation_history, f, indent=2)
    
    def _rebuild_identity_from_history(self):
        """Rebuild identity from conversation history."""
        for interaction in self.conversation_history:
            if 'user_feedback' in interaction:
                self._process_feedback(interaction['user_feedback'])
    
    def respond(self, prompt: str, user_id: str = "user") -> str:
        """Generate response and learn from interaction."""
        outputs = run_model(prompt, n_samples=3)
        gravity_score = self.identity.gravitational_resistance()
        final_output = outputs[0]
        
        # Save interaction
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "prompt": prompt,
            "response": final_output,
            "identity_state": {
                "mass": self.identity.mass,
                "resistance": gravity_score
            }
        }
        self._save_conversation(interaction)
        
        return identity_tone(final_output, gravity_score)
    
    def receive_feedback(self, feedback: str, feedback_type: str = "general"):
        """
        Process user feedback to update identity.
        
        feedback_type: 'positive', 'negative', 'clarity', 'knowledge', etc.
        """
        # Determine which belief to update based on feedback
        belief_mapping = {
            'clarity': 'I communicate clearly',
            'understanding': 'I understand users', 
            'knowledge': 'I am knowledgeable',
            'general': 'I communicate clearly'  # default
        }
        
        target_belief = belief_mapping.get(feedback_type, 'I communicate clearly')
        
        # Analyze sentiment of feedback
        positive_words = ['good', 'great', 'helpful', 'clear', 'excellent', 'perfect']
        negative_words = ['bad', 'unclear', 'confusing', 'wrong', 'unhelpful', 'terrible']
        
        positive_score = sum(1 for word in positive_words if word in feedback.lower())
        negative_score = sum(1 for word in negative_words if word in feedback.lower())
        
        if positive_score > negative_score:
            valence = "positive"
            intensity = min(positive_score / 3.0, 1.0)
        elif negative_score > positive_score:
            valence = "negative"
            intensity = min(negative_score / 3.0, 1.0)
        else:
            valence = "positive"
            intensity = 0.1  # neutral feedback is slightly positive
        
        # Create experience from feedback
        experience = Experience(
            content=feedback,
            valence=valence,
            intensity=intensity,
            source="user_feedback"
        )
        
        # Update identity
        if target_belief in self.identity.beliefs:
            self.identity.integrate_experience(experience, target_belief)
        
        # Save feedback to conversation history
        if self.conversation_history:
            self.conversation_history[-1]['user_feedback'] = {
                'feedback': feedback,
                'type': feedback_type,
                'processed_valence': valence,
                'processed_intensity': intensity
            }
            self._save_conversation_history()
    
    def _save_conversation_history(self):
        """Save updated conversation history."""
        os.makedirs(os.path.dirname(self.conversation_file), exist_ok=True)
        with open(self.conversation_file, 'w') as f:
            json.dump(self.conversation_history, f, indent=2)
    
    def _process_feedback(self, feedback_data: dict):
        """Process historical feedback to rebuild identity."""
        experience = Experience(
            content=feedback_data['feedback'],
            valence=feedback_data['processed_valence'],
            intensity=feedback_data['processed_intensity'],
            source="historical_feedback"
        )
        
        # Map feedback type to belief
        belief_mapping = {
            'clarity': 'I communicate clearly',
            'understanding': 'I understand users',
            'knowledge': 'I am knowledgeable',
            'general': 'I communicate clearly'
        }
        
        target_belief = belief_mapping.get(feedback_data['type'], 'I communicate clearly')
        if target_belief in self.identity.beliefs:
            self.identity.integrate_experience(experience, target_belief)
    
    def get_conversation_stats(self) -> dict:
        """Get statistics about conversation history and identity evolution."""
        feedback_count = sum(1 for conv in self.conversation_history if 'user_feedback' in conv)
        
        return {
            "total_conversations": len(self.conversation_history),
            "feedback_received": feedback_count,
            "identity_summary": {
                "mass": self.identity.mass,
                "resistance": self.identity.gravitational_resistance(),
                "beliefs": {
                    name: {
                        "strength": belief.strength,
                        "experiences": len(belief.experiences)
                    }
                    for name, belief in self.identity.beliefs.items()
                }
            }
        }

# Usage example
def demonstrate_conversational_agent():
    """Show how conversational identity builds over time."""
    print("🧠 Conversational Identity Agent Demo")
    print("=" * 50)
    
    agent = ConversationalIdentityAgent("ChatBot")
    
    # Simulate conversation with feedback
    print("1. Initial interaction:")
    response1 = agent.respond("Explain quantum computing", "user1")
    print(f"Response: {response1}")
    
    print("\n2. User gives positive feedback:")
    agent.receive_feedback("That was very clear and helpful!", "clarity")
    
    print("\n3. Another interaction:")
    response2 = agent.respond("How does machine learning work?", "user1") 
    print(f"Response: {response2}")
    
    print("\n4. User gives negative feedback:")
    agent.receive_feedback("That was confusing and too technical", "clarity")
    
    print("\n5. Final interaction:")
    response3 = agent.respond("What is Python?", "user1")
    print(f"Response: {response3}")
    
    # Show stats
    stats = agent.get_conversation_stats()
    print(f"\nConversation Stats:")
    print(f"  Total conversations: {stats['total_conversations']}")
    print(f"  Feedback received: {stats['feedback_received']}")
    print(f"  Current identity mass: {stats['identity_summary']['mass']:.3f}")
    print(f"  Gravitational resistance: {stats['identity_summary']['resistance']:.3f}")
    
    for belief_name, belief_data in stats['identity_summary']['beliefs'].items():
        print(f"  {belief_name}: {belief_data['strength']:.3f} (from {belief_data['experiences']} experiences)")

if __name__ == "__main__":
    demonstrate_conversational_agent()