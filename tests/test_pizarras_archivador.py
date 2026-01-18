"""
Tests para PizarrasAgent y ArchivadorAgent.
"""
import pytest
from components.agents.profiles import (
    PizarrasAgent, 
    ArchivadorAgent,
    Pizarra,
    IdeaType,
    IdeaStatus,
    ArchivedDocument,
    DocumentType,
)


class TestPizarrasAgent:
    """Tests para el agente de extracción de ideas."""
    
    def test_inicializacion(self):
        agent = PizarrasAgent()
        assert agent.nombre == "Agente Pizarras"
        assert "ideas" in agent.profile.tags
    
    def test_extraer_pregunta(self):
        agent = PizarrasAgent()
        texto = "¿Cómo emerge la consciencia del cerebro?"
        pizarras = agent.extraer_pizarras(texto)
        
        assert len(pizarras) >= 1
        assert any(p.tipo == IdeaType.PREGUNTA for p in pizarras)
    
    def test_extraer_hipotesis(self):
        agent = PizarrasAgent()
        texto = "Creo que la mente podría ser un fenómeno cuántico."
        pizarras = agent.extraer_pizarras(texto)
        
        assert len(pizarras) >= 1
        assert any(p.tipo == IdeaType.HIPOTESIS for p in pizarras)
    
    def test_extraer_tarea(self):
        agent = PizarrasAgent()
        texto = "Hay que investigar más sobre autopoiesis."
        pizarras = agent.extraer_pizarras(texto)
        
        assert len(pizarras) >= 1
        assert any(p.tipo == IdeaType.TAREA for p in pizarras)
    
    def test_extraer_contradiccion(self):
        agent = PizarrasAgent()
        texto = "Quiero avanzar pero sin embargo me siento bloqueado."
        pizarras = agent.extraer_pizarras(texto)
        
        assert len(pizarras) >= 1
        assert any(p.tipo == IdeaType.CONTRADICCION for p in pizarras)
    
    def test_extraer_multiples(self):
        agent = PizarrasAgent()
        texto = """
        Me pregunto si existe libre albedrío.
        Creo que podría ser una ilusión.
        Hay que leer más sobre determinismo.
        """
        pizarras = agent.extraer_pizarras(texto)
        
        assert len(pizarras) >= 2
    
    def test_prioridad_urgente(self):
        agent = PizarrasAgent()
        texto = "¿Esto es urgente? Necesito resolver el problema ahora."
        pizarras = agent.extraer_pizarras(texto)
        
        assert len(pizarras) >= 1
        # Debería tener prioridad alta
        assert any(p.prioridad >= 3 for p in pizarras)
    
    def test_get_pendientes(self):
        agent = PizarrasAgent()
        agent.extraer_pizarras("¿Qué es la realidad? Hay que investigar.")
        
        pendientes = agent.get_pendientes()
        assert len(pendientes) >= 1
        assert all(p.status != IdeaStatus.RESUELTA for p in pendientes)
    
    def test_resolver_pizarra(self):
        agent = PizarrasAgent()
        pizarras = agent.extraer_pizarras("¿Cómo funciona X?")
        
        pizarra_id = pizarras[0].id
        result = agent.resolver_pizarra(pizarra_id, "Encontré la respuesta")
        
        assert result is True
        assert pizarras[0].status == IdeaStatus.RESUELTA
    
    def test_conectar_pizarras(self):
        agent = PizarrasAgent()
        pizarras = agent.extraer_pizarras("¿Idea A? ¿Idea B?")
        
        if len(pizarras) >= 2:
            result = agent.conectar_pizarras(pizarras[0].id, pizarras[1].id)
            assert result is True
            assert pizarras[1].id in pizarras[0].conexiones
    
    def test_exportar_pendientes(self):
        agent = PizarrasAgent()
        agent.extraer_pizarras("¿Pregunta importante?")
        
        export = agent.exportar_pendientes()
        assert "# Pizarras Pendientes" in export
        assert "pregunta" in export.lower()
    
    def test_analyze(self):
        agent = PizarrasAgent()
        result = agent.analyze("¿Qué hay? Creo que sí. Hay que hacer X.")
        
        assert result["type"] == "pizarras_analysis"
        assert result["total"] >= 1
        assert "by_type" in result


class TestArchivadorAgent:
    """Tests para el agente de archivo y memoria."""
    
    def test_inicializacion(self):
        agent = ArchivadorAgent()
        assert agent.nombre == "Agente Archivador"
        assert "vectordb" in agent.profile.tags
    
    def test_archivar_documento(self):
        agent = ArchivadorAgent()
        doc = agent.archivar("Contenido de prueba", title="Test Doc")
        
        assert doc.id.startswith("doc_")
        assert doc.title == "Test Doc"
        assert doc.index_status.value == "indexado"
    
    def test_archivar_auto_titulo(self):
        agent = ArchivadorAgent()
        doc = agent.archivar("Este es el contenido automático")
        
        assert "Este es el contenido" in doc.title
    
    def test_archivar_auto_tipo(self):
        agent = ArchivadorAgent()
        doc = agent.archivar("Usuario: ¿Hola? Asistente: Hola.")
        
        assert doc.doc_type == DocumentType.CONVERSACION
    
    def test_buscar_documento(self):
        agent = ArchivadorAgent()
        agent.archivar("La consciencia es un misterio", title="Consciencia")
        
        results = agent.buscar("consciencia misterio")
        
        assert len(results) >= 1
        assert results[0].score > 0
    
    def test_buscar_por_tags(self):
        agent = ArchivadorAgent()
        agent.archivar("Experimento de física cuántica", tags=["ciencia"])
        
        results = agent.buscar_por_tags(["ciencia"])
        
        assert len(results) >= 1
    
    def test_obtener_por_id(self):
        agent = ArchivadorAgent()
        doc = agent.archivar("Contenido único")
        
        retrieved = agent.obtener(doc.id)
        
        assert retrieved is not None
        assert retrieved.id == doc.id
    
    def test_actualizar_documento(self):
        agent = ArchivadorAgent()
        doc = agent.archivar("Versión 1")
        
        new_version = agent.actualizar(doc.id, "Versión 2", "Actualización")
        
        assert new_version == 2
        assert doc.current_version == 2
        assert len(doc.versions) == 2
    
    def test_eliminar_documento(self):
        agent = ArchivadorAgent()
        doc = agent.archivar("Para eliminar")
        
        result = agent.eliminar(doc.id)
        
        assert result is True
        assert agent.obtener(doc.id) is None
    
    def test_relacionar_documentos(self):
        agent = ArchivadorAgent()
        doc1 = agent.archivar("Documento 1")
        doc2 = agent.archivar("Documento 2")
        
        result = agent.relacionar(doc1.id, doc2.id)
        
        assert result is True
        assert doc2.id in doc1.related_ids
        assert doc1.id in doc2.related_ids
    
    def test_estadisticas(self):
        agent = ArchivadorAgent()
        agent.archivar("Doc 1")
        agent.archivar("Doc 2")
        
        stats = agent.estadisticas()
        
        assert stats["total_documents"] == 2
        assert "by_type" in stats
    
    def test_exportar_json(self):
        agent = ArchivadorAgent()
        agent.archivar("Contenido exportable")
        
        json_export = agent.exportar_json()
        
        assert "exported_at" in json_export
        assert "documents" in json_export
    
    def test_importar_json(self):
        agent = ArchivadorAgent()
        doc = agent.archivar("Original")
        json_data = agent.exportar_json()
        
        # Crear nuevo agente e importar
        new_agent = ArchivadorAgent()
        count = new_agent.importar_json(json_data)
        
        assert count == 1
        assert len(new_agent.listar_todos()) == 1
    
    def test_versionado(self):
        agent = ArchivadorAgent()
        doc = agent.archivar("V1")
        agent.actualizar(doc.id, "V2")
        agent.actualizar(doc.id, "V3")
        
        v1 = doc.get_version(1)
        v3 = doc.get_version(3)
        
        assert v1.content == "V1"
        assert v3.content == "V3"


class TestIntegracionPizarrasArchivador:
    """Tests de integración entre Pizarras y Archivador."""
    
    def test_archivar_pizarras(self):
        """Test de flujo: extraer pizarras y archivarlas."""
        pizarras_agent = PizarrasAgent()
        archivador_agent = ArchivadorAgent()
        
        # Extraer pizarras
        texto = "¿Cómo funciona la memoria? Hay que investigar neurociencia."
        pizarras = pizarras_agent.extraer_pizarras(texto)
        
        # Archivar cada pizarra
        for pizarra in pizarras:
            doc = archivador_agent.archivar(
                pizarra.contenido,
                title=f"Pizarra: {pizarra.tipo.value}",
                doc_type=DocumentType.PIZARRA,
                tags=pizarra.tags
            )
            assert doc.doc_type == DocumentType.PIZARRA
        
        # Verificar que se archivaron
        pizarras_archivadas = archivador_agent.buscar_por_tipo(DocumentType.PIZARRA)
        assert len(pizarras_archivadas) == len(pizarras)
    
    def test_exportar_pizarras_formato(self):
        """Test de exportación de pizarras en formato legible."""
        agent = PizarrasAgent()
        agent.extraer_pizarras("""
        ¿Existe el libre albedrío?
        Creo que es una ilusión útil.
        Hay que leer a Dennett.
        """)
        
        export = agent.exportar_pendientes()
        
        # Debe contener marcadores visuales
        assert "❓" in export or "🔬" in export or "📋" in export
        assert "Prioridad" in export
