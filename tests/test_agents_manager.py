# test_agents_manager.py

import pytest
from unittest.mock import Mock, patch, MagicMock
from components.core.agents_manager import AgentsManager


class TestAgentsManager:
    """Suite de tests para AgentsManager."""
    
    @patch('components.core.agents_manager.Ollama')
    def test_initialization(self, mock_ollama):
        """Verifica inicialización del gestor de agentes."""
        mock_llm_instance = Mock()
        mock_ollama.return_value = mock_llm_instance
        
        manager = AgentsManager(model="test/model")
        
        assert manager.model == "test/model"
        assert manager.llm is not None
        assert len(manager.agents_config) == 4
        mock_ollama.assert_called_once_with(model="test/model")
    
    @patch('components.core.agents_manager.Ollama')
    def test_agents_config_structure(self, mock_ollama):
        """Verifica que la configuración de agentes sea correcta."""
        mock_ollama.return_value = Mock()
        manager = AgentsManager()
        
        expected_agents = {
            "🔬 Científico",
            "🎨 Creativo",
            "🧠 Filósofo",
            "💻 Técnico"
        }
        
        assert set(manager.agents_config.keys()) == expected_agents
        
        # Verificar que cada agente tenga role, goal y backstory
        for agent_name, config in manager.agents_config.items():
            assert "role" in config
            assert "goal" in config
            assert "backstory" in config
            assert len(config["role"]) > 0
            assert len(config["goal"]) > 0
            assert len(config["backstory"]) > 0
    
    @patch('components.core.agents_manager.Ollama')
    def test_get_active_agents(self, mock_ollama):
        """Verifica obtención de agentes activos."""
        mock_ollama.return_value = Mock()
        manager = AgentsManager()
        
        agents = manager.get_active_agents()
        
        assert len(agents) == 4
        assert "🔬 Científico" in agents
        assert "🎨 Creativo" in agents
        assert "🧠 Filósofo" in agents
        assert "💻 Técnico" in agents
    
    @patch('components.core.agents_manager.Ollama')
    def test_get_agents_count(self, mock_ollama):
        """Verifica conteo de agentes."""
        mock_ollama.return_value = Mock()
        manager = AgentsManager()
        
        count = manager.get_agents_count()
        
        assert count == 4
    
    @patch('components.core.agents_manager.Ollama')
    def test_process_idea_empty_input_raises_error(self, mock_ollama):
        """Verifica que idea vacía lance error."""
        mock_ollama.return_value = Mock()
        manager = AgentsManager()
        
        with pytest.raises(ValueError, match="La idea no puede estar vacía"):
            manager.process_idea("")
        
        with pytest.raises(ValueError, match="La idea no puede estar vacía"):
            manager.process_idea("   ")
    
    @patch('components.core.agents_manager.Crew')
    @patch('components.core.agents_manager.Ollama')
    def test_process_idea_success(self, mock_ollama, mock_crew_class):
        """Verifica procesamiento exitoso de una idea."""
        # Setup mocks
        mock_llm = Mock()
        mock_ollama.return_value = mock_llm
        
        mock_crew_instance = Mock()
        mock_crew_instance.kickoff.return_value = "Respuesta de agente"
        mock_crew_class.return_value = mock_crew_instance
        
        manager = AgentsManager()
        
        idea = "Test idea"
        results = manager.process_idea(idea)
        
        # Verificar que retorna dict con 4 agentes
        assert isinstance(results, dict)
        assert len(results) == 4
        
        # Verificar que cada agente tiene una respuesta
        for agent_name in manager.get_active_agents():
            assert agent_name in results
            assert isinstance(results[agent_name], str)
            assert len(results[agent_name]) > 0
    
    @patch('components.core.agents_manager.Crew')
    @patch('components.core.agents_manager.Ollama')
    def test_process_idea_with_error_handling(self, mock_ollama, mock_crew_class):
        """Verifica manejo de errores durante procesamiento."""
        mock_llm = Mock()
        mock_ollama.return_value = mock_llm
        
        # Simular que un crew falla
        mock_crew_instance = Mock()
        mock_crew_instance.kickoff.side_effect = Exception("Test error")
        mock_crew_class.return_value = mock_crew_instance
        
        manager = AgentsManager()
        
        idea = "Test idea"
        results = manager.process_idea(idea)
        
        # Verificar que todas los agentes tengan respuesta (incluso con errores)
        assert len(results) == 4
        assert all("Error" in response for response in results.values())
    
    @patch('components.core.agents_manager.Ollama')
    def test_create_agent(self, mock_ollama):
        """Verifica creación de agentes individuales."""
        mock_llm = Mock()
        mock_ollama.return_value = mock_llm
        
        manager = AgentsManager()
        
        # Crear agente científico
        with patch('components.core.agents_manager.Agent') as mock_agent_class:
            mock_agent_instance = Mock()
            mock_agent_class.return_value = mock_agent_instance
            
            agent = manager._create_agent("🔬 Científico")
            
            # Verificar que se creó con parámetros correctos
            call_kwargs = mock_agent_class.call_args[1]
            assert "Científico" in call_kwargs["role"]
            assert call_kwargs["llm"] == mock_llm
            assert call_kwargs["allow_delegation"] == False
    
    @patch('components.core.agents_manager.Ollama')
    def test_create_analysis_task(self, mock_ollama):
        """Verifica creación de tareas de análisis."""
        mock_llm = Mock()
        mock_ollama.return_value = mock_llm
        
        manager = AgentsManager()
        
        mock_agent = Mock()
        idea = "Test idea"
        agent_name = "🔬 Científico"
        
        with patch('components.core.agents_manager.Task') as mock_task_class:
            mock_task_instance = Mock()
            mock_task_class.return_value = mock_task_instance
            
            task = manager._create_analysis_task(mock_agent, idea, agent_name)
            
            # Verificar que se creó la tarea con parámetros correctos
            call_kwargs = mock_task_class.call_args[1]
            assert idea in call_kwargs["description"]
            assert call_kwargs["agent"] == mock_agent


class TestAgentsManagerIntegration:
    """Tests de integración (requieren Ollama ejecutándose)."""
    
    @pytest.mark.integration
    def test_real_ollama_connection(self):
        """Prueba conexión real con Ollama (saltado si Ollama no está disponible)."""
        try:
            manager = AgentsManager()
            assert manager.llm is not None
            assert manager.get_agents_count() == 4
        except Exception as e:
            pytest.skip(f"Ollama no disponible: {e}")
