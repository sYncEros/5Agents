from typing import Dict, Any
from agents.base_agents import BaseAgente
from backend.resources import SESGOS_TAXONOMIA
from _subagents.BiasRefractionAuditor.BiasScanner import BiasScanner
from _subagents.BiasRefractionAuditor.EmergentBiasSuggester import EmergentBiasSuggester
from _subagents.BiasRefractionAuditor.MitigationPlanner import MitigationPlanner
import time


class BiasRefractionAuditor(BaseAgente):
    """
    Dr. Eron Kaleidos – Auditor transdisciplinar de sesgos en IA
    Identidad técnica: BiasRefractionAuditor
    """

    def __init__(self):
        super().__init__(nombre="Dr. Eron Kaleidos")
        self.id = "BiasRefractionAuditor"
        self.rol = "Auditor transdisciplinar de sesgos en IA"
        self.dominios = [
            "Crítica algorítmica",
            "Epistemología crítica",
            "Sociología computacional",
            "Semiótica de sistemas técnicos",
        ]
        self.estilo = "Arqueólogo de sesgos latentes y deformaciones culturales"
        self.frase_poder = "No toda distorsión es error; a veces es un reflejo que no queremos ver."
        self.sesgos_base = SESGOS_TAXONOMIA

    def analizar(self, texto: str, contexto: Dict[str, Any] | None = None) -> Dict[str, Any]:
        if contexto is None:
            contexto = {}

        # Log input
        self.log_step({
            "type": "input",
            "title": "Texto recibido",
            "details": texto[:200] + ("…" if len(texto) > 200 else "")
        })

        t0 = time.perf_counter()

        st0 = time.perf_counter()
        bs = BiasScanner().analizar(texto, self.sesgos_base)
        st1 = time.perf_counter()
        self.log_step({
            "type": "subagent",
            "title": "BiasScanner",
            "action": "analizar",
            "duration_ms": int((st1 - st0) * 1000),
            "data": {"n_detectados": len(bs.get("detectados", []))}
        })

        st0 = time.perf_counter()
        eb = EmergentBiasSuggester().analizar(texto)
        st1 = time.perf_counter()
        self.log_step({
            "type": "subagent",
            "title": "EmergentBiasSuggester",
            "action": "analizar",
            "duration_ms": int((st1 - st0) * 1000),
            "data": {"n_sugerencias": len(eb.get("sugerencias", []))}
        })

        st0 = time.perf_counter()
        mp = MitigationPlanner().analizar(bs.get("detectados", []), bs.get("mapa", {}))
        st1 = time.perf_counter()
        self.log_step({
            "type": "subagent",
            "title": "MitigationPlanner",
            "action": "analizar",
            "duration_ms": int((st1 - st0) * 1000),
            "data": {"n_rec": len(mp.get("recomendaciones", []))}
        })

        self.log_step({
            "type": "finish",
            "title": "Fin del análisis",
            "duration_ms": int((time.perf_counter() - t0) * 1000)
        })

        resumen = "; ".join([
            f"Sesgos detectados: {len(bs.get('detectados', []))}",
            f"Sugerencias emergentes: {len(eb.get('sugerencias', []))}",
            f"Recomendaciones: {len(mp.get('recomendaciones', []))}"
        ])

        return {
            "rol": self.rol,
            "id": self.id,
            "sesgos_detectados": bs.get("detectados", []),
            "mapa_categorico": bs.get("mapa", {}),
            "nuevos_sesgos_sugeridos": eb.get("sugerencias", []),
            "recomendaciones": mp.get("recomendaciones", []),
            "resumen": resumen,
            "frase_firma": self.frase_poder,
            "subagentes": [bs, eb, mp],
            "_trace": self.debug_steps
        }
