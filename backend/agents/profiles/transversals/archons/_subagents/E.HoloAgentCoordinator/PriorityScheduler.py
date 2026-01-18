from typing import Dict, Any, List, Tuple

class PriorityScheduler:
    """
    Subagente de Hermes: asigna prioridades a agentes para la siguiente ronda.
    """

    def __init__(self):
        pass

    def priorizar(self, agentes: List[Tuple[str, float]]) -> Dict[str, Any]:
        """
        Recibe agentes como lista de (nombre, score) y devuelve ordenados por prioridad.
        """
        ordenados = sorted(agentes, key=lambda x: -x[1])
        nombres = [a[0] for a in ordenados]

        return {
            "subagente": "PriorityScheduler",
            "orden": nombres,
            "resumen": f"Agentes priorizados: {', '.join(nombres)}"
        }
