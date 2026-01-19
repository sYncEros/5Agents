# test_statistics_manager.py

import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime
from backend.core.statistics_manager import StatisticsManager


@pytest.fixture
def temp_stats_file():
    """Crea un archivo temporal para pruebas."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = Path(f.name)
    yield temp_path
    # Cleanup
    if temp_path.exists():
        temp_path.unlink()


class TestStatisticsManager:
    """Suite de tests para StatisticsManager."""
    
    def test_initialization_creates_stats(self, temp_stats_file, monkeypatch):
        """Verifica que se inicialicen estadísticas nuevas."""
        monkeypatch.setattr(
            'backend.core.statistics_manager.STATS_FILE',
            temp_stats_file
        )
        manager = StatisticsManager()
        assert manager.data is not None
        assert manager.data["ideas_processed"] == 0
        assert manager.data["insights_generated"] == 0
        assert manager.data["agents_active"] == 4
    
    def test_increment_ideas_processed(self, temp_stats_file, monkeypatch):
        """Verifica incremento de ideas procesadas."""
        monkeypatch.setattr(
            'backend.core.statistics_manager.STATS_FILE',
            temp_stats_file
        )
        manager = StatisticsManager()
        
        result1 = manager.increment_ideas_processed()
        result2 = manager.increment_ideas_processed()
        
        assert result1 == 1
        assert result2 == 2
        assert manager.get_ideas_processed() == 2
    
    def test_increment_insights_generated(self, temp_stats_file, monkeypatch):
        """Verifica incremento de insights generados."""
        monkeypatch.setattr(
            'backend.core.statistics_manager.STATS_FILE',
            temp_stats_file
        )
        manager = StatisticsManager()
        
        result1 = manager.increment_insights_generated(3)
        result2 = manager.increment_insights_generated(2)
        
        assert result1 == 3
        assert result2 == 5
    
    def test_record_processing(self, temp_stats_file, monkeypatch):
        """Verifica registro de procesamiento."""
        monkeypatch.setattr(
            'backend.core.statistics_manager.STATS_FILE',
            temp_stats_file
        )
        manager = StatisticsManager()
        
        idea = "Test idea for processing"
        responses = {
            "🔬 Científico": "Scientific response",
            "🎨 Creativo": "Creative response"
        }
        
        process_id = manager.record_processing(idea, responses)
        
        assert process_id.startswith("proc_")
        assert manager.get_ideas_processed() == 1
        assert manager.get_insights_generated() == 2
    
    def test_get_processing_history(self, temp_stats_file, monkeypatch):
        """Verifica obtención del histórico."""
        monkeypatch.setattr(
            'backend.core.statistics_manager.STATS_FILE',
            temp_stats_file
        )
        manager = StatisticsManager()
        
        responses1 = {"Agent1": "Response1", "Agent2": "Response2"}
        responses2 = {"Agent1": "Response3"}
        
        manager.record_processing("Idea 1", responses1)
        manager.record_processing("Idea 2", responses2)
        
        history = manager.get_processing_history(limit=10)
        
        assert len(history) == 2
        assert history[0]["input_idea"] == "Idea 1"
        assert history[1]["input_idea"] == "Idea 2"
    
    def test_get_all_stats(self, temp_stats_file, monkeypatch):
        """Verifica obtención de todas las estadísticas."""
        monkeypatch.setattr(
            'backend.core.statistics_manager.STATS_FILE',
            temp_stats_file
        )
        manager = StatisticsManager()
        
        manager.increment_ideas_processed()
        manager.increment_insights_generated(5)
        
        all_stats = manager.get_all_stats()
        
        assert all_stats["ideas_processed"] == 1
        assert all_stats["agents_active"] == 4
        assert all_stats["insights_generated"] == 5
        assert "last_update" in all_stats
    
    def test_persistence(self, temp_stats_file, monkeypatch):
        """Verifica que los datos persistan en archivo."""
        monkeypatch.setattr(
            'backend.core.statistics_manager.STATS_FILE',
            temp_stats_file
        )
        
        # Crear primera instancia y guardar datos
        manager1 = StatisticsManager()
        manager1.increment_ideas_processed()
        manager1.increment_ideas_processed()
        manager1.increment_insights_generated(3)
        manager1.save()
        
        # Crear segunda instancia y verificar que carga datos guardados
        manager2 = StatisticsManager()
        
        assert manager2.get_ideas_processed() == 2
        assert manager2.get_insights_generated() == 3
