# components/controller/ArcontesSystem.py
from __future__ import annotations

from typing import Any, Dict, List, Optional

from arcontes.ArconteApolo import ArconteApolo
from arcontes.ArconteAtenea import ArconteAtenea
from arcontes.ArconteDionisio import ArconteDionisio
from arcontes.ArconteEris import ArconteEris
# Importar todos los Arcontes
from arcontes.ArconteHermes import ArconteHermes


class ArcontesSystem:
    """
    🏛️ Consejo de Arcontes

    Orquesta la interacción de Hermes, Atenea, Apolo, Eris y Dionisio.
    Permite:
      • Invocar a todos los Arcontes sobre una entrada.
      • Invocar solo a un subconjunto.
      • Recibir síntesis final integrada.
    """

    def __init__(self, debug: bool = False):
        self.debug = debug
        self.arcontes = {
            "Hermes": ArconteHermes(debug=debug),
            "Atenea": ArconteAtenea(debug=debug),
            "Apolo": ArconteApolo(debug=debug),
            "Eris": ArconteEris(debug=debug),
            "Dionisio": ArconteDionisio(debug=debug),
        }

    def invocar(
        self,
        texto_usuario: str,
        contexto: Optional[Dict[str, Any]] = None,
        seleccionar: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Ejecuta el Consejo de Arcontes sobre un input.
        - texto_usuario: entrada textual.
        - contexto: datos adicionales (ActivationContext, etc.).
        - seleccionar: lista de nombres de Arcontes específicos a invocar.
        """
        if contexto is None:
            contexto = {}

        if seleccionar:
            activos = {k: v for k, v in self.arcontes.items() if k in seleccionar}
        else:
            activos = self.arcontes

        resultados: Dict[str, Any] = {}
        for nombre, arconte in activos.items():
            try:
                if hasattr(arconte, "ejecutar"):   # Hermes usa ejecutar()
                    res = arconte.ejecutar(texto_usuario, contexto)
                elif hasattr(arconte, "auditar"):  # Atenea, Dionisio, Eris
                    res = arconte.auditar(texto_usuario, contexto)
                elif hasattr(arconte, "sintetizar"):  # Apolo
                    res = arconte.sintetizar(contexto.get("resultados_agentes", {}))
                else:
                    res = {"error": f"Arconte {nombre} no tiene método compatible"}
                resultados[nombre] = res
            except Exception as e:
                resultados[nombre] = {"error": str(e)}

        return {
            "Consejo_de_Arcontes": resultados,
            "resumen": self._resumen_consejo(resultados),
        }

    def _resumen_consejo(self, resultados: Dict[str, Any]) -> str:
        partes = []
        for nombre, salida in resultados.items():
            if isinstance(salida, dict) and "resumen" in salida:
                partes.append(f"{nombre}: {salida['resumen']}")
        return " | ".join(partes) if partes else "Sin síntesis disponible"
