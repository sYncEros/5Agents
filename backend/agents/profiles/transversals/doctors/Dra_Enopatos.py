# agents/TransversalSynthesisCore.py

from typing import Dict, Any
import time
from agents.base_agents import BaseAgente
from _subagents.TransversalSynthesisCore.ConvergenceScanner import ConvergenceScanner
from _subagents.TransversalSynthesisCore.TensionDetector import TensionDetector
from _subagents.TransversalSynthesisCore.CrossHypothesisBuilder import CrossHypothesisBuilder
from _subagents.TransversalSynthesisCore.VisualSchemeDesigner import VisualSchemeDesigner


class TransversalSynthesisCore(BaseAgente):
    """
    Dra. Sol Enopatos – Sintetizador Transversal de Hallazgos
    Identidad técnica: TransversalSynthesisCore
    """

    def __init__(self):
        super().__init__(nombre="Dra. Sol Enopatos")
        self.id = "TransversalSynthesisCore"
        self.rol = "Sintetizadora transversal de hallazgos"
        self.dominios = [
            "Integración transdisciplinar",
            "Sistemas complejos",
            "Síntesis epistémica",
            "Visualización conceptual",
        ]
        self.estilo = "Arquitecta de pensamiento emergente, transversal, visualizadora"
        self.frase_firma = "El conocimiento emerge entre las tensiones."

        self.subagentes = [
            ConvergenceScanner(),
            TensionDetector(),
            CrossHypothesisBuilder(),
            VisualSchemeDesigner(),
        ]

    def sintetizar(self, analisis_agentes: Dict[str, Dict[str, Any]] | None = None) -> Dict[str, Any]:
        if analisis_agentes is None:
            analisis_agentes = {}

        resultados = []
        t0 = time.perf_counter()

        for sa in self.subagentes:
            st = time.perf_counter()
            try:
                if isinstance(sa, ConvergenceScanner):
                    r = sa.analizar(analisis_agentes, {})
                elif isinstance(sa, TensionDetector):
                    r = sa.analizar(analisis_agentes, {})
                elif isinstance(sa, CrossHypothesisBuilder):
                    conv = resultados[0].get("convergencias", []) if resultados else []
                    tens = resultados[1].get("tensiones", []) if len(resultados) > 1 else []
                    r = sa.analizar(conv, tens, {})
                elif isinstance(sa, VisualSchemeDesigner):
                    hips = resultados[2].get("hipotesis", []) if len(resultados) > 2 else []
                    r = sa.analizar(hips, {})
                else:
                    r = sa.analizar({}, {})
                resultados.append(r)

                if self.debug_enabled:
                    self.log_step({
                        "type": "subagent",
                        "title": sa.__class__.__name__,
                        "action": "analizar",
                        "duration_ms": int((time.perf_counter() - st) * 1000),
                        "data": {k: v for k, v in r.items() if k != "contenido"}
                    })
            except Exception as e:
                resultados.append({"subagente": sa.__class__.__name__, "error": str(e)})
                if self.debug_enabled:
                    self.log_step({
                        "type": "subagent",
                        "title": sa.__class__.__name__,
                        "action": "error",
                        "details": str(e)
                    })

        if self.debug_enabled:
            self.log_step({
                "type": "finish",
                "title": "Síntesis transversal completada",
                "duration_ms": int((time.perf_counter() - t0) * 1000)
            })

        resumen = " | ".join([r.get("contenido", "") for r in resultados if isinstance(r, dict)]) or \
                  "Sin hallazgos en la síntesis transversal"

        return {
            "rol": self.rol,
            "id": self.id,
            "convergencias": resultados[0].get("convergencias", []) if len(resultados) > 0 else [],
            "tensiones": resultados[1].get("tensiones", []) if len(resultados) > 1 else [],
            "hipotesis": resultados[2].get("hipotesis", []) if len(resultados) > 2 else [],
            "esquema": resultados[3].get("esquema", "") if len(resultados) > 3 else "",
            "resumen": resumen,
            "frase_firma": self.frase_firma,
            "subagentes": resultados,
        }

    def analizar(self, texto: str, contexto: Dict[str, Any]) -> Dict[str, Any]:
        """
        Método adaptador para el pipeline actual de AgentsSystem.
        Esta clase está pensada para sintetizar resultados de múltiples agentes,
        lo cual se realiza aguas abajo por el Motor de Síntesis. Aquí devolvemos
        un resultado mínimo no bloqueante para evitar errores de ejecución.
        """
        if self.debug_enabled:
            self.log_step({
                "type": "noop",
                "title": "Agente de síntesis global (fase diferida)",
                "details": "No opera sobre una sola entrada, solo en síntesis global."
            })
        return {
            "rol": self.rol,
            "id": self.id,
            "resumen": "Operación diferida al módulo de síntesis global.",
            "convergencias": [],
            "tensiones": [],
            "hipotesis": [],
            "esquema": "",
            "frase_firma": self.frase_firma,
        }
