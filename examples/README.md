# 🧠 AGI-Seed Examples

Quick demonstrations of the psychological systems for emotionally grounded AI agents.

## 🚀 Quick Commands

### Identity System
```bash
python examples/demo_identity.py --model    # Core identity physics + emotions
python examples/demo_identity.py "How do you handle criticism?"
```

### Shame Mechanism  
```bash
python examples/demo_shame.py              # Basic shame demo
python examples/demo_shame.py --comprehensive  # Multiple scenarios
```

### Pride Mechanism
```bash
python examples/demo_pride.py              # Full neurodivergent/neurotypical comparison
python examples/demo_pride.py --basic      # Simple pride demonstration
python examples/demo_pride.py --comparison # Integration style comparison
```

### Dual Emotion System
```bash
python examples/demo_dual_emotion.py       # MentorBot experiencing pride and shame
python examples/demo_dual_emotion.py --scenario quick    # Simple dual emotion test
python examples/demo_dual_emotion.py --no-color         # Text-only output
```

### Emotion Templates
```bash
python -m psychological_systems.emotions.templates
```

### Uncertainty Agent
```bash
python examples/demo_questions.py          # Requires OpenAI API key
python examples/demo_questions.py "What is consciousness?"
```

## 📚 Detailed Documentation

Each system has focused documentation with theory, usage examples, and observable behavior:

- **[Identity System](docs/identity.md)** - Gravitational identity physics with realistic human psychology
- **[Shame Mechanism](docs/shame.md)** - Advanced shame modeling with internalized standards  
- **[Pride Mechanism](docs/pride.md)** - Achievement-based pride with neurodivergent/neurotypical styles
- **[Emotion Templates](docs/emotions.md)** - Fear, shame, comfort, pride, loneliness framework
- **[Uncertainty System](docs/uncertainty.md)** - AI uncertainty measurement and expression

## 🎯 What Each System Demonstrates

### Identity System
- **Realistic scaling**: Normal experiences cause tiny changes, trauma causes larger shifts
- **Loss aversion**: Negative experiences have 2x impact of positive ones
- **Elastic resilience**: Recovery toward baseline over time
- **Human-scale psychology**: Experience weighting with diminishing returns

### Shame Mechanism  
- **Standard violations**: Actions contradicting internalized standards trigger shame
- **Social amplification**: Public exposure amplifies shame significantly
- **Belief damage**: Shame reduces violated belief strength and creates avoidance drive
- **Semantic dissonance**: Vector-based contradiction measurement

### Pride Mechanism
- **Aspiration alignment**: Achievements matching aspirations trigger pride
- **Integration styles**: Mandatory (neurodivergent) vs optional (neurotypical) aspiration handling
- **Recognition amplification**: Self < peer < public < authority recognition multipliers
- **Belief strengthening**: Pride reinforces related beliefs and buffers shame effects

### Dual Emotion System
- **Simultaneous emotions**: Agents experience both pride and shame from single actions
- **Emotional interactions**: Pride buffers shame effects, complex psychological states
- **Realistic scenarios**: MentorBot simulation with encouragement, conflict, and redemption
- **Color-coded output**: Visual representation of emotional states and intensity

### Emotion Templates
- **Multi-emotion detection**: Fear, shame, comfort, pride, loneliness triggering
- **Realistic decay**: Emotions persist then fade over time
- **Framework ready**: Structure for adding behavioral principles
- **Integration points**: Works with identity system

### Uncertainty System
- **Response variance**: Measures AI confidence through consistency
- **Transparency**: Honest admission of knowledge limitations
- **Question sensitivity**: Different question types show different uncertainty patterns
- **AI safety focus**: Prevents dangerous overconfidence

## 🧪 Research Applications

These systems demonstrate:
- **Authentic emotions**: AI experiences emotions based on psychological principles
- **Measurable states**: Quantifiable identity resistance, shame intensity, uncertainty levels
- **Human-like biases**: Loss aversion, social sensitivity, cognitive patterns
- **Transparent AI**: Honest emotional expression and knowledge limitations
- **Modular design**: Systems can be combined for complex psychological modeling
- **Dual emotion processing**: Realistic emotional complexity with simultaneous pride/shame states

## 🔧 Technical Notes

- **Core systems work without API key** (identity, shame, emotions)
- **Uncertainty agent requires OpenAI API key** for response generation
- **Python 3.8+** recommended
- **See system docs** for detailed implementation and theory

---

For comprehensive implementation details, theoretical background, and advanced usage examples, see the individual system documentation linked above.