"""
Perfiles de agentes individuales.
Cada agente tiene su propio archivo para facilitar extensión y escalabilidad.
"""
from .base_agents import AgentProfile, BaseAgent
from .cassandra_quark import CassandraQuarkAgent
from .valis import ValisAgent
from .logos import LogosAgent
from .mnemosyne import MnemosyneAgent
from .multiverse_sim import MultiverseSimAgent
from .experimentalist import ExperimentalistAgent
from .pizarras import PizarrasAgent, Pizarra, PizarraBoard, IdeaType, IdeaStatus
from .archivador import ArchivadorAgent, ArchivedDocument, DocumentType, SearchResult

# Registro central de todos los agentes
AGENT_PROFILES = {
    "cassandra_quark": CassandraQuarkAgent.profile,
    "valis": ValisAgent.profile,
    "logos": LogosAgent.profile,
    "mnemosyne": MnemosyneAgent.profile,
    "multiverse_sim": MultiverseSimAgent.profile,
    "experimentalist": ExperimentalistAgent.profile,
    "pizarras": PizarrasAgent.profile,
    "archivador": ArchivadorAgent.profile,
}

# Clases de agentes para acceso directo
AGENT_CLASSES = {
    "cassandra_quark": CassandraQuarkAgent,
    "valis": ValisAgent,
    "logos": LogosAgent,
    "mnemosyne": MnemosyneAgent,
    "multiverse_sim": MultiverseSimAgent,
    "experimentalist": ExperimentalistAgent,
    "pizarras": PizarrasAgent,
    "archivador": ArchivadorAgent,
}


def get_profile(nombre: str) -> AgentProfile | None:
    """Obtiene un perfil de agente por su nombre."""
    return AGENT_PROFILES.get(nombre)


def get_agent_class(nombre: str):
    """Obtiene la clase de un agente por su nombre."""
    return AGENT_CLASSES.get(nombre)


def list_profiles() -> list[str]:
    """Lista todos los perfiles disponibles."""
    return list(AGENT_PROFILES.keys())


__all__ = [
    # Base
    "AgentProfile",
    "BaseAgent",
    # Registros
    "AGENT_PROFILES",
    "AGENT_CLASSES",
    # Funciones
    "get_profile",
    "get_agent_class",
    "list_profiles",
    # Agentes
    "CassandraQuarkAgent",
    "ValisAgent",
    "LogosAgent",
    "MnemosyneAgent",
    "MultiverseSimAgent",
    "ExperimentalistAgent",
    "PizarrasAgent",
    "ArchivadorAgent",
    # Tipos de datos
    "Pizarra",
    "PizarraBoard",
    "IdeaType",
    "IdeaStatus",
    "ArchivedDocument",
    "DocumentType",
    "SearchResult",
]
