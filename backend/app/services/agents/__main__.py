"""
CLI smoke test for the agent system.

Run from project root with:
    cd backend && uv run python -m app.services.agents
"""

import json
import sys

from . import MarketFitOrchestrator
from .mock_data import EXAMPLES


def run_one(label: str, key: str) -> None:
    print(f"\n{'=' * 70}")
    print(f"  {label}  (fixture: {key})")
    print('=' * 70)
    report = MarketFitOrchestrator().analyze(EXAMPLES[key])

    # Print the public final report (skip the heavy per-agent payloads here).
    public = {k: v for k, v in report.items() if k != 'agentOutputs'}
    print(json.dumps(public, indent=2, ensure_ascii=False))


def main() -> int:
    selected = sys.argv[1:] if len(sys.argv) > 1 else list(EXAMPLES.keys())
    titles = {
        'arctic_jp': 'Arctic Sea Mineral Supplement -> Japan',
        'noodle_de': 'Instant Noodle Brand -> Germany',
        'protein_kr': 'Protein Bar -> South Korea',
    }
    for key in selected:
        if key not in EXAMPLES:
            print(f"Unknown example: {key}")
            continue
        run_one(titles.get(key, key), key)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
