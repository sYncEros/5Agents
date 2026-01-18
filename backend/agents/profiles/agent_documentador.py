"""
Agent_Documentador - Summarización y generación de reportes
Basado en Palimpsestos: De lo Místico a lo Técnico
"""
from typing import Any
from dataclasses import dataclass, field
from datetime import datetime
from .base_agents import AgentProfile, BaseAgent


@dataclass
class Reporte:
    """Reporte generado por el Documentador."""
    titulo: str
    resumen: str
    por_tema: dict = field(default_factory=dict)  # {tema: resumen}
    por_capa: dict = field(default_factory=dict)  # {capa: hallazgos}
    insights_principales: list[str] = field(default_factory=list)
    recomendaciones: list[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: dict = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "titulo": self.titulo,
            "resumen": self.resumen,
            "por_tema": self.por_tema,
            "por_capa": self.por_capa,
            "insights": self.insights_principales,
            "recomendaciones": self.recomendaciones,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }
    
    def to_markdown(self) -> str:
        """Exporta reporte a markdown."""
        lineas = [
            f"# {self.titulo}",
            f"*Generado: {self.timestamp}*",
            "",
            "## Resumen Ejecutivo",
            self.resumen,
            ""
        ]
        
        if self.por_tema:
            lineas.append("## Por Tema")
            for tema, resumen in self.por_tema.items():
                lineas.append(f"### {tema}")
                lineas.append(resumen)
                lineas.append("")
        
        if self.por_capa:
            lineas.append("## Por Capa de Palimpsestos")
            for capa, hallazgos in self.por_capa.items():
                lineas.append(f"### {capa}")
                lineas.append(hallazgos)
                lineas.append("")
        
        if self.insights_principales:
            lineas.append("## Insights Principales")
            for insight in self.insights_principales:
                lineas.append(f"- {insight}")
            lineas.append("")
        
        if self.recomendaciones:
            lineas.append("## Recomendaciones")
            for rec in self.recomendaciones:
                lineas.append(f"- {rec}")
        
        return "\n".join(lineas)


class DocumentadorAgent(BaseAgent):
    """
    Summarization + template-based report generation (por tema y capa).
    
    USO: generación de reportes estructurados, síntesis de análisis, documentación.
    """
    
    profile = AgentProfile(
        nombre="Documentador",
        rol="Generación de reportes y documentación",
        prompt_base="""Eres un experto en síntesis y reportería.
Tu tarea es generar reportes estructurados:

1. RESUMEN EJECUTIVO: síntesis de 3-5 líneas
2. POR TEMA: análisis desglosado por tema principal
3. POR CAPA: hallazgos según capas de Palimpsestos
4. INSIGHTS: descubrimientos clave (3-5 máximo)
5. RECOMENDACIONES: acciones sugeridas

Formato: claro, estructurado, exportable a markdown/json.
Público: especialistas técnicos y no-técnicos.
Tono: profesional pero accesible.
""",
        modelo_llm="mistral",
        temperatura=0.6,
        tags=["reportería", "síntesis", "documentación"],
        capabilities=["summarization", "report_generation", "markdown_export"]
    )
    
    def __init__(self, llm_client=None):
        super().__init__(llm_client=llm_client)
    
    def process(self, input_text: str, context: dict | None = None) -> str:
        """Procesa y genera reporte."""
        reporte = self.generar_reporte(input_text, context or {})
        return f"Reporte generado: {reporte.titulo}"
    
    def generar_reporte(self, texto: str, contexto: dict) -> Reporte:
        """
        Genera reporte completo basado en texto y contexto.
        """
        titulo = contexto.get("titulo", "Reporte de Análisis")
        
        # Resumen ejecutivo
        resumen = self._generar_resumen(texto)
        
        # Análisis por tema
        por_tema = self._analizar_por_tema(texto, contexto.get("temas", []))
        
        # Análisis por capa (si disponible en contexto)
        por_capa = contexto.get("capas_analisis", {})
        
        # Insights
        insights = self._extraer_insights(texto)
        
        # Recomendaciones
        recomendaciones = self._generar_recomendaciones(insights)
        
        reporte = Reporte(
            titulo=titulo,
            resumen=resumen,
            por_tema=por_tema,
            por_capa=por_capa,
            insights_principales=insights,
            recomendaciones=recomendaciones,
            metadata={
                "longitud_texto": len(texto),
                "contexto_keys": list(contexto.keys()),
                "temas_analizados": len(por_tema)
            }
        )
        
        return reporte
    
    def _generar_resumen(self, texto: str) -> str:
        """Genera resumen ejecutivo (max 3-5 líneas)."""
        # Heurística simple: primeras 2 oraciones
        oraciones = texto.split('.')[:2]
        resumen = '. '.join(oraciones).strip()
        
        if not resumen:
            resumen = "Análisis completado sin hallazgos principales."
        
        return resumen + ("." if not resumen.endswith(".") else "")
    
    def _analizar_por_tema(self, texto: str, temas: list) -> dict:
        """Analiza el texto desglosado por temas."""
        resultado = {}
        
        if not temas:
            return {"general": "Análisis sin temas específicos"}
        
        texto_lower = texto.lower()
        
        for tema in temas:
            if tema.lower() in texto_lower:
                # Extraer párrafos relacionados
                parrafos = texto.split('\n\n')
                relevantes = [p for p in parrafos if tema.lower() in p.lower()]
                
                if relevantes:
                    resumen = relevantes[0][:200] + "..." if len(relevantes[0]) > 200 else relevantes[0]
                    resultado[tema] = resumen
                else:
                    resultado[tema] = f"Tema mencionado pero sin análisis detallado."
            else:
                resultado[tema] = "No presente en el texto"
        
        return resultado
    
    def _extraer_insights(self, texto: str) -> list[str]:
        """Extrae insights principales del texto."""
        insights = []
        
        # Heurística: buscar palabras clave indicadoras de insights
        indicadores = ["importante", "clave", "descubrimiento", "notablemente", "señala", "demuestra"]
        oraciones = texto.split('.')
        
        for oracion in oraciones:
            if any(ind in oracion.lower() for ind in indicadores):
                insight = oracion.strip()
                if len(insight) > 20:  # Mínimo de longitud
                    insights.append(insight)
        
        # Si no hay suficientes, generar genéricos
        while len(insights) < 2:
            insights.append("Análisis completado exitosamente")
        
        return insights[:5]  # Máximo 5
    
    def _generar_recomendaciones(self, insights: list) -> list:
        """Genera recomendaciones basadas en insights."""
        recomendaciones = [
            "Continuar monitoreo de temas principales",
            "Escalar a especialistas si es necesario",
            "Documentar resultados para referencia futura",
        ]
        
        # Agregar recomendaciones específicas según insights
        if any("crisis" in ins.lower() or "riesgo" in ins.lower() for ins in insights):
            recomendaciones.insert(0, "URGENTE: Escalado inmediato recomendado")
        
        return recomendaciones
    
    def analyze(self, input_text: str) -> dict[str, Any]:
        """Análisis - retorna reporte."""
        reporte = self.generar_reporte(input_text, {})
        return {
            "agent": self.profile.nombre,
            "reporte": reporte.to_dict()
        }
