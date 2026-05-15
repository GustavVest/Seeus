"""
MarketFitOrchestrator — runs all 8 specialist agents over an AnalysisInput
and synthesizes the FinalReport.

Frontend / API path:
    >>> from app.services.agents.orchestrator import MarketFitOrchestrator
    >>> report = MarketFitOrchestrator().analyze(analysis_input)
"""

from typing import Dict

from .types import AnalysisInput, AgentOutput, FinalReport
from .culture_fit import CultureFitAgent
from .market_trend import MarketTrendAgent
from .claims_safety import ClaimsSafetyAgent
from .visual_hierarchy import VisualHierarchyAgent
from .palette_design import PaletteDesignAgent
from .competitor_positioning import CompetitorPositioningAgent
from .buyer_psychology import BuyerPsychologyAgent
from .export_readiness import ExportReadinessAgent
from .final_strategy import synthesize
from .competitor_references import get_competitor_references


class MarketFitOrchestrator:
    """Runs all specialist agents and synthesizes the final report."""

    def __init__(self):
        self.agents = [
            CultureFitAgent(),
            MarketTrendAgent(),
            ClaimsSafetyAgent(),
            VisualHierarchyAgent(),
            PaletteDesignAgent(),
            CompetitorPositioningAgent(),
            BuyerPsychologyAgent(),
            ExportReadinessAgent(),
        ]

    def analyze(self, input: AnalysisInput) -> FinalReport:
        # Step 1: pull market-reference signals BEFORE the agents run so each
        # agent can read summary['marketReferences'] from the input if it
        # wants to ground its findings in observed category norms.
        # TODO (live): swap this for a real-data adapter; same return shape.
        market_refs = get_competitor_references(
            product_name=input.get('product_name', ''),
            product_category=input.get('product_category', ''),
            target_market=input.get('target_market', ''),
            target_channel=input.get('target_channel', ''),
            target_buyer=input.get('target_buyer', ''),
            price_tier=input.get('price_tier', ''),
            brand_goal=input.get('brand_goal', ''),
        )
        # Attach to the input dict the agents read from.
        enriched_input = dict(input)
        enriched_input['marketReferences'] = market_refs

        outputs: Dict[str, AgentOutput] = {}
        for agent in self.agents:
            outputs[agent.id] = agent.run(enriched_input)
        return synthesize(enriched_input, outputs, market_refs)
