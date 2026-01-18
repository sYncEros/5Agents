from typing import Dict, Any, List


class EthicalDesignPlanner:
    def analizar(self, texto: str, contexto: Dict[str, Any] | None = None) -> Dict[str, Any]:
        if contexto is None:
            contexto = {}
        modelos: List[str] = contexto.get("modelos", [])
        if modelos:
            plan = "Co-disenos iterativos con humanos en bucle"
        else:
            plan = "Auditorias criticas + prototipos de co-agencia"
        return {
            "subagente": "EthicalDesignPlanner",
            "metodologia": plan,
            "contenido": plan,
        }
