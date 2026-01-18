import { useState } from 'react';

export default function AgentDashboard() {
  const [texto, setTexto] = useState('');
  const [resultados, setResultados] = useState(null);

  const procesarTexto = async () => {
    const res = await fetch('http://localhost:8000/procesar/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ texto }),
    });
    const data = await res.json();
    setResultados(data);
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">🔍 Panel de Agentes Cognitivos</h1>
      <textarea
        value={texto}
        onChange={(e) => setTexto(e.target.value)}
        className="w-full p-2 border rounded mb-4"
        rows={6}
        placeholder="Escribe el texto aquí..."
      />
      <button
        onClick={procesarTexto}
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        Ejecutar
      </button>

      {resultados && (
        <div className="mt-6">
          <h2 className="text-xl font-semibold">📚 Temas detectados:</h2>
          <ul className="list-disc ml-6">
            {resultados.temas.map((t, i) => (
              <li key={i}>{t}</li>
            ))}
          </ul>

          {resultados.resultados.map((res, i) => (
            <div key={i} className="mt-4 border-t pt-4">
              <h3 className="font-bold text-lg">{res.topic}</h3>
              <pre className="bg-gray-100 p-2 whitespace-pre-wrap">{res.paper}</pre>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
