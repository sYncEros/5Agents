from typing import Dict, Any


class BiasScanner:
    def analizar(self, texto: str, taxonomia: Dict[str, list]) -> Dict[str, Any]:
        texto_l = texto.lower()
        detectados = []
        mapa: Dict[str, list] = {}
        for categoria, sesgos in taxonomia.items():
            mapa[categoria] = []
            for sesgo in sesgos:
                if any(k in texto_l for k in sesgo.get("palabras_clave", [])):
                    detectados.append(sesgo["nombre"])
                    mapa[categoria].append({
                        "nombre": sesgo["nombre"],
                        "explicacion": sesgo.get("explicacion", ""),
                        "riesgo": sesgo.get("riesgo", "medio"),
                    })
        return {
            "subagente": "BiasScanner",
            "detectados": detectados,
            "mapa": mapa,
            "contenido": f"sesgos:{len(detectados)} categorias:{len(mapa)}",
        }
