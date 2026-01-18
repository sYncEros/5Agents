# pipelines/context_builder.py
from __future__ import annotations
from typing import Dict, Any, List
from components.analysis.ActivationContext import ActivationContext


def build_activation_context(
    analisis_temas: Dict[str, Any],
    niveles: Dict[str, float] | None = None,
    guia_sistema: str | None = None,
) -> ActivationContext:
    """
    Construye un ActivationContext a partir de los resultados de TopicsDetector.

    Args:
        analisis_temas: Diccionario con salida de TopicsDetector. 
            Espera claves como:
              - "planos_activos": lista de enums/objetos con `.value`
              - "temas_explícitos": lista de objetos con `.nombre`
              - "contradicciones_emergentes": lista de str
              - "bifurcaciones_detectadas": lista de str
        niveles: dict opcional con floats { "abstraccion", "especulacion", "tecnico" }.
        guia_sistema: string opcional con guía/prompt para los agentes.

    Returns:
        ActivationContext listo para usar con AgentsSystem.
    """
    niveles = niveles or {}
    try:
        planos = [p.value if hasattr(p, "value") else str(p) for p in analisis_temas.get("planos_activos", [])]
        temas = [t.nombre if hasattr(t, "nombre") else str(t) for t in analisis_temas.get("temas_explícitos", [])]
        contradicciones = analisis_temas.get("contradicciones_emergentes", [])
        bifurcaciones = analisis_temas.get("bifurcaciones_detectadas", [])

        ctx = ActivationContext(
            planos_detectados=planos,
            temas_principales=temas,
            contradicciones=contradicciones,
            bifurcaciones=bifurcaciones,
            nivel_abstraccion=float(niveles.get("abstraccion", 0.5)),
            nivel_especulacion=float(niveles.get("especulacion", 0.5)),
            nivel_tecnico=float(niveles.get("tecnico", 0.5)),
            guia_sistema=guia_sistema or "",
        )
        return ctx
    except Exception as e:
        raise ValueError(f"Error al construir ActivationContext: {e}") from e


# 🔧 Extensiones opcionales de análisis contextual

def detectar_faltantes(ctx: ActivationContext) -> List[str]:
    """
    Revisa qué planos/atributos están ausentes y sugiere plantillas.
    Ejemplo: si no hay plano técnico, añade la pregunta-guía correspondiente.
    """
    faltantes: List[str] = []
    if "tecnico" not in [p.lower() for p in ctx.planos_detectados]:
        faltantes.append("Falta plano técnico → sugerir: '¿Qué implicaciones tendría analizar este debate desde una perspectiva técnica/pragmática?'")
    if not ctx.temas_principales:
        faltantes.append("Faltan temas principales → usar TF-IDF para extraer candidatos emergentes")
    return faltantes


def enriquecer_contexto(ctx: ActivationContext, analisis_temas: Dict[str, Any]) -> ActivationContext:
    """
    Ejemplo de pipeline extendido: añade temas emergentes con un simple TF-IDF/clustering,
    detecta contradicciones básicas entre pares de temas, etc.
    """
    from collections import Counter
    import re

    texto_fuente = analisis_temas.get("texto_original", "")
    # TF-IDF/clustering simple → keywords frecuentes
    toks = re.findall(r"[a-zA-Záéíóúüñ]{4,}", texto_fuente.lower())
    freq = Counter(toks)
    emergentes = [w for w, c in freq.most_common(8) if w not in ctx.temas_principales]

    if emergentes:
        ctx.temas_principales.extend(emergentes)

    # Contradicciones simples: IA vs humanidad, etc.
    if "ia" in ctx.temas_principales and "humanidad" in ctx.temas_principales:
        ctx.contradicciones.append("Tensión detectada: IA vs Humanidad")

    return ctx
