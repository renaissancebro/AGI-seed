# AGI-Seed

AGI-Seed is my starting point toward building emotionally grounded AI systems. It stems from a personal need: to understand myself and translate that awareness into tools that can make AI safer, more human-aligned, and harder to misuse.

This is a project about embedding emotional primitives — like uncertainty, shame, pride, and empathy — into models using realistic human-scale psychology. My belief is simple: if we can't model meaning and emotional behavior, we're building powerful tools blind to the real structure of human experience.

This repository implements sophisticated psychological systems including gravitational identity formation, emotion templates, and advanced shame mechanisms for authentic AI emotional expression.

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/renaissancebro/AGI-seed.git
cd AGI-seed
pip install -r requirements.txt

# Add your OpenAI API key to .env file (optional for core systems)
echo "OPENAI_API_KEY=your-key-here" > .env

# Try the psychological systems
python examples/demo_identity.py --model    # Identity & emotion templates
python examples/demo_shame.py              # Advanced shame mechanism
python examples/demo_pride.py              # Pride with neurodivergent/neurotypical styles
python examples/demo_questions.py          # Uncertainty agent (needs API key)
```

## 🧠 Psychological Systems

This repository implements **emotions as computational primitives** using physics-based metaphors and realistic human-scale psychology:

### ✅ Fully Implemented
- **[Identity as Gravitational Physics](examples/docs/identity.md)** - Beliefs create mass, experiences cause gravitational resistance to change
  - Loss aversion, elastic resilience, trauma thresholds, realistic scaling
- **[Advanced Shame Mechanism](examples/docs/shame.md)** - Violations of internalized standards trigger shame
  - Semantic dissonance, social exposure amplification, belief damage
- **[Pride Mechanism](examples/docs/pride.md)** - Achievement-based pride with neurodivergent/neurotypical integration styles
  - Mandatory vs optional aspirations, recognition amplification, shame buffering
- **[Emotion Templates](examples/docs/emotions.md)** - Fear, shame, comfort, pride, loneliness detection framework
- **[Uncertainty as AI Measurement](examples/docs/uncertainty.md)** - Response variance driving decision confidence

### 🧪 Integration Framework
- **Modular Architecture** - `psychological_systems/` with identity, emotions, uncertainty modules
- **Unified Agents** - Framework ready for combining multiple psychological primitives
- **Realistic Psychology** - Human-scale experience weighting, diminishing returns, recovery patterns

## 📁 Repository Structure

```
├── psychological_systems/    # Core psychological modeling
│   ├── identity/            # Gravitational identity physics
│   ├── emotions/            # Emotion templates & shame mechanism  
│   ├── uncertainty/         # AI uncertainty measurement
│   └── integration/         # Unified agent framework
├── examples/                # Demonstrations and focused docs
│   └── docs/               # Detailed system documentation
├── agents/                 # Legacy agents (uncertainty_agent)
├── core/                   # Legacy core systems
├── notes/                  # Research notes and theory
└── models/                 # AI model integrations
```

## 📚 Documentation

### System Documentation
- **[Identity System](examples/docs/identity.md)** - Gravitational identity physics with realistic human psychology
- **[Shame Mechanism](examples/docs/shame.md)** - Advanced shame modeling with internalized standards
- **[Emotion Templates](examples/docs/emotions.md)** - Fear, shame, comfort, pride, loneliness framework
- **[Uncertainty System](examples/docs/uncertainty.md)** - AI uncertainty measurement and expression

### Quick Reference
- **[Examples Overview](examples/README.md)** - Quick start commands and system overview
- **[Robustness Roadmap](notes/robustness_roadmap.md)** - Future improvements and research directions

## Vision

- Build emotionally grounded AI systems using realistic human-scale psychology
- Develop modular psychological primitives that can be combined for complex emotional behavior
- Create AI that experiences emotions authentically rather than simulating them superficially
- Enable transparent emotional decision-making through measurable psychological states
- Advance AI alignment through embodied emotional understanding and human-like cognitive biases

## Credit & Origin

This project is created and maintained by [Josh Freeman](https://www.linkedin.com/in/josh-freeman/). It is the starting point of an open emotional modeling framework. All commits are timestamped. Feel free to fork and build — just cite the origin.
