from typing import Dict, Any, List


class TensionDetector:
    def analizar(self, data: Dict[str, Any] | None = None, contexto: Dict[str, Any] | None = None) -> Dict[str, Any]:
        if data is None:
            data = {}
        tensiones: List[str] = []
        # Heuristica simple: presencia simultanea de campos que suelen chocar
        if any("logica" in (v.get("rol","" )+" "+v.get("id","" )).lower() for v in data.values()) and \
           any("mito" in (v.get("rol","" )+" "+v.get("id","" )).lower() or "narrativ" in (v.get("rol","" )+" "+v.get("id","" )).lower() for v in data.values()):
            tensiones.append("Logico-formal vs narrativo-mitico")
        if any("memoria" in (v.get("rol","" )+" "+v.get("id","" )).lower() for v in data.values()) and \
           any("generativ" in (v.get("rol","" )+" "+v.get("id","" )).lower() for v in data.values()):
            tensiones.append("Memoria humana vs generativo")
        if not tensiones:
            tensiones = ["Determinista vs caotico"]
        return {
            "subagente": "TensionDetector",
            "tensiones": tensiones,
            "contenido": "; ".join(tensiones),
        }
