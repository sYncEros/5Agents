"""
Clase base para perfiles de agentes conversacionales.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass
class AgentProfile:
    """Perfil de configuración para un agente conversacional."""
    
    nombre: str
    rol: str
    prompt_base: str
    modelo_llm: str = "mistral"
    temperatura: float = 0.7
    max_tokens: Optional[int] = None
    
    # Metadatos adicionales para extensibilidad
    tags: list[str] = field(default_factory=list)
    capabilities: list[str] = field(default_factory=list)
    version: str = "1.0.0"
    
    def build_prompt(self, user_input: str) -> str:
        """Construye el prompt completo incluyendo la entrada del usuario."""
        return f"{self.prompt_base}\n\nUsuario: {user_input}\n\nRespuesta:"
    
    def build_context_prompt(self, user_input: str, context: dict[str, Any]) -> str:
        """Construye prompt con contexto adicional."""
        context_str = "\n".join(f"- {k}: {v}" for k, v in context.items())
        return f"{self.prompt_base}\n\nContexto:\n{context_str}\n\nUsuario: {user_input}\n\nRespuesta:"


class BaseAgent(ABC):
    """Clase base abstracta para todos los agentes."""
    
    profile: AgentProfile  # Cada subclase define su perfil
    
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self._history: list[dict] = []
    
    @property
    def nombre(self) -> str:
        return self.profile.nombre
    
    @property
    def rol(self) -> str:
        return self.profile.rol
    
    def build_prompt(self, user_input: str) -> str:
        """Construye el prompt para este agente."""
        return self.profile.build_prompt(user_input)
    
    def add_to_history(self, role: str, content: str):
        """Añade mensaje al historial."""
        self._history.append({"role": role, "content": content})
    
    def get_history(self) -> list[dict]:
        """Obtiene historial de conversación."""
        return self._history.copy()
    
    def clear_history(self):
        """Limpia historial."""
        self._history.clear()
    
    @abstractmethod
    def process(self, input_text: str, context: dict | None = None) -> str:
        """Procesa entrada y genera respuesta. Implementar en subclases."""
        pass
    
    def analyze(self, input_text: str) -> dict[str, Any]:
        """Análisis específico del agente. Override en subclases."""
        return {
            "agent": self.profile.nombre,
            "input": input_text,
            "analysis": None
        }
    
    def collaborate(self, other_agent: "BaseAgent", topic: str) -> dict[str, Any]:
        """Genera perspectivas colaborativas con otro agente."""
        return {
            "from": self.nombre,
            "to": other_agent.nombre,
            "topic": topic,
            "perspective": None
        }
