<div align="center">

# ORAMA INTEL

### Predict Anything

A next-generation AI prediction engine powered by multi-agent swarm intelligence.

Upload any document. Describe what you want to predict. Get a detailed simulation report.

---

</div>

## What It Does

**ORAMA INTEL** transforms unstructured data into predictive simulations. It extracts "reality seeds" from your documents, builds a digital parallel world populated by thousands of AI agents, and simulates outcomes — giving you a rehearsal of the future.

**Input:** Upload documents (reports, articles, data) + describe your prediction goal in natural language

**Output:** A detailed prediction report + an interactive digital world you can explore

## How It Works

1. **Graph Build** — Extracts entities and relationships, builds a knowledge graph
2. **Environment Setup** — Generates agent personas with independent personalities and memory
3. **Simulation** — Agents interact and evolve across multiple rounds
4. **Report** — AI analyzes simulation results into actionable predictions
5. **Interaction** — Chat with any simulated agent or the report AI

## Quick Start

### Prerequisites
- Node.js >= 18
- Python >= 3.11
- [UV](https://docs.astral.sh/uv/) (Python package manager)

### Setup

```bash
# Install all dependencies
npm run setup:all

# Copy env and add your API keys
cp .env.example .env
```

### Required API Keys

| Key | Where to get it | Cost |
|-----|----------------|------|
| `LLM_API_KEY` | [OpenAI](https://platform.openai.com/api-keys) | Pay-per-use |
| `ZEP_API_KEY` | [Zep Cloud](https://app.getzep.com/) | Free tier available |

### Run

```bash
npm run dev
```

Frontend: http://localhost:3000
Backend: http://localhost:5001

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vue 3, Vite, D3.js, Vue Router |
| Backend | Flask, Python 3.11+ |
| AI/LLM | OpenAI-compatible APIs |
| Memory | Zep Cloud (knowledge graphs) |
| Simulation | CAMEL OASIS (multi-agent) |

## License

AGPL-3.0
