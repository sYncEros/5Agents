from typing import Dict, Any, List

class ConvergenceEvaluator:
    """
    Subagente de Hermes: evalúa convergencia de hipótesis/síntesis.
    """

    def __init__(self, umbral: float = 0.8):
        self.umbral = umbral

    def evaluar(self, resultados: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Determina si el sistema alcanzó convergencia suficiente para detener rondas.
        """
        scores = []
        for r in resultados:
            if isinstance(r, dict) and "score" in r:
                scores.append(r["score"])

        convergencia = (sum(scores) / len(scores)) if scores else 0.0
        detener = convergencia >= self.umbral

        return {
            "subagente": "ConvergenceEvaluator",
            "convergencia_score": convergencia,
            "detener": detener,
            "resumen": f"Convergencia {convergencia:.2f} (umbral {self.umbral})"
        }
