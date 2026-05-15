"""
Active services module.

The legacy MiroFish simulation services (graph_builder, ontology_generator,
zep_entity_reader, oasis_profile_generator, simulation_manager,
simulation_config_generator, simulation_runner, zep_graph_memory_updater,
simulation_ipc) are intentionally NOT imported here — they depend on
zep-cloud / camel-ai / camel-oasis which are no longer installed.
The legacy files remain on disk so the feature can be revived later by
reinstating those requirements and uncommenting the imports below.

If you re-add a legacy service, also re-add its corresponding blueprint
registration in app/api/__init__.py.
"""

# Currently nothing needs to be eagerly exported. The new market-fit
# agent system lives in app/services/agents/ and is imported directly
# by app/api/label.py.

# --- Legacy (dormant) ---
# from .ontology_generator import OntologyGenerator
# from .graph_builder import GraphBuilderService
# from .text_processor import TextProcessor
# from .zep_entity_reader import ZepEntityReader, EntityNode, FilteredEntities
# from .oasis_profile_generator import OasisProfileGenerator, OasisAgentProfile
# from .simulation_manager import SimulationManager, SimulationState, SimulationStatus
# from .simulation_config_generator import (
#     SimulationConfigGenerator, SimulationParameters, AgentActivityConfig,
#     TimeSimulationConfig, EventConfig, PlatformConfig,
# )
# from .simulation_runner import (
#     SimulationRunner, SimulationRunState, RunnerStatus, AgentAction, RoundSummary,
# )
# from .zep_graph_memory_updater import (
#     ZepGraphMemoryUpdater, ZepGraphMemoryManager, AgentActivity,
# )
# from .simulation_ipc import (
#     SimulationIPCClient, SimulationIPCServer, IPCCommand, IPCResponse,
#     CommandType, CommandStatus,
# )

__all__ = []
