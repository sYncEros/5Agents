import re
from typing import Any, Dict


class FactualityChecker:
    nombre = "FactualityChecker"
    """Subagente: estima factualidad (citas, números, referencias temporales, entidades)."""

    PISTAS = {
        "citas": [r"\[\d+\]", r"\(\d{4}\)"],
        "numeros": [r"\b\d+(?:,\d+)?\b"],
        "tiempo": [r"\b\d{4}\b", r"siglo", r"década"],
        "entidades": [r"[A-Z][a-z]+(?:\s[A-Z][a-z]+)+"],
    }

    def analizar(self, texto: str, contexto: Dict[str, Any]) -> Dict[str, Any]:
        puntajes = {}
        for k, patrones in self.PISTAS.items():
            count = sum(len(re.findall(p, texto)) for p in patrones)
            puntajes[k] = count
        hipotesis = "Mayor densidad de anclajes empíricos indica orientación documental (no solo ensayística)."
        score = sum(puntajes.values())
        return {
            "subagente": self.nombre,
            "hipotesis": hipotesis,
            "metricas": puntajes,
            "score_factualidad": score,
            "contenido": f"Factualidad -> score={score}, det={puntajes}",
        }
