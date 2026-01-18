"""
Perfiles de agentes conversacionales con configuraciones específicas de LLM.

NOTA: Los perfiles ahora están modularizados en components/agents/profiles/
Este archivo mantiene compatibilidad hacia atrás re-exportando desde los nuevos módulos.
"""
from components.agents.profiles import (
    AgentProfile,
    AGENT_PROFILES,
    AGENT_CLASSES,
    get_profile,
    get_agent_class,
    list_profiles,
    CassandraQuarkAgent,
    ValisAgent,
    LogosAgent,
    MnemosyneAgent,
    MultiverseSimAgent,
    ExperimentalistAgent,
)

__all__ = [
    "AgentProfile",
    "AGENT_PROFILES",
    "AGENT_CLASSES",
    "get_profile",
    "get_agent_class",
    "list_profiles",
    "CassandraQuarkAgent",
    "ValisAgent",
    "LogosAgent",
    "MnemosyneAgent",
    "MultiverseSimAgent",
    "ExperimentalistAgent",
]
