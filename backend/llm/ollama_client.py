"""Cliente para interactuar con Ollama (LLM local)."""
import os
import subprocess
import json
from typing import Optional, Dict, Any
import requests


class OllamaClient:
    """Cliente para ejecutar LLMs locales con Ollama."""
    
    def __init__(
        self,
        base_url: Optional[str] = None,
        default_model: Optional[str] = None,
    ):
        # Permitir configurar por entorno para evitar valores hardcodeados.
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.default_model = default_model or os.getenv("OLLAMA_DEFAULT_MODEL", "mistral")
        
    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> str:
        """
        Genera una respuesta usando Ollama.
        
        Args:
            prompt: El prompt completo a enviar al modelo
            model: Nombre del modelo (mistral, llama2, phi, etc.)
            temperature: Control de aleatoriedad (0.0-1.0)
            max_tokens: Máximo de tokens a generar
            stream: Si devolver la respuesta en streaming
            
        Returns:
            La respuesta generada por el modelo
        """
        model_to_use = model or self.default_model

        try:
            # Método 1: API REST de Ollama
            response = self._generate_via_api(prompt, model_to_use, temperature, max_tokens)
            return response
        except Exception as e:
            # Fallback: Método CLI
            print(f"API falló, usando CLI: {e}")
            return self._generate_via_cli(prompt, model_to_use, temperature)
    
    def _generate_via_api(
        self,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: Optional[int]
    ) -> str:
        """Genera respuesta usando la API REST de Ollama."""
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False
        }
        
        if max_tokens:
            payload["options"] = {"num_predict": max_tokens}
        
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        return result.get("response", "")
    
    def _generate_via_cli(
        self,
        prompt: str,
        model: str,
        temperature: float
    ) -> str:
        """Genera respuesta usando el CLI de Ollama."""
        try:
            comando = ["ollama", "run", model]
            proceso = subprocess.Popen(
                comando,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            salida, error = proceso.communicate(input=prompt, timeout=120)
            
            if proceso.returncode != 0:
                raise Exception(f"Error en Ollama CLI: {error}")
            
            return salida.strip()
        except FileNotFoundError:
            raise Exception("Ollama no está instalado o no está en el PATH")
        except subprocess.TimeoutExpired:
            proceso.kill()
            raise Exception("Timeout al ejecutar Ollama")
    
    def list_models(self) -> list[str]:
        """Lista los modelos disponibles en Ollama."""
        try:
            url = f"{self.base_url}/api/tags"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
        except Exception as e:
            print(f"Error listando modelos: {e}")
            return []
    
    def is_available(self) -> bool:
        """Verifica si Ollama está disponible."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False