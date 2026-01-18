# technomorphs/analyst/Dr_Diotropos.py

import time
from typing import Any, Dict, List

from _subagents.RadicalDocumentAnalyst.ArgumentationMapper import \
    ArgumentationMapper
from _subagents.RadicalDocumentAnalyst.FactualityChecker import \
    FactualityChecker
from _subagents.RadicalDocumentAnalyst.RhetoricAnalyzer import RhetoricAnalyzer
from doctors.base_agents import BaseAgente


class RadicalDocumentsAnalyst(BaseAgente):
    """
    Dr. Kael Diótropos – Analista Radical de Documentos
    Identidad técnica: RadicalDocumentsAnalyst
    """

    def __init__(self):
        super().__init__(nombre="Dr. Kael Diótropos")
        self.id = "RadicalDocumentsAnalyst"
        self.rol = "Analista radical de documentos"
        self.dominios = [
            "Retórica política",
            "Cartografía de la argumentación",
            "Verificación factual",
            "Análisis crítico del discurso",
        ]
        self.estilo = "Filoso, documentado, crítico"
        self.frase_firma = "Todo documento es un campo de batalla entre narrativas."

        self.subagentes = [
            RhetoricAnalyzer(),
            ArgumentationMapper(),
            FactualityChecker(),
        ]

    def analizar(self, texto: str, contexto: Dict[str, Any] | None = None) -> Dict[str, Any]:
        if contexto is None:
            contexto = {}

        t0 = time.perf_counter()
        if self.debug_enabled:
            self.log_step({
                "type": "start",
                "title": "Inicio del análisis documental radical",
                "details": {"len_texto": len(texto or ""), "ctx_keys": list(contexto.keys())}
            })

        subresultados: List[Dict[str, Any]] = []

        for sa in self.subagentes:
            st0 = time.perf_counter()
            try:
                res = sa.analizar(texto, contexto)
                subresultados.append(res)
                if self.debug_enabled:
                    self.log_step({
                        "type": "subagent",
                        "title": sa.__class__.__name__,
                        "action": "analizar",
                        "duration_ms": int((time.perf_counter() - st0) * 1000),
                        "data": {k: v for k, v in res.items() if k != "contenido"}
                    })
            except Exception as e:
                subresultados.append({"subagente": sa.__class__.__name__, "error": str(e)})
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
                "title": "Fin del análisis documental radical",
                "duration_ms": int((time.perf_counter() - t0) * 1000)
            })

        resumen = self._sintetizar(subresultados)

        return {
            "rol": self.rol,
            "id": self.id,
            "tipo": "documental",
            "resumen": resumen,
            "frase_firma": self.frase_firma,
            "subagentes": subresultados,
        }

    def _sintetizar(self, subresultados: List[Dict[str, Any]]) -> str:
        partes = []
        for r in subresultados:
            if isinstance(r, dict) and "contenido" in r:
                partes.append(r["contenido"])
        return " | ".join(partes) if partes else "Sin hallazgos destacables"
