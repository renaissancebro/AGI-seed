# 🧠 Modeling Uncertainty as Osmosis

## 🌊 Overview

This doc maps the metaphor of **osmosis** — the movement of particles across a semi-permeable membrane — onto the behavior of **intelligent agents under uncertainty**.

Rather than treating uncertainty as a static probability, we model it as a **dynamic pressure gradient** that affects agent behavior, tone, and decision-making.

---

## 🔬 Osmosis vs. Decision Flow

| Osmosis Concept      | Agent Interpretation                         | Description |
|----------------------|-----------------------------------------------|-------------|
| Solute concentration | Option strength / confidence signal           | Each possible decision has a "weight" or pressure |
| Solvent              | Cognitive energy / processing effort          | The fluid that carries attention between options |
| Membrane             | Decision boundary (what enters action space)  | Filters between considered vs. chosen paths |
| Concentration gradient | Utility difference between options          | Drives agent toward one outcome — or creates tension |
| Equilibrium          | Indecision / internal stalemate               | When no option outweighs the others — agent may pause or hesitate |
| Osmotic pressure     | Force of "known good" pushing through doubt   | High-confidence → behavior passes membrane into action |
| Reverse osmosis      | Forcing action despite imbalance              | Overriding natural hesitation (e.g., with user prompt override) |

---

## 🧠 Core Metaphor:  
> *"In uncertain decisions, mental energy flows like solvent across options. The greater the imbalance, the stronger the push toward a choice. But if pressures are equal — the agent remains in tension."*

---

## 🔁 Behavioral Effects of the Osmosis Model

### 1. **Uncertainty as Pressure**

The agent doesn't "know" it is unsure. Instead, it:
- Detects variance in completions (multi-sample)
- Measures entropy of token probabilities
- Observes conflict in internal logic or external feedback

These become a **pressure score**:
- Low pressure differential = indecision
- High differential = fluid, confident action

---

### 2. **Membrane Behavior: Expression Gate**

Before an output leaves the agent:
- It’s passed through a **verbalization membrane**
- The tone adapts to the pressure:
  - High pressure (certainty) → clear, direct
  - Mid-pressure → hedged, cautious
  - Low pressure (ambiguous) → hesitant, exploratory

---

### 3. **Oscillation Between Choices**

In states of near-equal pressure, the agent may:
- Flip between options (oscillate)
- Verbally reflect indecision
- Request clarification to break tie
- Log tension for later resolution

This mirrors the **unstable flow between membranes** in equilibrium.

---

## 🧠 Emotional Mapping: Uncertainty as Emotion Primitive

Rather than treat uncertainty as just a score:

> We treat it as a **pre-emotional state** — a signal that affects tone, risk aversion, and even self-reflection.

This becomes:
- A scaffold for other emotions (fear, doubt, hesitation)
- A feedback loop that makes the agent *feel more alive and human*

---

## 🧪 Implementation Notes

- Uncertainty score can be derived from:
  - Token entropy
  - Embedding divergence across samples
  - Self-critique chains (“Does this contradict earlier beliefs?”)
- Output is passed through a **verbalizer**, which maps score → language
- Future: agent can remember previous uncertainty and adapt

---

## 🛠 Example System Flow

```text
[Prompt] → [LLM Completion x3] → [Entropy + Variance] → [Uncertainty Score]
     → [Verbalizer: adjust tone] → [Final Output]

---

## 🧪 Testing

### Mock Test (`test_mock_uncertainty.py`)
Comprehensive testing without requiring API keys:

**Components Tested:**
- **Basic Response Generation**: Verifies the complete pipeline from prompt to uncertainty-adjusted response
- **Variance Scoring**: Tests `score_variance()` function with sample outputs to ensure proper uncertainty quantification
- **Uncertainty Verbalization**: Validates `uncertainty_tone()` function across different confidence levels:
  - Low uncertainty (score < 0.2): Returns response without modification
  - Medium uncertainty (0.2-0.5): Adds "I believe this is likely, but not fully certain"
  - High uncertainty (> 0.5): Adds "This may be unreliable — here's my best attempt"

**Mock System**: Uses simulated OpenAI responses with controlled variance to test uncertainty detection without API costs.

### Interactive Tester (`simulation/test_uncertainty_agent.py`)
Real-time testing interface for live uncertainty assessment:

**Features:**
- **Interactive Prompt**: Continuous input loop with `>> ` prompt
- **Exit Commands**: Type `quit` or `exit` to end, or use Ctrl+C
- **Error Handling**: Graceful handling of API errors and connection issues
- **Real API Integration**: Uses actual OpenAI API calls to demonstrate uncertainty in real responses

**Usage:**
```bash
python simulation/test_uncertainty_agent.py
```

**What to Observe:**
- Response variance across multiple API calls
- Uncertainty qualifiers based on output consistency
- Different confidence levels for various types of questions (factual vs. subjective)
EOF < /dev/null