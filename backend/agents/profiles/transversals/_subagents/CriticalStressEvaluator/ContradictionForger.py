from typing import Dict, Any, List

class ContradictionForger:
    """
    Subagente de Eris: genera contra-escenarios y paradojas para tensionar hipótesis.
    """

    def __init__(self):
        pass

    def forjar(self, hipotesis: List[str]) -> Dict[str, Any]:
        contradicciones = []
        for h in hipotesis:
            contradicciones.append(f"Si ocurre lo opuesto a '{h[:40]}...', ¿qué consecuencias tendría?")
        return {
            "subagente": "ContradictionForger",
            "contradicciones": contradicciones,
            "resumen": f"{len(contradicciones)} contradicciones forjadas"
        }
