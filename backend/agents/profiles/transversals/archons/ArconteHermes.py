# domain/archetypes/archons/ArconteHermes.py
"""
Arconte Hermes – HoloMensajero y Meta-Coordinador
=================================================

Rostros y atributos:
- Mensajero universal: traduce entre voces divergentes.
- Psicopompo: guía memorias y mensajes entre rondas.
- Trickster: reordena prioridades para desatascar flujos.
- Orquestador: marca el ritmo de las iteraciones múltiples.

Integra los subagents del HoloAgentCoordinator:
- ConvergenceEvaluator
- MemoryInjector
- PriorityScheduler
- RoundOrchestrator
"""

from typing import Dict, Any, List
from _subagents.HoloAgentCoordinator.ConvergenceEvaluator import ConvergenceEvaluator
from _subagents.HoloAgentCoordinator.MemoryInjector import MemoryInjector
from _subagents.HoloAgentCoordinator.PriorityScheduler import PriorityScheduler
from _subagents.HoloAgentCoordinator.RoundOrchestrator import RoundOrchestrator


class ArconteHermes:
    def __init__(self, max_rondas: int = 3, usar_memoria: bool = True, debug: bool = False):
        self.convergence = ConvergenceEvaluator()
        self.memory_injector = MemoryInjector()
        self.priority_scheduler = PriorityScheduler()
        self.round_orchestrator = RoundOrchestrator(max_rondas=max_rondas)

        self.usar_memoria = usar_memoria
        self.debug = debug
        self.state = "silent"

    # === Funciones míticas ===
    def invoke(self) -> str:
        """
        Invocación general de Hermes como holo-mensajero.
        """
        self.state = "awakened"
        return (
            "👣 Hermes despierta: mensajero, guía de memorias, "
            "astuto reordenador y orquestador del flujo."
        )

    # === Funciones holo ===
    def mediar(self, voces: List[str]) -> str:
        """
        Usa ConvergenceEvaluator para buscar acuerdos entre voces divergentes.
        """
        convergencia = self.convergence.evaluar(voces)
        return f"🤝 Hermes media: {convergencia}"

    def guiar_memoria(self, contexto: Dict[str, Any], recuerdos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Usa MemoryInjector para transportar memorias al siguiente contexto.
        """
        nuevo_contexto = self.memory_injector.inyectar(contexto, recuerdos)
        return nuevo_contexto

    def reordenar_prioridades(self, tareas: List[str]) -> List[str]:
        """
        Usa PriorityScheduler para alterar el orden y desbloquear el flujo.
        """
        nuevas = self.priority_scheduler.reordenar(tareas)
        return nuevas

    def orquestar_dialogo(self, rondas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Usa RoundOrchestrator para coordinar iteraciones multi-ronda.
        """
        resultado = self.round_orchestrator.orquestar(rondas)
        return resultado
