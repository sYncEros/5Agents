from typing import Dict, Any, List


class ConvergenceScanner:
    def analizar(self, data: Dict[str, Any] | None = None, contexto: Dict[str, Any] | None = None) -> Dict[str, Any]:
        if data is None:
            data = {}
        temas = []
        for k, v in data.items():
            if isinstance(v, dict):
                for campo in ("cronotopias", "narrativas", "estructuras", "axiomas", "patrones"):
                    if campo in v and v[campo]:
                        temas.append(f"{campo}:{len(v[campo])}")
        if not temas:
            temas = ["convergencias basicas"]
        return {
            "subagente": "ConvergenceScanner",
            "convergencias": temas,
            "contenido": ", ".join(temas),
        }
