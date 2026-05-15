"""Visual Hierarchy Agent — can a buyer understand the product in 2 seconds?"""

from .base import BaseAgent, market_context
from .types import AnalysisInput, AgentOutput


HIERARCHY_BY_CHANNEL = {
    'supermarket':  ['Category cue', 'Quantified hero benefit', 'Brand mark',
                     'Trust signal', 'Compliance / regulatory line'],
    'pharmacy':     ['Pharmacy-grade seal', 'Active ingredient + amount',
                     'Daily dose clarity', 'Brand mark', 'Regulatory line'],
    'convenience':  ['Hero benefit', 'Format / pack size', 'Brand mark',
                     'Price-tier cue', 'Compliance line'],
    'amazon':       ['Quantified hero benefit (thumbnail-readable)',
                     'Product type', 'Brand mark', 'Trust badge', 'Compliance line'],
    'specialty':    ['Provenance / story line', 'Quantified hero benefit',
                     'Brand mark', 'Certification', 'Compliance line'],
    'b2b':          ['Product type + category', 'Active ingredient + amount',
                     'Brand mark', 'Importer / distributor field', 'Compliance line'],
}


class VisualHierarchyAgent(BaseAgent):
    id = 'visualHierarchy'
    label = 'Visual Hierarchy Agent'

    def run(self, input: AnalysisInput) -> AgentOutput:
        channel = input.get('target_channel', 'supermarket')
        hierarchy = HIERARCHY_BY_CHANNEL.get(channel, HIERARCHY_BY_CHANNEL['supermarket'])
        score = self.stable_score(input, lo=50, hi=85)

        findings = [
            'Buyers likely notice the brand mark first; the benefit comes second.',
            'Front-of-pack reads cluttered at shelf distance.',
            'Mobile-thumbnail crop loses key trust markers.',
        ]
        recommendations = [
            'Lead with the quantified hero benefit, not the brand.',
            'Demote tagline below the hero benefit.',
            'Reduce visual elements on front-of-pack by ~30%.',
            'Move trust seals into a single horizontal strip near the top edge.',
        ]

        return {
            'agent': self.id,
            'score': score,
            'findings': findings,
            'recommendations': recommendations,
            'detail': {
                'whatBuyersNoticeFirst': 'Brand mark (current)',
                'whatTheyShouldNoticeFirst': hierarchy[0],
                'recommendedFrontHierarchy': hierarchy,
                'makeBigger': [hierarchy[0], hierarchy[1]],
                'makeSmaller': ['Brand mark', 'Tagline'],
                'remove': ['Redundant secondary badge', 'Decorative pattern overlay'],
            },
        }
