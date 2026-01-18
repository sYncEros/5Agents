"""
Módulo de integración con LLMs locales y remotos.
"""
from .ollama_client import OllamaClient
from .profiles import AgentProfile, AGENT_PROFILES

__all__ = ["OllamaClient", "AgentProfile", "AGENT_PROFILES"]
