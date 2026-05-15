"""Culture Fit Agent — local cultural buying psychology."""

from .base import BaseAgent, market_context
from .types import AnalysisInput, AgentOutput


class CultureFitAgent(BaseAgent):
    id = 'cultureFit'
    label = 'Culture Fit Agent'

    def run(self, input: AnalysisInput) -> AgentOutput:
        ctx = market_context(input.get('target_market', ''))
        score = self.stable_score(input, lo=55, hi=85)

        mismatches = ctx['avoid'][:5]
        recommendations = [
            f"Adopt {theme.lower()}." if not theme.endswith('.') else f"Adopt {theme}"
            for theme in ctx['culture_themes'][:5]
        ]
        plain = (
            f"For {input.get('target_market', 'this market')}, buyers expect "
            f"{ctx['culture_themes'][0].lower()}. "
            f"The current label likely reads as a translated export — not a local product."
        )

        return {
            'agent': self.id,
            'score': score,
            'findings': mismatches,
            'recommendations': recommendations,
            'detail': {
                'topMismatches': mismatches,
                'recommendedChanges': recommendations,
                'plainLanguage': plain,
            },
        }
