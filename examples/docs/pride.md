# Pride Mechanism Documentation

## Overview

**STATUS: FULLY IMPLEMENTED ✅**

The pride mechanism models how AI agents experience pride when achieving goals that align with their aspirations and values. Unlike shame (triggered by violations), pride is triggered by accomplishments that meet or exceed internalized aspirational standards, with recognition amplifying the positive effect.

The system supports both **mandatory** (neurodivergent) and **optional** (neurotypical) aspiration integration styles, modeling different psychological approaches to identity-defining goals.

## Core Concepts

### 🎯 Pride Formula
```
pride_intensity = aspiration_strength × achievement_alignment × recognition_multiplier × pride_sensitivity
```

### 🏗️ Architecture Components

**Aspiration** → **PrideAction** → **SemanticAlignment** → **PrideEmotion**

- **Aspirations**: Positive standards the agent strives to meet or exceed (with integration styles)
- **PrideActions**: Agent achievements that can trigger pride (with recognition types)
- **SemanticAlignment**: Cosine similarity between achievement and aspiration vectors (0-1 scale)
- **PrideEmotion**: Resulting positive emotional state with belief strengthening and shame buffering

### 🧠 Integration Styles

**Mandatory Aspirations (Neurodivergent Style):**
- Identity-defining aspirations that must be met
- Low alignment triggers shame-like feedback
- Stronger pride boosts when exceeded
- More fragile to aspiration violations

**Optional Aspirations (Neurotypical Style):**
- Flexible aspirations that are "nice to have"
- Low alignment is tolerated without penalty
- Moderate pride when achieved
- Resilient to occasional misalignment

## Recognition Types and Multipliers

The system implements four recognition types with increasing amplification:

- **Self Recognition** (1.0x): Personal satisfaction from achievement
- **Peer Recognition** (1.5x): Recognition from equals or colleagues  
- **Public Recognition** (2.0x): Public acknowledgment or visibility
- **Authority Recognition** (2.5x): Recognition from respected authority figures

## Usage Examples

### Basic Pride Demonstration

```python
from psychological_systems.emotions.pride import PrideCapableIdentity, Aspiration, PrideAction

# Create agent with optional aspirations
agent = PrideCapableIdentity("CreativeBot", integration_style="optional")

# Add aspiration
creativity_aspiration = Aspiration(
    name="Artistic Expression",
    description="I strive to create beautiful art",
    domain_vector=[1.0, 0.3, 0.5, 0.2],  # [creativity, mastery, impact, recognition]
    strength=0.8,
    integration_style="optional"
)
agent.add_aspiration(creativity_aspiration)

# Achievement that aligns with aspiration
achievement = PrideAction(
    content="Created a beautiful painting",
    domain_vector=[0.9, 0.2, 0.4, 0.1],  # High creativity
    recognition_type="public"  # Public exhibition
)

# Process achievement
pride, alignments, effects = agent.achieve_action(achievement)
print(f"Pride intensity: {pride.intensity:.3f}")
print(f"Confidence boost: {pride.get_confidence_boost():.3f}")
```

### Integration Style Comparison

```python
# Neurotypical agent (optional aspirations)
nt_agent = PrideCapableIdentity("NeurotypicalBot", integration_style="optional")

# Neurodivergent agent (mandatory aspirations) 
nd_agent = PrideCapableIdentity("NeurodivergentBot", integration_style="mandatory")

# Same aspiration, different integration styles
for agent, name in [(nt_agent, "Neurotypical"), (nd_agent, "Neurodivergent")]:
    aspiration = Aspiration(
        name="Technical Excellence",
        description="Excel at technical skills",
        domain_vector=[0.2, 1.0, 0.6, 0.3],
        strength=0.8,
        integration_style=agent.integration_style
    )
    agent.add_aspiration(aspiration)
    
    # Test poorly aligned action
    poor_action = PrideAction(
        content="Made casual mistake",
        domain_vector=[0.1, 0.2, 0.1, 0.0],  # Low technical skill
        recognition_type="self"
    )
    
    pride, alignments, effects = agent.achieve_action(poor_action)
    print(f"{name}: {effects}")
    # Neurotypical: No penalty for poor alignment
    # Neurodivergent: "Shame feedback for mandatory aspiration"
```

## Proposed Structure

### Aspiration Example
```python
aspiration = Aspiration(
    name="Excel in Problem Solving",
    description="I strive to solve complex problems elegantly",
    strength=0.9,
    achievement_threshold=0.7  # How much achievement triggers pride
)
```

### Achievement Recognition Levels
```python
# Private achievement (low recognition)
private_achievement = PrideAction("Solved difficult puzzle alone", recognition_level=0.1)

# Public achievement (high recognition)  
public_achievement = PrideAction("Won prestigious award", recognition_level=0.9)
```

### Pride Effects (Proposed)
```python
def get_belief_boost(self) -> float:
    return self.intensity * 0.1  # Up to 10% belief strengthening

def get_confidence_drive(self) -> float:
    return self.intensity * 0.8  # Confidence vs shame's avoidance
```

## Implementation Specifications Needed

### 1. **Aspiration Modeling**
- What categories of aspirations should agents have?
- How do aspirations relate to existing beliefs and standards?
- Should aspirations be hierarchical or flat?

### 2. **Achievement Detection**
- What keywords/patterns indicate achievements vs failures?
- How to distinguish self-achievements from external recognition?
- Should achievements be graded or binary?

### 3. **Recognition Mechanics** 
- How does recognition level get determined?
- Should recognition amplify linearly or exponentially?
- Different recognition sources: self, peers, authority, public?

### 4. **Pride Calculation**
- What's the exact formula for pride intensity?
- What thresholds determine when pride triggers?
- How should multiple aspiration alignments be handled?

### 5. **Behavioral Effects**
- How does pride modify future behavior?
- Should pride make agents more/less risk-taking?
- How does pride interact with existing identity systems?

### 6. **Integration Points**
- How does pride interact with shame mechanisms?
- Can agents experience both simultaneously?
- How does pride modify the emotion template system?

## Demonstration Scenarios (TBD)

Proposed demonstration scenarios:
1. **Achievement Pride**: Agent accomplishes difficult task, experiences pride
2. **Recognition Amplification**: Same achievement with different recognition levels
3. **Multiple Aspirations**: Achievement aligns with multiple aspirational goals
4. **Pride-Shame Interaction**: How pride and shame interact in complex scenarios
5. **Identity Integration**: How pride strengthens identity over time

## Integration with Existing Systems

### Identity System
- How pride affects gravitational resistance
- Whether pride creates "positive mass" vs shame's weakening
- Integration with elastic resilience and recovery

### Emotion Templates
- How pride template relates to existing pride emotion template
- Whether to replace or enhance existing pride detection
- Integration with fear, shame, comfort, loneliness systems

### Shame Mechanism
- Complementary or competing mechanisms?
- Can agent experience pride and shame about different aspects simultaneously?
- How they affect the same beliefs/aspirations differently

## Next Steps

1. **Define aspiration categories and structure**
2. **Specify achievement recognition mechanics** 
3. **Design pride calculation formula**
4. **Determine behavioral and identity effects**
5. **Create demonstration scenarios**
6. **Implement and test integration points**

---

**Ready for your specifications to transform this skeleton into a full pride mechanism!**