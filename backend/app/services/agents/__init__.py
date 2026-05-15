"""
Market-fit agent system.

Public API:
    from app.services.agents import MarketFitOrchestrator
    from app.services.agents.mock_data import EXAMPLES

The orchestrator runs all 8 specialist agents and synthesizes the final report.
"""

from .orchestrator import MarketFitOrchestrator
from .types import (
    AnalysisInput,
    AgentOutput,
    FinalReport,
    AGENT_WEIGHTS,
)

__all__ = [
    'MarketFitOrchestrator',
    'AnalysisInput',
    'AgentOutput',
    'FinalReport',
    'AGENT_WEIGHTS',
]
