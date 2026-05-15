"""Market Trend Agent — current category and consumer trends in the target market."""

from .base import BaseAgent, market_context
from .types import AnalysisInput, AgentOutput


CATEGORY_TRENDS = {
    'Supplement': {
        'relevant': ['Functional adaptogens', 'Quantified daily dose', 'Clean label simplicity',
                     'Personalized stacks', 'Third-party testing visibility'],
        'overused': ['Vague "wellness" stock photography', 'Generic green-leaf imagery',
                     'Unsubstantiated "boost" claims'],
    },
    'Food': {
        'relevant': ['Protein density', 'High-fiber signaling', 'Provenance and origin',
                     'Allergen transparency', 'Carbon footprint cues'],
        'overused': ['Cluttered "no-artificial" badges', 'Cartoon mascot reuse', 'Generic farm imagery'],
    },
    'Beverage': {
        'relevant': ['Functional infusion', 'Low/no sugar quantified', 'Local-source storytelling',
                     'Recyclable / refill formats', 'Adaptogenic positioning'],
        'overused': ['Tropical fruit photography', 'Generic energy-bolt iconography'],
    },
    'Private Label': {
        'relevant': ['Premium-tier private label', 'Origin transparency', 'Allergen visibility',
                     'Recyclable / clean packaging', 'Cleaner ingredient panels'],
        'overused': ['Generic "value" colorways', 'Identical packaging across SKUs'],
    },
}


class MarketTrendAgent(BaseAgent):
    id = 'trendFit'
    label = 'Market Trend Agent'

    def run(self, input: AnalysisInput) -> AgentOutput:
        ctx = market_context(input.get('target_market', ''))
        cat = input.get('product_category', 'Food')
        trends = CATEGORY_TRENDS.get(cat, CATEGORY_TRENDS['Food'])
        score = self.stable_score(input, lo=50, hi=85)

        relevant = trends['relevant'][:5]
        missing = relevant[:3]
        overused = trends['overused'][:3]

        # Lean on observed competitor patterns if available — these are
        # market-specific signals, not generic category lists.
        refs = input.get('marketReferences') or {}
        observed_overused = (refs.get('overusedPatterns') or [])[:3]
        if observed_overused:
            overused = observed_overused
        whitespace = (refs.get('whiteSpaceOpportunities') or [])[:2]
        if whitespace:
            relevant = whitespace + relevant
            missing = whitespace[:2] + missing[:1]

        positioning = (
            f"Position as {input.get('brand_goal', 'premium')} {cat.lower()} "
            f"leaning into: {', '.join(relevant[:2])}."
        )

        return {
            'agent': self.id,
            'score': score,
            'findings': [
                f"Relevant trend present: {relevant[0]}",
                f"Trend the label misses: {missing[1] if len(missing) > 1 else missing[0]}",
                f"Cliché to drop: {overused[0]}",
            ],
            'recommendations': [
                f"Lean into: {t}" for t in relevant[:3]
            ] + [f"Avoid: {t}" for t in overused],
            'detail': {
                'relevantTrends': relevant,
                'missingTrends': missing,
                'overusedTrends': overused,
                'recommendedPositioning': positioning,
            },
        }
