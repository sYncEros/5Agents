# statistics_manager.py
"""
Gestor de estadísticas reales usando JSON.
Registra: ideas procesadas, agentes activos, insights generados, resultados.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

# Ruta del archivo de estadísticas
STATS_FILE = Path(__file__).parent.parent.parent / "data" / "statistics.json"


class StatisticsManager:
    """Gestor de estadísticas persistente en JSON."""
    
    def __init__(self):
        """Inicializa el gestor y crea el archivo si no existe."""
        self.stats_file = STATS_FILE
        self._ensure_data_dir()
        self._load_or_create_stats()
    
    def _ensure_data_dir(self):
        """Crea el directorio de datos si no existe."""
        self.stats_file.parent.mkdir(parents=True, exist_ok=True)
    
    def _load_or_create_stats(self):
        """Carga estadísticas existentes o crea nuevas."""
        if self.stats_file.exists():
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                logger.info("Estadísticas cargadas desde archivo existente.")
            except (json.JSONDecodeError, IOError) as e:
                logger.error(f"Error al cargar estadísticas: {e}. Creando nuevo archivo.")
                self.data = self._create_empty_stats()
        else:
            self.data = self._create_empty_stats()
    
    def _create_empty_stats(self) -> Dict[str, Any]:
        """Crea estructura vacía de estadísticas."""
        return {
            "ideas_processed": 0,
            "agents_active": 4,  # Se actualiza dinámicamente
            "insights_generated": 0,
            "processing_history": [],
            "agent_responses": [],
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "version": "1.0"
            }
        }
    
    def save(self):
        """Guarda estadísticas en archivo."""
        self.data["metadata"]["last_updated"] = datetime.now().isoformat()
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            logger.info(f"Estadísticas guardadas en {self.stats_file}")
        except IOError as e:
            logger.error(f"Error al guardar estadísticas: {e}")
    
    def increment_ideas_processed(self) -> int:
        """Incrementa contador de ideas procesadas."""
        self.data["ideas_processed"] += 1
        self.save()
        return self.data["ideas_processed"]
    
    def increment_insights_generated(self, count: int = 1) -> int:
        """Incrementa contador de insights generados."""
        self.data["insights_generated"] += count
        self.save()
        return self.data["insights_generated"]
    
    def get_ideas_processed(self) -> int:
        """Retorna total de ideas procesadas."""
        return self.data["ideas_processed"]
    
    def get_agents_active(self) -> int:
        """Retorna número de agentes activos."""
        return self.data["agents_active"]
    
    def get_insights_generated(self) -> int:
        """Retorna total de insights generados."""
        return self.data["insights_generated"]
    
    def get_recent_increase(self, stat_name: str, days: int = 1) -> int:
        """Calcula incremento reciente de una estadística."""
        history = self.data["processing_history"]
        
        if not history:
            return 0

        if days <= 0:
            return 0

        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent_count = 0
        for entry in history:
            ts = entry.get("timestamp")
            if not ts:
                continue
            try:
                entry_date = datetime.fromisoformat(ts)
            except ValueError:
                continue
            if entry_date >= cutoff_date:
                recent_count += 1
        
        return recent_count
    
    def record_processing(self, idea: str, agent_responses: Dict[str, str]) -> str:
        """Registra el procesamiento de una idea con respuestas de agentes."""
        process_id = f"proc_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        record = {
            "process_id": process_id,
            "timestamp": datetime.now().isoformat(),
            "input_idea": idea,
            "agent_responses": agent_responses,
            "status": "completed"
        }
        
        self.data["processing_history"].append(record)
        # Evita escrituras redundantes: actualiza contadores y guarda una sola vez.
        self.data["ideas_processed"] += 1
        self.data["insights_generated"] += len(agent_responses)
        self.save()
        
        logger.info(f"Procesamiento registrado: {process_id}")
        return process_id
    
    def get_processing_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retorna histórico de procesamiento reciente."""
        return self.data["processing_history"][-limit:]
    
    def get_all_stats(self) -> Dict[str, Any]:
        """Retorna todas las estadísticas."""
        return {
            "ideas_processed": self.get_ideas_processed(),
            "agents_active": self.get_agents_active(),
            "insights_generated": self.get_insights_generated(),
            "recent_increase": self.get_recent_increase("ideas_processed"),
            "last_update": self.data["metadata"]["last_updated"]
        }


# Instancia global
_stats_manager = None


def get_stats_manager() -> StatisticsManager:
    """Retorna la instancia global del gestor de estadísticas."""
    global _stats_manager
    if _stats_manager is None:
        _stats_manager = StatisticsManager()
    return _stats_manager
