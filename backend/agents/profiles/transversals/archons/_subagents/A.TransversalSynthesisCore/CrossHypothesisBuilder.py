from typing import Dict, Any, List


class CrossHypothesisBuilder:
    def analizar(self, convergencias: List[str], tensiones: List[str], contexto: Dict[str, Any] | None = None) -> Dict[str, Any]:
        hip: List[str] = []
        if convergencias:
            hip.append("Usar convergencias como base de modelos")
        if tensiones:
            hip.append("Explotar tensiones como energia creativa")
        if not hip:
            hip = ["Sintesis minima transdisciplinar"]
        return {
            "subagente": "CrossHypothesisBuilder",
            "hipotesis": hip,
            "contenido": "; ".join(hip),
        }
