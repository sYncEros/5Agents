from typing import Dict, Any, List

class RoundOrchestrator:
    """
    Subagente de Hermes: coordina las rondas de resonancia entre agentes.
    """

    def __init__(self, max_rondas: int = 3):
        self.max_rondas = max_rondas

    def organizar(self, agentes: List[str]) -> Dict[str, Any]:
        """
        Genera la secuencia de rondas con agentes asignados.
        """
        rondas = []
        for i in range(self.max_rondas):
            rondas.append({
                "ronda": i + 1,
                "agentes": agentes
            })

        return {
            "subagente": "RoundOrchestrator",
            "rondas_plan": rondas,
            "resumen": f"{len(rondas)} rondas programadas"
        }
