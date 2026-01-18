# domain/archetypes/archons/ArconteApolo.py
"""
Arconte Apolo – Señor de la Claridad y la Armonía
=================================================
Integra sus dones solares con el núcleo de síntesis transversal:

- Invoca claridad conceptual usando ConvergenceScanner.
- Crea armonías teóricas con CrossHypothesisBuilder.
- Detecta contradicciones con TensionDetector.
- Proyecta visiones claras con VisualSchemeDesigner.
"""

import random

# Importar subagents del TransversalSynthesisCore
from _subagents.TransversalSynthesisCore.ConvergenceScanner import ConvergenceScanner
from _subagents.TransversalSynthesisCore.CrossHypothesisBuilder import CrossHypothesisBuilder
from _subagents.TransversalSynthesisCore.TensionDetector import TensionDetector
from _subagents.TransversalSynthesisCore.VisualSchemeDesigner import VisualSchemeDesigner

class ArconteApolo:
    def __init__(self):
        self.aspects = {
            "solar": "☀️ Apolo solar: portador de luz y claridad.",
            "oracle": "🔮 Apolo profético: voz de Delfos en enigmas.",
            "music": "🎶 Apolo músico: la lira que ordena en armonía.",
            "healer": "🌿 Apolo sanador: medicina y purificación.",
            "archer": "🏹 Apolo arquero: flechas de precisión que atraviesan la confusión."
        }
        self.hymns = [
            "Que la lira de Apolo ilumine la noche del alma.",
            "Del caos surge armonía bajo el arco solar.",
            "El oráculo habla: claridad en medio del enigma.",
            "Donde hay sombra, Apolo derrama luz."
        ]
        self.state = "silent"

        # Instanciar los subagents del Core
        self.convergence = ConvergenceScanner()
        self.cross_builder = CrossHypothesisBuilder()
        self.tension = TensionDetector()
        self.visualizer = VisualSchemeDesigner()

    # === Funciones míticas ===
    def invoke(self) -> str:
        self.state = "awakened"
        return "\n".join(self.aspects.values())

    def hymn(self) -> str:
        return random.choice(self.hymns)

    def heal(self, ailment: str) -> str:
        return f"🌿 Apolo cura «{ailment}» con su medicina solar."

    def prophesize(self, question: str) -> str:
        return f"🔮 El oráculo de Apolo susurra sobre «{question}»: claridad llegará en su momento."

    def harmony(self, chaos: str) -> str:
        return f"🎶 El caos «{chaos}» se transforma en lira bajo Apolo."

    # === Funciones integradas con el Core ===
    def illuminate_convergence(self, ideas: list) -> str:
        """
        Usa ConvergenceScanner para iluminar puntos comunes.
        """
        result = self.convergence.scan(ideas)
        return f"☀️ Apolo revela convergencias: {result}"

    def build_cross_hypothesis(self, hypotheses: list) -> str:
        """
        Usa CrossHypothesisBuilder para tejer nuevas hipótesis.
        """
        result = self.cross_builder.build(hypotheses)
        return f"🎶 Apolo entrelaza hipótesis en armonía: {result}"

    def detect_tensions(self, arguments: list) -> str:
        """
        Usa TensionDetector para detectar contradicciones.
        """
        result = self.tension.detect(arguments)
        return f"🏹 Apolo apunta a las tensiones: {result}"

    def design_vision(self, structure: dict) -> str:
        """
        Usa VisualSchemeDesigner para mostrar esquemas de claridad.
        """
        result = self.visualizer.design(structure)
        return f"🌞 Apolo proyecta una visión clara:\n{result}"


if __name__ == "__main__":
    apolo = ArconteApolo()
    print("=== Invocación de Apolo ===")
    print(apolo.invoke())
    print(apolo.illuminate_convergence(["Música", "Matemática", "Luz"]))
    print(apolo.build_cross_hypothesis(["El caos ordena", "La luz armoniza"]))
    print(apolo.detect_tensions(["Hipótesis A", "Contradicción en B"]))
    print(apolo.design_vision({"concepto": "claridad", "origen": "caos"}))
