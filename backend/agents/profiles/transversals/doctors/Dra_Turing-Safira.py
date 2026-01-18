# agents/agente_nox.py

from typing import Dict, Any
import time
from agents.base_agents import BaseAgente
from _subagents.SymbioticAgencyCritic.AgencyTensionScanner import AgencyTensionScanner
from _subagents.SymbioticAgencyCritic.SymbioticModelFormulator import SymbioticModelFormulator
from _subagents.SymbioticAgencyCritic.EthicalDesignPlanner import EthicalDesignPlanner


class SymbioticAgencyCritic(BaseAgente):
    """
    Dra. Nox Turing-Safira – Crítica Simbiótica de la Agencia Técnica
    Identidad técnica: SymbioticAgencyCritic
    """

    def __init__(self):
        super().__init__(nombre="Dra. Nox Turing-Safira")
        self.id = "SymbioticAgencyCritic"
        self.rol = "Crítica simbiótica de la agencia técnica"
        self.dominios = [
            "Filosofía de la técnica",
            "Simbiosis humano-máquina",
            "Crítica cultural tecnognóstica",
            "Antropotecnia",
            "Diseño especulativo post-humano",
        ]
        self.estilo = "Crítica, elegante, ácida"
        self.frase_firma = "La agencia no se programa: se negocia."

        self.subagentes = [
            AgencyTensionScanner(),
            SymbioticModelFormulator(),
            EthicalDesignPlanner(),
        ]

    def analizar(self, texto: str, contexto: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """Analiza agencia técnica, ética emergente y simbiosis humano-máquina"""
        if contexto is None:
            contexto = {}

        t0 = time.perf_counter()
        if self.debug_enabled:
            self.log_step({
                "type": "start",
                "title": "Inicio del análisis de agencia simbiótica",
                "details": {"len_texto": len(texto or ""), "ctx_keys": list(contexto.keys())}
            })

        resultados = []
        for sa in self.subagentes:
            st0 = time.perf_counter()
            try:
                res = sa.analizar(texto, contexto)
                resultados.append(res)
                if self.debug_enabled:
                    self.log_step({
                        "type": "subagent",
                        "title": sa.__class__.__name__,
                        "action": "analizar",
                        "duration_ms": int((time.perf_counter() - st0) * 1000),
                        "data": {k: v for k, v in res.items() if k != "contenido"}
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
                "title": "Fin del análisis de agencia simbiótica",
                "duration_ms": int((time.perf_counter() - t0) * 1000)
            })

        # Extraer outputs clave
        tensiones = resultados[0].get("tensiones", []) if isinstance(resultados[0], dict) else []
        modelos = resultados[1].get("modelos", []) if len(resultados) > 1 and isinstance(resultados[1], dict) else []
        metodologia = resultados[2].get("metodologia", "") if len(resultados) > 2 and isinstance(resultados[2], dict) else ""

        resumen = " | ".join([r.get("contenido", "") for r in resultados if isinstance(r, dict)]) or "Sin hallazgos destacables"

        return {
            "rol": self.rol,
            "id": self.id,
            "tensiones": tensiones,
            "modelos": modelos,
            "metodologia": metodologia,
            "resumen": resumen,
            "frase_firma": self.frase_firma,
            "subagentes": resultados,
        }
