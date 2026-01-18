"""
Agent_Archivador - Vector DB, versionado y metadatos para reconstrucción
Basado en Palimpsestos: De lo Místico a lo Técnico
"""
from typing import Any, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json


@dataclass
class DocumentoArchivado:
    """Documento versionado en el archivo."""
    id: str
    contenido: str
    tipo: str  # "conversacion", "análisis", "síntesis", "insight"
    timestamp_creacion: str
    timestamp_ultima_mod: str
    versiones: List[dict] = field(default_factory=list)  # [{version, content, timestamp, cambios}]
    metadatos: dict = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    estado_indexacion: str = "pendiente"  # "pendiente", "indexado", "error"
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "contenido": self.contenido,
            "tipo": self.tipo,
            "creacion": self.timestamp_creacion,
            "ultima_mod": self.timestamp_ultima_mod,
            "versiones": self.versiones,
            "metadatos": self.metadatos,
            "tags": self.tags,
            "estado": self.estado_indexacion
        }


@dataclass
class IndiceVector:
    """Índice simple para búsqueda (simulado sin VectorDB real)."""
    documento_id: str
    palabras_clave: List[str]
    similitud_base: float  # Para búsqueda de similitud


class ArchivadorAgent:
    """
    Vector DB (Pinecone, Milvus simulado), versionado y metadatos.
    
    USO: reconstruir conversaciones, auditoría, recuperación de análisis previos.
    
    NOTA: Implementación sin dependencias externas (sin llm_client).
    """
    
    def __init__(self, storage_path: str = "./data/archive"):
        self.storage_path = storage_path
        self.documentos: dict[str, DocumentoArchivado] = {}
        self.indices: List[IndiceVector] = []
    
    @property
    def nombre(self) -> str:
        return "Archivador"
    
    @property
    def rol(self) -> str:
        return "Gestión de memoria persistente y versionado"
    
    def process(self, input_text: str, context: dict | None = None) -> str:
        """Procesa y archiva documento."""
        contexto = context or {}
        doc_id = self.archivar_documento(
            contenido=input_text,
            tipo=contexto.get("tipo", "documento"),
            tags=contexto.get("tags", []),
            metadatos=contexto
        )
        return f"Documento archivado: {doc_id}"
    
    def archivar_documento(
        self,
        contenido: str,
        tipo: str = "documento",
        tags: List[str] | None = None,
        metadatos: dict | None = None
    ) -> str:
        """
        Archiva un documento con versionado automático.
        """
        doc_id = f"doc_{len(self.documentos)}_{hash(contenido) % 10000}"
        ahora = datetime.now().isoformat()
        
        # Primera versión
        version_inicial = {
            "version": 1,
            "contenido": contenido,
            "timestamp": ahora,
            "cambios": "Creación inicial"
        }
        
        doc = DocumentoArchivado(
            id=doc_id,
            contenido=contenido,
            tipo=tipo,
            timestamp_creacion=ahora,
            timestamp_ultima_mod=ahora,
            versiones=[version_inicial],
            metadatos=metadatos or {},
            tags=tags or [],
            estado_indexacion="pendiente"
        )
        
        self.documentos[doc_id] = doc
        
        # Indexar
        self._indexar_documento(doc_id, contenido)
        
        return doc_id
    
    def actualizar_documento(
        self,
        doc_id: str,
        contenido_nuevo: str,
        cambios_descripcion: str = "Actualización"
    ) -> bool:
        """
        Actualiza documento creando nueva versión.
        """
        if doc_id not in self.documentos:
            return False
        
        doc = self.documentos[doc_id]
        version_num = len(doc.versiones) + 1
        
        nueva_version = {
            "version": version_num,
            "contenido": contenido_nuevo,
            "timestamp": datetime.now().isoformat(),
            "cambios": cambios_descripcion
        }
        
        doc.versiones.append(nueva_version)
        doc.contenido = contenido_nuevo
        doc.timestamp_ultima_mod = nueva_version["timestamp"]
        doc.estado_indexacion = "actualizado"
        
        # Re-indexar
        self._indexar_documento(doc_id, contenido_nuevo)
        
        return True
    
    def recuperar_documento(self, doc_id: str) -> DocumentoArchivado | None:
        """Recupera documento actual."""
        return self.documentos.get(doc_id)
    
    def obtener_version(self, doc_id: str, version_num: int) -> str | None:
        """Obtiene contenido de versión específica."""
        if doc_id not in self.documentos:
            return None
        
        doc = self.documentos[doc_id]
        for ver in doc.versiones:
            if ver["version"] == version_num:
                return ver["contenido"]
        
        return None
    
    def listar_versiones(self, doc_id: str) -> List[dict] | None:
        """Lista todas las versiones de un documento."""
        if doc_id not in self.documentos:
            return None
        
        doc = self.documentos[doc_id]
        return [
            {
                "version": v["version"],
                "timestamp": v["timestamp"],
                "cambios": v["cambios"]
            }
            for v in doc.versiones
        ]
    
    def buscar_por_tags(self, tags_query: List[str]) -> List[str]:
        """Busca documentos por tags."""
        resultados = []
        for doc_id, doc in self.documentos.items():
            if any(tag in doc.tags for tag in tags_query):
                resultados.append(doc_id)
        return resultados
    
    def buscar_por_tipo(self, tipo: str) -> List[str]:
        """Busca documentos por tipo."""
        return [doc_id for doc_id, doc in self.documentos.items() if doc.tipo == tipo]
    
    def buscar_similitud(self, texto_query: str, k: int = 5) -> List[tuple[str, float]]:
        """
        Búsqueda de similitud simple (sin VectorDB).
        Retorna [(doc_id, similitud), ...]
        """
        palabras_query = set(texto_query.lower().split())
        resultados = []
        
        for indice in self.indices:
            palabras_indice = set(indice.palabras_clave)
            # Similitud Jaccard
            similitud = len(palabras_query & palabras_indice) / len(palabras_query | palabras_indice) if palabras_query | palabras_indice else 0
            resultados.append((indice.documento_id, similitud))
        
        # Ordenar por similitud
        resultados.sort(key=lambda x: x[1], reverse=True)
        return resultados[:k]
    
    def _indexar_documento(self, doc_id: str, contenido: str) -> None:
        """Crea índice para documento (simulado)."""
        # Extrae palabras clave (simulado: top 10 palabras)
        palabras = contenido.lower().split()
        palabras_importantes = [p for p in palabras if len(p) > 4][:10]
        
        # Buscar índice existente y actualizar
        for indice in self.indices:
            if indice.documento_id == doc_id:
                indice.palabras_clave = palabras_importantes
                return
        
        # Crear nuevo índice
        self.indices.append(IndiceVector(
            documento_id=doc_id,
            palabras_clave=palabras_importantes,
            similitud_base=0.5
        ))
    
    def reconstruir_sesion(self, doc_ids: List[str]) -> str:
        """
        Reconstruye sesión completa a partir de documentos.
        """
        documentos = [self.documentos[did] for did in doc_ids if did in self.documentos]
        
        # Ordenar por timestamp
        documentos.sort(key=lambda d: d.timestamp_creacion)
        
        # Compilar contenido
        sesion = []
        for doc in documentos:
            sesion.append(f"\n{'='*60}")
            sesion.append(f"DOC: {doc.id} | TIPO: {doc.tipo}")
            sesion.append(f"TIMESTAMP: {doc.timestamp_creacion}")
            sesion.append(f"TAGS: {', '.join(doc.tags)}")
            sesion.append(f"{'='*60}\n")
            sesion.append(doc.contenido)
        
        return "\n".join(sesion)
    
    def exportar_json(self, doc_id: str) -> str:
        """Exporta documento a JSON."""
        if doc_id not in self.documentos:
            return "{}"
        
        doc = self.documentos[doc_id]
        return json.dumps(doc.to_dict(), indent=2, default=str)
    
    def get_estadisticas(self) -> dict:
        """Retorna estadísticas del archivo."""
        tipos = {}
        total_versiones = 0
        
        for doc in self.documentos.values():
            tipos[doc.tipo] = tipos.get(doc.tipo, 0) + 1
            total_versiones += len(doc.versiones)
        
        return {
            "total_documentos": len(self.documentos),
            "total_versiones": total_versiones,
            "por_tipo": tipos,
            "total_indices": len(self.indices)
        }
    
    def analyze(self, input_text: str) -> dict[str, Any]:
        """Análisis - retorna estadísticas del archivo."""
        return {
            "agent": self.nombre,
            "estadisticas": self.get_estadisticas(),
            "documentos_activos": len(self.documentos)
        }
