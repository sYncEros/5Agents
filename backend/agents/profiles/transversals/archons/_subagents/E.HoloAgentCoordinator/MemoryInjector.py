from typing import Dict, Any, List

class MemoryInjector:
    """
    Subagente de Hermes: inyecta memoria histórica en el contexto activo.
    """

    def __init__(self, memoria_global: List[Dict[str, Any]] | None = None):
        self.memoria_global = memoria_global or []

    def inyectar(self, contexto: Dict[str, Any]) -> Dict[str, Any]:
        """
        Añade memoria previa al contexto actual.
        """
        contexto_actualizado = {**contexto}
        contexto_actualizado["memoria_inyectada"] = self.memoria_global[:5]

        return {
            "subagente": "MemoryInjector",
            "contexto_actualizado": contexto_actualizado,
            "resumen": f"Se inyectaron {len(self.memoria_global[:5])} elementos de memoria"
        }
