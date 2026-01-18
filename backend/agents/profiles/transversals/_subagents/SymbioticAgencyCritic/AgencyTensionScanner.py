from typing import Dict, Any, List


class AgencyTensionScanner:
    def analizar(self, texto: str, contexto: Dict[str, Any] | None = None) -> Dict[str, Any]:
        if contexto is None:
            contexto = {}
        t = texto.lower()
        tensiones: List[str] = []
        if any(k in t for k in ["sesgo", "bias", "algoritmico", "algorítmico"]):
            tensiones.append("Sesgos algoritmicos autorreplicantes")
        if any(k in t for k in ["humano", "maquina", "maquina", "hibrido", "hibrida", "hibrida"]):
            tensiones.append("Agencia compartida no explicitada")
        if any(k in t for k in ["gnostico", "tecnognostico", "mito", "simbolo"]):
            tensiones.append("Simbolismo tecnognostico")
        if not tensiones:
            tensiones = [
                "Tensiones agenciales latentes",
                "Ambiguiedades de control y responsabilidad",
            ]
        return {
            "subagente": "AgencyTensionScanner",
            "tensiones": tensiones,
            "contenido": ", ".join(tensiones),
        }
