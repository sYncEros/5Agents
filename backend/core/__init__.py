"""
Módulo core: Lógica central del sistema de agentes.
"""
from .layer_detector import analyze_text, AnalysisResult, Segment
from .layer_detector import analyze_text, AnalysisResult, Segment

# "render_motor_innovacion" depende de Streamlit, que puede no estar instalado en
# entornos de test minimalistas. Hacemos el import de forma perezosa para que
# el resto del paquete (p.ej. layer_detector) pueda usarse sin esa dependencia.
try:  # pragma: no cover - ruta defensiva
    from .motor_innovacion import render_motor_innovacion
except ModuleNotFoundError as exc:  # streamlit ausente
    def render_motor_innovacion(*args, **kwargs):
        raise ModuleNotFoundError(
            "'render_motor_innovacion' requiere la dependencia opcional 'streamlit'. "
            "Instálala para usar esta función."  # pragma: no cover
        ) from exc
from .agent_activator import (
    ContextoActivacion,
    DetectorTemasPlanos,
    SistemaActivacionAgentes
)
from .synthesis_engine import MotorSintesis, Sintesis
from .conversation_controller import ConversationController, ResultadoConversacion

__all__ = [
    "analyze_text",
    "AnalysisResult",
    "Segment",
    "render_motor_innovacion",
    "ContextoActivacion",
    "DetectorTemasPlanos",
    "SistemaActivacionAgentes",
    "MotorSintesis",
    "Sintesis",
    "ConversationController",
    "ResultadoConversacion"
]
