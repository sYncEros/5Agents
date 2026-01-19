import { useState } from "react";
import { agentProcess } from "@/lib/agentApi";

export default function AgentDashboard() {
  const [texto, setTexto] = useState("");
  const [resultados, setResultados] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const procesarTexto = async () => {
    setError("");
    setLoading(true);
    try {
      const data = await agentProcess({ text: texto, ritual_opt_in: false });
      setResultados(data);
    } catch (e) {
      setResultados(null);
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">🔍 Panel de Agentes</h1>

      <textarea
        value={texto}
        onChange={(e) => setTexto(e.target.value)}
        className="w-full p-2 border rounded mb-4"
        rows={6}
        placeholder="Escribe el texto aquí..."
      />

      <button
        onClick={procesarTexto}
        disabled={loading || !texto.trim()}
        className="bg-blue-600 disabled:opacity-60 text-white px-4 py-2 rounded"
      >
        {loading ? "Procesando..." : "Ejecutar"}
      </button>

      {error && (
        <div className="mt-4 p-3 border border-red-300 bg-red-50 text-red-800 rounded">
          {error}
        </div>
      )}

      {resultados && (
        <div className="mt-6 space-y-6">
          <div>
            <h2 className="text-xl font-semibold">🤖 Respuestas de agentes</h2>
            <div className="mt-2 space-y-3">
              {Object.entries(resultados.agents || {}).map(([name, response]) => (
                <div key={name} className="border rounded p-3">
                  <div className="font-semibold">{name}</div>
                  <pre className="whitespace-pre-wrap text-sm">{response}</pre>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h2 className="text-xl font-semibold">🧭 Capas detectadas</h2>
            <div className="mt-2">
              {(resultados.analysis?.layers || []).length
                ? resultados.analysis.layers.join(", ")
                : "Sin capas explícitas"}
            </div>
          </div>

          <div>
            <h2 className="text-xl font-semibold">🧪 Rutas sugeridas</h2>
            <div className="mt-2">
              {(resultados.analysis?.routing || []).join(", ")}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
