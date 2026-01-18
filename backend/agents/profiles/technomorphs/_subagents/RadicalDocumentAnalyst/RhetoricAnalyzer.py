import re
from typing import Any, Dict


class RhetoricAnalyzer:
    nombre = "RhetoricAnalyzer"
    """Subagente: identifica recursos retóricos (metáforas, hipérboles, analogías, preguntas retóricas)."""

    METRICAS = {
        "metafora": [r"como\s+un[oa]?\b", r"como si"],
        "hiperbole": [r"nunca", r"siempre", r"infinit[oa]"],
        "pregunta": [r"\?"],
        "analogias": [r"análogo", r"analogía", r"similar a"],
    }

    def analizar(self, texto: str, contexto: Dict[str, Any]) -> Dict[str, Any]:
        low = texto.lower()
        puntajes = {}
        for k, patrones in self.METRICAS.items():
            count = sum(len(re.findall(p, low)) for p in patrones)
            puntajes[k] = count
        hipotesis = "El documento refuerza persuasión mediante dispositivos retóricos detectables cuantitativamente."
        return {
            "subagente": self.nombre,
            "hipotesis": hipotesis,
            "metricas": puntajes,
            "contenido": f"Retórica -> {puntajes}",
        }
