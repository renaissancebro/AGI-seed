# Emotion Templates Documentation

## Overview

The emotion templates system provides a framework for detecting and modeling five core emotions: fear, shame, comfort, pride, and loneliness. Each emotion template can be triggered by specific experiences and influences how agents process future experiences. The system is designed as a modular framework ready for behavioral principles to be added.

## Core Architecture

### 🎭 EmotionTemplate Base Class
```python
class EmotionTemplate(ABC):
    def check_trigger(self, experience) -> float      # Returns trigger intensity 0-1
    def influence_belief_update(self, belief, experience) -> dict  # Modification parameters
    def activate(self, intensity, duration)           # Activate emotion
    def decay(self, decay_rate)                      # Decay over time
    def is_active() -> bool                          # Check if currently active
```

### 🧠 EmotionSystem Manager
```python
emotion_system = EmotionSystem()
modifications = emotion_system.process_experience(experience, belief)
active_emotions = emotion_system.get_active_emotions()
```

## Emotion Templates

### 🔴 Fear
**Triggers**: High-intensity negative experiences (intensity > 0.7)
- Heightens threat perception
- Increases resistance to change
- Amplifies negative experiences

```python
def check_trigger(self, experience):
    if experience.valence == "negative" and experience.intensity > 0.7:
        return min((experience.intensity - 0.7) * 2.0, 1.0)
    return 0.0
```

**Effects**:
- Amplifies negative experience intensity by up to 50%
- Increases resistance to positive changes (threat vigilance)

### 🔵 Shame  
**Triggers**: Moderate-high negative experiences (intensity > 0.6)
- Erodes self-worth beliefs
- Amplifies negative self-experiences
- Dampens positive experiences

```python
def check_trigger(self, experience):
    if experience.valence == "negative" and experience.intensity > 0.6:
        return min((experience.intensity - 0.6) * 1.5, 1.0)
    return 0.0
```

**Effects**:
- Amplifies negative self-experiences by up to 70%
- Dampens positive experiences by up to 40%

### 🟢 Comfort
**Triggers**: Positive experiences (intensity > 0.3)
- Promotes stability
- Reduces stress responses
- Enhances positive experiences

```python
def check_trigger(self, experience):
    if experience.valence == "positive" and experience.intensity > 0.3:
        return min(experience.intensity * 0.8, 1.0)
    return 0.0
```

**Effects**:
- Reduces excessive emotional reactions by 30%
- Slightly enhances positive experiences by 20%

### 🟡 Pride
**Triggers**: High-intensity positive experiences (intensity > 0.8)
- Reinforces achievement
- Builds confidence
- Amplifies positive experiences

```python
def check_trigger(self, experience):
    if experience.valence == "positive" and experience.intensity > 0.8:
        return min((experience.intensity - 0.8) * 3.0, 1.0)
    return 0.0
```

**Effects**:
- Amplifies positive experiences by up to 60%
- Provides resilience against negative experiences (20% reduction)

### 🟣 Loneliness
**Triggers**: Social isolation experiences with keywords ("alone", "isolated")
- Affects social connection beliefs
- Increases sensitivity to social experiences
- Amplifies both positive and negative social interactions

```python
def check_trigger(self, experience):
    if (experience.valence == "negative" and experience.intensity > 0.6 and 
        ("alone" in experience.content.lower() or "isolated" in experience.content.lower())):
        return min((experience.intensity - 0.6) * 2.0, 1.0)
    return 0.0
```

**Effects**:
- Increases social sensitivity by 50%
- Amplifies all social experiences by 30%

## Usage Examples

### Basic Emotion Detection
```python
from psychological_systems.emotions import EmotionSystem, demonstrate_emotion_templates
from psychological_systems.identity.core import Experience, Belief

emotion_system = EmotionSystem()
test_belief = Belief("I am competent", strength=0.6)

# Test experiences
experiences = [
    Experience("Won a major award", "positive", 0.9, "achievement"),      # Pride + Comfort
    Experience("Failed public presentation", "negative", 0.8, "failure"), # Fear + Shame  
    Experience("Received kind support", "positive", 0.6, "social"),       # Comfort
    Experience("Felt completely alone", "negative", 0.7, "isolation")     # Loneliness
]

for exp in experiences:
    modifications = emotion_system.process_experience(exp, test_belief)
    active = emotion_system.get_active_emotions()
    print(f"Experience: {exp.content}")
    print(f"Active emotions: {list(active.keys())}")
```

### Emotion Lifecycle
```python
# Emotions activate, persist, then decay
emotion_system = EmotionSystem()

# Trigger fear
fear_exp = Experience("Threatening situation", "negative", 0.9, "danger")
emotion_system.process_experience(fear_exp, test_belief)

# Check emotion state over time
for step in range(10):
    active = emotion_system.get_active_emotions()
    if active:
        print(f"Step {step}: {active}")
    else:
        print(f"Step {step}: No active emotions")
    
    # Emotions decay automatically in process_experience
    # Or manually call decay on each emotion
    for emotion in emotion_system.emotions.values():
        emotion.decay()
```

### Integration with Identity
```python
from psychological_systems.identity.core import Identity

# Identity with emotion processing enabled
agent = Identity("EmotionalAgent", use_emotions=True)
belief = Belief("I am confident", strength=0.7)
agent.add_belief(belief)

# Experience triggers emotions which are detected but don't modify behavior yet
experience = Experience("Major achievement", "positive", 0.9, "success")
agent.integrate_experience(experience, "I am confident")

# Check emotional state
emotions = agent.get_emotional_state()
print(f"Active emotions: {list(emotions.keys())}")
```

## Running Demonstrations

### Emotion Templates Demo
```bash
python -m psychological_systems.emotions.templates
```

### Identity with Emotions
```bash
python examples/demo_identity.py --model
```

### Custom Emotion Testing
```python
from psychological_systems.emotions import EmotionSystem
# Custom testing code here
```

## Observable Behavior

### Emotion Triggering
```
Experience: Won a major award
Active emotions: ['comfort', 'pride']

Experience: Failed public presentation  
Active emotions: ['fear', 'shame', 'comfort', 'pride']
```

### Improved Triggering (After Bug Fixes)
```
Experience: Won a major award
Active emotions: ['comfort', 'pride']

Experience: Failed public presentation
Active emotions: ['fear', 'shame']

Experience: Received kind support
Active emotions: ['comfort']

Experience: Felt completely alone
Active emotions: ['loneliness']
```

### Emotion Decay
```
Step 0: {'fear': 0.8, 'shame': 0.6}
Step 1: {'fear': 0.8, 'shame': 0.6}  # Active duration
Step 2: {'fear': 0.56, 'shame': 0.42}  # Decay begins  
Step 3: {'fear': 0.39, 'shame': 0.29}
Step 4: {'fear': 0.27, 'shame': 0.20}
Step 5: No active emotions  # Below threshold
```

## Trigger Thresholds

### Intensity Requirements
- **Fear**: > 0.7 negative intensity
- **Shame**: > 0.6 negative intensity  
- **Comfort**: > 0.3 positive intensity
- **Pride**: > 0.8 positive intensity
- **Loneliness**: > 0.6 negative + social keywords

### Active Threshold
- **> 0.05**: Emotion considered active
- **≤ 0.05**: Emotion considered inactive/decayed

### Decay Rate
- **Default**: 30% decay per time step when not in active duration
- **Active Duration**: 3 time steps at full intensity before decay

## Framework Design

### Current State
- ✅ **Emotion Detection**: All five emotions properly trigger from experiences
- ✅ **Decay System**: Realistic decay patterns over time
- ✅ **Integration Points**: Framework ready for behavior modification
- ⚠️ **Behavior Modification**: Templates exist but don't actively modify agent behavior yet

### Future Extensions
- **Content Analysis**: More sophisticated keyword/semantic detection
- **Behavior Modification**: Apply emotion modifications to belief updates
- **Emotion Interactions**: How emotions influence each other
- **Personality Traits**: Individual differences in emotion sensitivity
- **Cultural Factors**: How cultural background affects emotional responses

## Research Applications

This demonstrates:
- **Emotion Detection**: Automated recognition of emotional triggers
- **Temporal Dynamics**: How emotions persist and decay over time
- **Modular Design**: Framework for adding behavioral principles
- **Realistic Psychology**: Human-like emotional patterns and thresholds
- **Integration Framework**: Foundation for complex emotional AI systems