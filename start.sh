#!/bin/bash

# Script de inicio para el Backend de Agentes IA
# Uso: ./start.sh [development|production]

set -e

MODE=${1:-development}
PORT=${PORT:-5000}
HOST=${HOST:-0.0.0.0}

echo "🚀 Iniciando Backend de Agentes IA..."
echo "📍 Modo: $MODE"
echo "🌐 Host: $HOST"
echo "🔌 Puerto: $PORT"

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt

# Configurar variables de entorno
export FLASK_APP=app.py
export FLASK_ENV=$MODE

if [ "$MODE" = "development" ]; then
    export FLASK_DEBUG=1
    echo "🐛 Modo desarrollo activado"
else
    export FLASK_DEBUG=0
    echo "🏭 Modo producción activado"
fi

# Verificar conectividad
echo "🔍 Verificando configuración..."
python3 -c "
import sys
print(f'✅ Python: {sys.version}')
try:
    import flask
    print(f'✅ Flask: {flask.__version__}')
except ImportError:
    print('❌ Flask no instalado')
    sys.exit(1)

try:
    import socketio
    print(f'✅ SocketIO: {socketio.__version__}')
except ImportError:
    print('❌ SocketIO no instalado')
    sys.exit(1)
"

echo ""
echo "🎯 Agentes disponibles:"
echo "   🧠 Filósofo Especulativo"
echo "   🔬 Diseñador de Experimentos"  
echo "   🔧 Ingeniero de Prototipos"
echo "   📚 Historiador de las Ideas"
echo "   🌐 Modelador de Sistemas"

echo ""
echo "🌟 Servidor iniciando en http://$HOST:$PORT"
echo "📡 WebSocket disponible en ws://$HOST:$PORT"
echo "🔗 API endpoints:"
echo "   GET  /api/health"
echo "   POST /api/ideas/process"
echo "   GET  /api/agents/status"
echo "   GET  /api/analysis/history"
echo ""
echo "⏹️  Para detener: Ctrl+C"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Iniciar servidor
python3 app.py
