from typing import Dict, Any, List


class MitigationPlanner:
    def analizar(self, detectados: List[str], mapa: Dict[str, Any]) -> Dict[str, Any]:
        recs: List[str] = []
        if detectados:
            recs.append("Redisenar narrativas/datos para reducir sesgos")
            recs.append("Auditoria iterativa multi-agente")
        else:
            recs.append("Monitoreo preventivo de sesgos emergentes")
        return {
            "subagente": "MitigationPlanner",
            "recomendaciones": recs,
            "contenido": "; ".join(recs),
        }
