"""Export Readiness Agent — distributor / retailer / cross-border readiness."""

from .base import BaseAgent, market_context
from .types import AnalysisInput, AgentOutput


REQUIRED_FIELDS_BY_MARKET = {
    'Japan':        ['Japanese ingredient list', 'Importer field', 'Manufacturing origin', 'Allergen panel (Japanese)'],
    'South Korea':  ['Korean ingredient list', 'Importer field', 'KCA-style nutrition panel', 'Allergen panel'],
    'Germany':      ['German ingredient list', 'EU nutrition declaration', 'EU allergen formatting',
                     'Best-before / batch placement'],
    'EU':           ['Multi-language ingredient list', 'EU nutrition declaration',
                     'EU allergen formatting', 'EU importer / distributor field'],
    'Nordics':      ['Nordic-language ingredient list (NO/SE/DK as relevant)', 'EU nutrition declaration',
                     'EU allergen formatting', 'Sustainability / origin claim citation'],
    'USA':          ['US nutrition facts panel', 'FDA-compliant supplement disclaimer',
                     'Common-name ingredient list', 'Country-of-origin'],
}


class ExportReadinessAgent(BaseAgent):
    id = 'exportReadiness'
    label = 'Export Readiness Agent'

    def run(self, input: AnalysisInput) -> AgentOutput:
        tm = input.get('target_market', '')
        required = REQUIRED_FIELDS_BY_MARKET.get(tm, [
            'Local-language ingredient list', 'Importer / distributor field',
            'Local nutrition panel', 'Allergen visibility',
        ])
        score = self.stable_score(input, lo=50, hi=85)

        findings = [
            f"Required for {tm}: {required[0]}",
            'Distributor field is missing or placeholder.',
            'Batch / shelf-life format is not consistent with target market norms.',
        ]
        recommendations = [
            f"Add: {req}" for req in required[:4]
        ] + [
            'Add a scannable batch + best-before block in the bottom corner.',
            'Reserve a 20mm clear field for the importer / distributor stamp.',
        ]

        return {
            'agent': self.id,
            'score': score,
            'findings': findings,
            'recommendations': recommendations,
            'detail': {
                'distributorConcerns': [
                    'Missing local importer field',
                    'Allergen formatting not channel-compliant',
                    'Batch field hard to overprint',
                ],
                'retailerConcerns': [
                    'Front-of-pack reads foreign',
                    'Missing local-language hero benefit',
                    'Trust seals are not market-specific',
                ],
                'mustClarifyBeforeLaunch': required,
                'exportChecklist': required + [
                    'Importer / distributor field',
                    'Local-language hero benefit',
                    'Scannable batch + best-before block',
                ],
            },
        }
