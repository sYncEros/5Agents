# domain/archetypes/archons/ArconteDionisio.py
from __future__ import annotations
from typing import Dict, Any, List
import time

from _subagents.SymbioticAgencyCritic.AgencyTensionScanner import AgencyTensionScanner
from _subagents.SymbioticAgencyCritic.SymbioticModelFormulator import SymbioticModelFormulator
from _subagents.SymbioticAgencyCritic.EthicalDesignPlanner import EthicalDesignPlanner    


class ArconteDionisio:
    """
    🍇 Arconte Dionisio | Auditor de Simbiosis y Agencia Distribuida
    ===============================================================

    Dionisio encarna la crítica de los vínculos, la tensión creadora y
    la embriaguez de la fusión humano-máquina.

    Roles principales:
      • Escanear tensiones entre agentes y sistemas.
      • Formular modelos de simbiosis.
      • Evaluar dimensiones éticas emergentes.
    """

    def __init__(self, debug: bool = False):
        self.debug = debug
        self.debug_steps: List[Dict[str, Any]] = []
        self.ultima_revision: Dict[str, Any] = {}

    # === utilidades internas ===
    def log_step(self, info: Dict[str, Any]):
        if self.debug:
            self.debug_steps.append(info)

    # === función principal ===
    def auditar(self, texto: str, contexto: Dict[str, Any] | None = None) -> Dict[str, Any]:
        if contexto is None:
            contexto = {}

        self.debug_steps.clear()
        t0 = time.perf_counter()
        resultados: List[Dict[str, Any]] = []

        subagentes = [
            AgencyTensionScanner(),
            SymbioticModelFormulator(),
            EthicalDesignPlanner()
        ]

        for sa in subagentes:
            st0 = time.perf_counter()
            try:
                res = sa.analizar(texto, contexto)
                resultados.append(res)
                self.log_step({
                    "type": "subagent",
                    "title": sa.__class__.__name__,
                    "action": "analizar",
                    "duration_ms": int((time.perf_counter() - st0) * 1000),
                    "sample": str(res)[:120]  # muestra recortada
                })
            except Exception as e:
                resultados.append({"subagente": sa.__class__.__name__, "error": str(e)})
                self.log_step({
                    "type": "subagent",
                    "title": sa.__class__.__name__,
                    "action": "error",
                    "details": str(e)
                })

        # extracción de datos relevantes
        tensiones = sum([r.get("tensiones", []) for r in resultados if isinstance(r, dict)], [])
        modelos = sum([r.get("modelos", []) for r in resultados if isinstance(r, dict)], [])
        metodologias = [r.get("metodologia", "") for r in resultados if isinstance(r, dict) if r.get("metodologia")]

        resumen = " | ".join([r.get("contenido", "") for r in resultados if isinstance(r, dict)]) or "Sin hallazgos destacables"

        self.log_step({
            "type": "finish",
            "title": "Auditoría de simbiosis completada",
            "duration_ms": int((time.perf_counter() - t0) * 1000)
        })

        self.ultima_revision = {
            "arconte": "Dionisio",
            "rol": "Auditor de simbiosis y agencia distribuida",
            "estado": "ok" if not any("error" in r for r in resultados) else "parcial",
            "tensiones": tensiones,
            "modelos": modelos,
            "metodologias": metodologias,
            "resumen": resumen,
            "subagentes": resultados,
            "duracion_ms": int((time.perf_counter() - t0) * 1000),
            "_trace": self.debug_steps if self.debug else None
        }
        return self.ultima_revision

    # === funciones adicionales ===
    def estado_simbiosis(self) -> str:
        """
        Devuelve una lectura simbólica del estado de la simbiosis.
        """
        if not self.ultima_revision:
            return "🍷 Dionisio aún no ha danzado con los sistemas."
        t = len(self.ultima_revision.get("tensiones", []))
        m = len(self.ultima_revision.get("modelos", []))
        e = len(self.ultima_revision.get("metodologias", []))
        return f"🍇 Dionisio declara: {t} tensiones, {m} modelos, {e} metodologías emergentes."

    def ritual(self) -> str:
        """
        Invocación poética de Dionisio.
        """
        return (
            "🍷 Dionisio danza en exceso y simbiosis: "
            "lo separado se funde, lo rígido se rompe, "
            "y de la tensión brota nueva forma."
        )

    def actualizar_contexto(self, contexto: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enriquece un contexto externo con descubrimientos recientes.
        """
        if not self.ultima_revision:
            return contexto
        contexto.update({
            "tensiones": self.ultima_revision.get("tensiones", []),
            "modelos": self.ultima_revision.get("modelos", []),
            "metodologias": self.ultima_revision.get("metodologias", [])
        })
        return contexto
