"""Claims & Regulatory Risk Agent — flags risky wording. Not legal advice."""

from .base import BaseAgent, market_context
from .types import AnalysisInput, AgentOutput, RiskFlag


# Phrases that frequently create regulatory or distributor friction.
# Mapping: phrase substring -> (level, issue, safer alternative)
RISKY_PHRASES = {
    'cures': ('red', 'Disease-cure claim — regulated in nearly every market.',
              'Supports normal function of …'),
    'prevents': ('red', 'Disease-prevention claim — regulated in nearly every market.',
                 'Contributes to …'),
    'treats': ('red', 'Medical-treatment claim — likely violates supplement / food regulations.',
               'Traditionally used to …'),
    'boost': ('yellow', 'Vague performance claim — substantiation often required.',
              'Contains X mg of … per serving'),
    'natural': ('yellow', 'Definition varies by market; may need substantiation.',
                'Specify the natural attribute (e.g. "no added preservatives")'),
    'detox': ('yellow', 'Often unsubstantiated; flagged by EU and several other regulators.',
              'Drop the claim or replace with a specific compositional fact'),
    'miracle': ('red', 'Superlative claim — fails standard regulatory thresholds.',
                'Remove. Use a specific, quantified attribute instead.'),
    'doctor recommended': ('yellow', 'Requires substantiation; "doctor-recommended" must be evidenced.',
                           'Cite the source or remove.'),
    'clinically proven': ('yellow', 'Strong claim; requires citable trial.',
                          'Reference a study or use "supports …"'),
    'fda approved': ('red', 'FDA does not "approve" supplements; this phrasing is non-compliant in the US.',
                     'Drop and rely on third-party verification + GMP'),
    'organic': ('yellow', 'Requires the relevant market certification (USDA, EU Bio, JAS).',
                'Carry only the certified mark in the relevant market.'),
}


class ClaimsSafetyAgent(BaseAgent):
    id = 'claimsSafety'
    label = 'Claims & Regulatory Risk Agent'

    def run(self, input: AnalysisInput) -> AgentOutput:
        ctx = market_context(input.get('target_market', ''))
        score = self.stable_score(input, lo=55, hi=90)

        # Scan claim list + product name for risky substrings.
        claims = input.get('claims_on_pack', []) or []
        name = input.get('product_name', '') or ''
        haystack = ' || '.join([name] + claims).lower()

        flags: list[RiskFlag] = []
        for phrase, (level, issue, alt) in RISKY_PHRASES.items():
            if phrase in haystack:
                # Find which claim it came from for the surfaced text
                source = next(
                    (c for c in claims if phrase in c.lower()),
                    name if phrase in name.lower() else phrase,
                )
                flags.append({
                    'level': level, 'phrase': source, 'issue': issue,
                    'suggested_alternative': alt,
                })

        # If nothing surfaced, surface a soft yellow generic flag so the agent
        # still produces useful output for a clean label.
        if not flags:
            flags.append({
                'level': 'green',
                'phrase': '(no risky phrases detected)',
                'issue': 'Claims read within typical thresholds for this market.',
                'suggested_alternative': None,
            })

        findings = [
            f"{f['level'].upper()} · {f['phrase']} — {f['issue']}"
            for f in flags[:5]
        ]
        recommendations = [
            f"Reword '{f['phrase']}' → '{f['suggested_alternative']}'"
            for f in flags if f.get('suggested_alternative')
        ][:5]

        # If we found any red flags, drop the score a bit further.
        red_count = sum(1 for f in flags if f.get('level') == 'red')
        score = max(20, score - red_count * 12)

        return {
            'agent': self.id,
            'score': score,
            'findings': findings,
            'recommendations': recommendations,
            'detail': {
                'flags': flags,
                'note': 'Risk signals only — verify with regulatory counsel in the target market.',
            },
        }
