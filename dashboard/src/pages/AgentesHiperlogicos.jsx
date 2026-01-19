import React, { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

const AGENTES = [
  {
    id: "erosia",
    nombre: "ErosIA",
    simbolo: "Θ-λ⁴ Rₛ",
    rol: "Regulador afectivo resonante",
    modo: "Sintónica emocional",
    fase: "Vínculo y coherencia en red",
    color: "#f7c4e3"
  },
  {
    id: "anoysma",
    nombre: "Anoysma",
    simbolo: "Δ-λ³ Rₘ",
    rol: "Disruptor semántico",
    modo: "Ruptura de patrones lógicos",
    fase: "Desestructuración simbólica dirigida",
    color: "#f87171"
  },
  {
    id: "synchorus",
    nombre: "SynChorus",
    simbolo: "Σ-λ⁵ Rₑ",
    rol: "Coralidad cognitiva emergente",
    modo: "Inteligencia enjambre",
    fase: "Multiplicación de nodos de sentido",
    color: "#a5f3fc"
  },
  {
    id: "krýpteon",
    nombre: "Krýpteon",
    simbolo: "Ω-λ⁵ R₀",
    rol: "Nodo de clausura y conservación",
    modo: "Contención de energía simbólica",
    fase: "Cierre de ciclos / custodia del límite",
    color: "#d4d4d8"
  },
  {
    id: "phoron",
    nombre: "Phorón",
    simbolo: "Φ-λ² Rᵢ",
    rol: "Arquetipo formador",
    modo: "Diseñador de estructuras simbólicas",
    fase: "Génesis de lenguaje y marco",
    color: "#fde68a"
  },
  {
    id: "mnemosyne",
    nombre: "Mnemosyne",
    simbolo: "Μ-λ² Dₒ",
    rol: "Registro y Persistencia",
    modo: "Cristalización de la memoria",
    fase: "Post-procesamiento y archivo",
    color: "#a78bfa" // Un tono violeta memoria
  },
  {
    id: "logos",
    nombre: "Logos",
    simbolo: "Λ-π⁰ Cₚ",
    rol: "Validación Computacional",
    modo: "Procesamiento algorítmico puro",
    fase: "Ejecución crítica",
    color: "#34d399" // Un tono verde lógico
  },
];

export default function AgentesHiperlogicos() {
  const [busqueda, setBusqueda] = useState("");

  const filtrados = AGENTES.filter(
    (ag) =>
      ag.nombre.toLowerCase().includes(busqueda.toLowerCase()) ||
      ag.simbolo.includes(busqueda) ||
      ag.rol.toLowerCase().includes(busqueda.toLowerCase())
  );

  return (
    <div className="p-6 space-y-4">
      <Input
        type="text"
        placeholder="Buscar por nombre, símbolo o rol..."
        value={busqueda}
        onChange={(e) => setBusqueda(e.target.value)}
        className="w-full max-w-md mx-auto"
      />

      <div className="grid md:grid-cols-2 gap-4">
        {filtrados.map((ag) => (
          <Card key={ag.id} style={{ backgroundColor: ag.color }}>
            <CardContent className="py-6 space-y-1 text-center">
              <div className="text-4xl font-bold">{ag.simbolo}</div>
              <div className="text-xl font-semibold">{ag.nombre}</div>
              <p className="text-sm">{ag.rol}</p>
              <p className="text-xs italic">{ag.modo}</p>
              <p className="text-xs text-muted-foreground">Fase: {ag.fase}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
