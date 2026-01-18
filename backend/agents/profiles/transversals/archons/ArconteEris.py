# domain/archetypes/archons/ArconteEris.py
from __future__ import annotations
from typing import Dict, Any, List
import time

# Subagentes de Eris
from _subagents.CriticalStressEvaluator.VulnerabilityScanner import VulnerabilityScanner
from _subagents.CriticalStressEvaluator.ContradictionForger import ContradictionForger
from _subagents.CriticalStressEvaluator.AdversarialSimulator import AdversarialSimulator
from _subagents.CriticalStressEvaluator.EthicalRedTeamer import EthicalRedTeamer


class ArconteEris:
    """
    ⚡ Arconte Eris | Evaluadora Crítica de Tensiones

    Eris encarna el conflicto y la perturbación creativa.
    No es un agente con voz personal, sino una función crítica
    que somete hipótesis y modelos a pruebas de estrés.

    Rol:
      • Evaluar resiliencia de hipótesis frente a escenarios adversos.
      • Detectar vulnerabilidades éticas, lógicas o políticas.
      • Introducir contradicciones para fortalecer ideas.
      • Operar como red-team interno en dinámicas epistémicas.
    """

    def __init__(self, debug: bool = False):
        self.debug = debug
        self.debug_steps: List[Dict[str, Any]] = []

        self.subagentes = [
            VulnerabilityScanner(),
            ContradictionForger(),
            AdversarialSimulator(),
            EthicalRedTeamer(),
        ]

    def log_step(self, info: Dict[str, Any]):
        if self.debug:
            self.debug_steps.append(info)

    def estresar(self, entrada: Dict[str, Any]) -> Dict[str, Any]:
        """
        Protocolo de Eris:
          1. Recibe un conjunto de hipótesis o hallazgos.
          2. Pasa la entrada por los 4 subagentes críticos.
          3. Devuelve vulnerabilidades, contradicciones, escenarios adversarios y riesgos éticos.
        """
        t0 = time.perf_counter()
        hipotesis = entrada.get("hipotesis_generadas", []) or entrada.get("hallazgos_principales", [])

        resultados: List[Dict[str, Any]] = []
        for sa in self.subagentes:
            st0 = time.perf_counter()
            try:
                # Cada subagente recibe directamente las hipótesis
                if hasattr(sa, "analizar"):
                    res = sa.analizar(hipotesis)
                elif hasattr(sa, "forjar"):
                    res = sa.forjar(hipotesis)
                elif hasattr(sa, "simular"):
                    res = sa.simular(hipotesis)
                elif hasattr(sa, "evaluar"):
                    res = sa.evaluar(hipotesis)
                else:
                    res = {"subagente": sa.__class__.__name__, "error": "Método no implementado"}

                resultados.append(res)

                self.log_step({
                    "type": "subagent",
                    "title": sa.__class__.__name__,
                    "action": "ejecutado",
                    "duration_ms": int((time.perf_counter() - st0) * 1000)
                })
            except Exception as e:
                resultados.append({"subagente": sa.__class__.__name__, "error": str(e)})
                self.log_step({
                    "type": "subagent",
                    "title": sa.__class__.__name__,
                    "action": "error",
                    "details": str(e)
                })

        resumen = f"Eris aplicó {len(self.subagentes)} pruebas de estrés sobre {len(hipotesis)} hipótesis."

        self.log_step({
            "type": "finish",
            "title": "Evaluación crítica completada",
            "duration_ms": int((time.perf_counter() - t0) * 1000),
            "data": {"n_subagentes": len(self.subagentes), "n_hipotesis": len(hipotesis)}
        })

        return {
            "arconte": "Eris",
            "rol": "Evaluadora crítica y perturbadora epistémica",
            "hipotesis_recibidas": hipotesis,
            "resultados_subagentes": resultados,
            "resumen": resumen,
            "_trace": self.debug_steps if self.debug else None
        }
