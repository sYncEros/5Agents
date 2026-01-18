from domain.analysis.ActivationContext import ActivationContext
from domain.analysis.AgentsSystem import \
    AgentsActivationSystem as SistemaActivacionAgentes
from domain.analysis.SynthesisMotor import SynthesisMotor as MotorSintesis
from domain.analysis.TopicsDetector import \
    TopicsDetector as DetectorTemasPlanos


def ejecutar_analisis_completo(texto_usuario, parametros):
    # Paso 1: Detección
    detector = DetectorTemasPlanos()
    resultado_deteccion = detector.analizar_conversacion(texto_usuario)

    # Paso 2: Crear contexto para activar agentes
    temas_principales = [t.nombre for t in resultado_deteccion.get("temas_explícitos", [])]
    if not temas_principales:
        try:
            temas_principales = [t.nombre for t in resultado_deteccion.get("temas_implícitos", [])]
        except Exception:
            temas_principales = temas_principales or []
    if not temas_principales:
        try:
            temas_principales = [t.nombre for t in resultado_deteccion.get("temas_emergentes", [])]
        except Exception:
            temas_principales = temas_principales or []

    contexto = ActivationContext(
        planos_detectados=[getattr(plano, 'value', str(plano)) for plano in resultado_deteccion.get("planos_activos", [])],
        temas_principales=temas_principales,
        contradicciones=resultado_deteccion.get("contradicciones_emergentes", []),
        bifurcaciones=resultado_deteccion.get("bifurcaciones_detectadas", []),
        nivel_abstraccion=parametros["nivel_abstraccion"],
        nivel_especulacion=parametros["nivel_especulacion"],
        nivel_tecnico=parametros["nivel_tecnico"],
        guia_sistema=(parametros.get("guia_sistema", "") or "").strip()
    )

    # Paso 3: Activación de agentes
    sistema = SistemaActivacionAgentes()
    analisis_agentes = sistema.analizar_con_agentes(texto_usuario, contexto)

    # Paso 4: Síntesis
    motor = MotorSintesis()
    sintesis_final = motor.sintetizar_analisis_agentes(analisis_agentes)

    return resultado_deteccion, analisis_agentes, sintesis_final
