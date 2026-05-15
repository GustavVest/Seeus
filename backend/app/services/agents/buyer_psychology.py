"""Buyer Psychology Agent — does the label answer "why this product?" """

from .base import BaseAgent, market_context
from .types import AnalysisInput, AgentOutput


BUYER_PRIMITIVES = {
    'mass':            ('Price-value clarity', 'Functional benefit per cost'),
    'premium':         ('Documented quality', 'Provenance + restraint'),
    'health-conscious':('Clinical credibility', 'Specific compositional facts'),
    'athletes':        ('Performance proof', 'Quantified active amounts + 3rd-party testing'),
    'parents':         ('Risk reduction for the family', 'Allergen transparency + everyday format'),
    'elderly':         ('Trust + simplicity', 'Readable typography, conservative claims'),
    'gen-z':           ('Shareability + values alignment', 'Sustainability + design distinctiveness'),
    'tourists':        ('Local authenticity / souvenir', 'Origin story + gift presentation'),
    'business':        ('Distributor confidence', 'Channel-ready compliance + clear ingredient panel'),
}


class BuyerPsychologyAgent(BaseAgent):
    id = 'buyerMotivation'
    label = 'Buyer Psychology Agent'

    def run(self, input: AnalysisInput) -> AgentOutput:
        ctx = market_context(input.get('target_market', ''))
        buyer = input.get('target_buyer', 'mass')
        cat = input.get('product_category', 'Food')
        primary, lever = BUYER_PRIMITIVES.get(buyer, BUYER_PRIMITIVES['mass'])

        score = self.stable_score(input, lo=55, hi=85)

        # Compose a "stronger message" headline + subheadline.
        headline = self._headline(cat, buyer)
        subheadline = self._sub(buyer, ctx)

        # If the market refs show that competitors lead with specific
        # functional language, surface that as a finding so the agent
        # output reflects real market behavior, not just a template.
        refs = input.get('marketReferences') or {}
        common_claims = (refs.get('commonPatterns') or {}).get('claims') or []
        peer_signal = (
            f"Competitors in this market typically lead with: {', '.join(common_claims[:2])}."
            if common_claims else
            'Current label leads with brand emotion before the functional payoff.'
        )

        findings = [
            f"Target buyer is '{buyer}'; primary trigger is '{primary}'.",
            peer_signal,
            'No clear answer to "why this product, not the one next to it?"',
        ]
        recommendations = [
            f"Lead with: {lever}.",
            'Add one specific, quantified reason-to-believe near the hero.',
            'Position usage occasion (when / where) explicitly.',
        ]

        return {
            'agent': self.id,
            'score': score,
            'findings': findings,
            'recommendations': recommendations,
            'detail': {
                'primaryTrigger': primary,
                'persuasionLever': lever,
                'missingElements': [
                    'Quantified reason-to-believe',
                    'Usage occasion',
                    'Repeat-purchase logic',
                ],
                'recommendedHeadline': headline,
                'recommendedSubheadline': subheadline,
            },
        }

    @staticmethod
    def _headline(cat, buyer):
        if cat == 'Supplement':
            return {
                'athletes':         '10g Quantified Protein · Lab-Verified',
                'health-conscious': 'Quantified Wellness · Third-Party Tested',
                'elderly':          'Daily Support · Clear Daily Dose',
                'parents':          'Family-Safe Supplement · Allergen-Free',
                'gen-z':            'Quantified Wellness · K-Wellness',
                'mass':             'Quantified Daily Dose',
                'premium':          'Verified Origin · Quantified Wellness',
                'tourists':         'Origin-Verified · Souvenir Pack',
                'business':         'Channel-Ready Supplement · Quantified Active',
            }.get(buyer, 'Quantified Wellness')
        if cat == 'Food':
            return {
                'health-conscious': 'High-Protein · Clean-Ingredient',
                'parents':          'Family Snack · Allergen-Visible',
                'premium':          'Origin-Verified · Restrained Quality',
                'gen-z':            'Functional Fuel · Carbon-Aware',
                'mass':             'Family Pack · Trusted Nutrition',
                'tourists':         'Authentic Origin · Gift-Ready',
            }.get(buyer, 'Origin-Verified Food')
        if cat == 'Beverage':
            return {
                'gen-z':            'Functional Beverage · Low Sugar',
                'athletes':         'Quantified Performance Drink',
                'health-conscious': 'Functional Beverage · Quantified',
            }.get(buyer, 'Functional Beverage · Quantified')
        return 'Quantified Hero Benefit'

    @staticmethod
    def _sub(buyer, ctx):
        return ctx['buyer_motivation']
