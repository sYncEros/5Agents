import re
from typing import Any, Dict


class ArgumentationMapper:
    nombre = "ArgumentationMapper"
    """Subagente: extrae estructura argumental básica (tesis, premisas, objeciones, conclusiones)."""

    PISTAS = {
        "tesis": ["planteamos", "sostenemos", "proponemos"],
        "premisa": ["porque", "debido a", "dado que"],
        "objecion": ["sin embargo", "no obstante", "aunque"],
        "conclusion": ["por lo tanto", "en consecuencia", "concluimos"],
    }

    def analizar(self, texto: str, contexto: Dict[str, Any]) -> Dict[str, Any]:
        low = texto.lower()
        estructura = {}
        for k, pistas in self.PISTAS.items():
            estructura[k] = any(p in low for p in pistas)
        hipotesis = "La arquitectura argumental aparece con marcadores discursivos claros y jerarquizables."
        return {
            "subagente": self.nombre,
            "hipotesis": hipotesis,
            "estructura": estructura,
            "contenido": f"Argumentación -> {estructura}",
        }
