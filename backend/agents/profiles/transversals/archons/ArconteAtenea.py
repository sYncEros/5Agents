# domain/archetypes/archons/ArconteAtenea.py
from __future__ import annotations
from typing import Dict, Any, List
import time
from theory.commonsKnowLedge.BiasesTaxonomy import SESGOS_TAXONOMIA
from _subagents.B.BiasRefractionAuditor.BiasScanner import BiasScanner
from _subagents.B.BiasRefractionAuditor.EmergentBiasSuggester import EmergentBiasSuggester
from _subagents.B.BiasRefractionAuditor.MitigationPlanner import MitigationPlanner


class ArconteAtenea:
    """
    🏛️ Arconte Atenea | Guardiana de Claridad
    ==========================================

    Atenea examina los sesgos como diosa de la sabiduría y la estrategia.
    No habla en exceso, sino que ilumina lo oculto.

    Roles principales:
      • Escanear sesgos conocidos según taxonomía establecida.
      • Detectar posibles sesgos emergentes no catalogados.
      • Proponer estrategias de mitigación.
      • Mantener viva la taxonomía de sesgos.
      • Consultar el estado de claridad del sistema.
    """

    def __init__(self, debug: bool = False):
        self.debug = debug
        self.sesgos_base: Dict[str, Any] = SESGOS_TAXONOMIA.copy()
        self.debug_steps: List[Dict[str, Any]] = []
        self.ultima_revision: Dict[str, Any] = {}

    # === Utilidad interna ===
    def log_step(self, info: Dict[str, Any]):
        if self.debug:
            self.debug_steps.append(info)

    def _safe_call(self, func, *args, **kwargs) -> Dict[str, Any]:
        """
        Llamada resiliente a subagents: atrapa errores en lugar de romper el flujo.
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return {"error": str(e)}

    # === Funciones principales ===
    def auditar(self, texto: str, contexto: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """
        Protocolo de Atenea:
          1. Escanear sesgos conocidos.
          2. Sugerir sesgos emergentes.
          3. Proponer mitigaciones.
        """
        if contexto is None:
            contexto = {}

        self.debug_steps.clear()
        t0 = time.perf_counter()

        # Subagente 1 → escáner de sesgos
        st = time.perf_counter()
        bs = self._safe_call(BiasScanner().analizar, texto, self.sesgos_base)
        self.log_step({
            "type": "BiasScanner",
            "duration_ms": int((time.perf_counter() - st) * 1000),
            "sample": bs.get("detectados", [])[:2]
        })

        # Subagente 2 → sugerencias emergentes
        st = time.perf_counter()
        eb = self._safe_call(EmergentBiasSuggester().analizar, texto)
        self.log_step({
            "type": "EmergentBiasSuggester",
            "duration_ms": int((time.perf_counter() - st) * 1000),
            "sample": eb.get("sugerencias", [])[:2]
        })

        # Subagente 3 → mitigación
        st = time.perf_counter()
        mp = self._safe_call(MitigationPlanner().analizar,
                             bs.get("detectados", []),
                             bs.get("mapa", {}))
        self.log_step({
            "type": "MitigationPlanner",
            "duration_ms": int((time.perf_counter() - st) * 1000),
            "sample": mp.get("recomendaciones", [])[:2]
        })

        resumen = "; ".join([
            f"Sesgos detectados: {len(bs.get('detectados', []))}",
            f"Sugerencias emergentes: {len(eb.get('sugerencias', []))}",
            f"Recomendaciones: {len(mp.get('recomendaciones', []))}"
        ])

        self.ultima_revision = {
            "arconte": "Atenea",
            "rol": "Guardiana de claridad y crítica algorítmica",
            "sesgos_detectados": bs.get("detectados", []),
            "mapa_categorico": bs.get("mapa", {}),
            "nuevos_sesgos_sugeridos": eb.get("sugerencias", []),
            "recomendaciones": mp.get("recomendaciones", []),
            "resumen": resumen,
            "duracion_ms": int((time.perf_counter() - t0) * 1000),
            "_trace": self.debug_steps if self.debug else None
        }
        return self.ultima_revision

    # === Funciones adicionales ===
    def actualizar_taxonomia(self, nuevos_sesgos: List[Dict[str, Any]]):
        """
        Permite que Atenea incorpore nuevos sesgos validados a la taxonomía base.
        """
        for sesgo in nuevos_sesgos:
            clave = sesgo.get("nombre")
            if clave and clave not in self.sesgos_base:
                self.sesgos_base[clave] = sesgo
        return {"estado": "actualizado", "total": len(self.sesgos_base)}

    def estado_claridad(self) -> str:
        """
        Devuelve una lectura poética del estado de claridad del sistema.
        """
        if not self.ultima_revision:
            return "⚖️ Atenea aún no ha mirado en el espejo de los sesgos."
        sesgos = len(self.ultima_revision.get("sesgos_detectados", []))
        emergentes = len(self.ultima_revision.get("nuevos_sesgos_sugeridos", []))
        recs = len(self.ultima_revision.get("recomendaciones", []))
        return (f"🏛️ Atenea declara: {sesgos} sesgos visibles, "
                f"{emergentes} emergentes, {recs} caminos de mitigación.")
