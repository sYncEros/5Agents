import { useState, useRef, useEffect } from "react";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { 
  Send,
  Paperclip,
  Brain,
  FileEdit,
  Mail,
  Lightbulb,
  CheckCircle2,
  Clock,
  Zap,
  Activity
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import DataVisualization, { DataPoint, ChartType } from "@/components/DataVisualization";

interface ChatMessage {
  id: string;
  role: "user" | "agent" | "system";
  content: string;
  agentName?: string;
  agentType?: "research" | "writing" | "communication" | "creative";
  timestamp: Date;
  attachments?: { name: string; size: number }[];
  visualization?: {
    type: ChartType;
    data: DataPoint[];
    title: string;
    description?: string;
    source?: string;
  };
}

interface AgentLog {
  id: string;
  stage: "receiving" | "analyzing" | "reasoning" | "proposing" | "done";
  content: string;
  timestamp: Date;
  visualization?: {
    type: ChartType;
    data: DataPoint[];
    title: string;
    description?: string;
    source?: string;
  };
}

interface Agent {
  id: string;
  name: string;
  type: "research" | "writing" | "communication" | "creative";
  status: "idle" | "working" | "done";
  logs: AgentLog[];
}

const agentIcons = {
  research: Brain,
  writing: FileEdit,
  communication: Mail,
  creative: Lightbulb,
};

const agentColors = {
  research: { bg: "bg-blue-500/10", border: "border-blue-500/30", text: "text-blue-400", dot: "bg-blue-500" },
  writing: { bg: "bg-purple-500/10", border: "border-purple-500/30", text: "text-purple-400", dot: "bg-purple-500" },
  communication: { bg: "bg-green-500/10", border: "border-green-500/30", text: "text-green-400", dot: "bg-green-500" },
  creative: { bg: "bg-orange-500/10", border: "border-orange-500/30", text: "text-orange-400", dot: "bg-orange-500" },
};

const stageLabels = {
  receiving: "Recibiendo",
  analyzing: "Analizando",
  reasoning: "Razonando",
  proposing: "Proponiendo",
  done: "Completado",
};

const stageIcons = {
  receiving: Clock,
  analyzing: Brain,
  reasoning: Zap,
  proposing: Lightbulb,
  done: CheckCircle2,
};

export default function MainDashboard() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "1",
      role: "system",
      content: "Hola, soy tu equipo de IA profesional. Sube archivos o pregúntame lo que necesites.",
      timestamp: new Date(),
    },
  ]);
  const [messageInput, setMessageInput] = useState("");
  const [agents, setAgents] = useState<Agent[]>([
    { id: "1", name: "Dr. Insight", type: "research", status: "idle", logs: [] },
    { id: "2", name: "Sofía Escritora", type: "writing", status: "idle", logs: [] },
    { id: "3", name: "Alex Comunicador", type: "communication", status: "idle", logs: [] },
    { id: "4", name: "Luna Creativa", type: "creative", status: "idle", logs: [] },
  ]);
  const [isProcessing, setIsProcessing] = useState(false);
  const chatScrollRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Auto-scroll chat
  useEffect(() => {
    if (chatScrollRef.current) {
      chatScrollRef.current.scrollTop = chatScrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    const fileList = Array.from(files);
    const attachments = fileList.map((f) => ({
      name: f.name,
      size: f.size,
    }));

    const systemMessage: ChatMessage = {
      id: Math.random().toString(36).substr(2, 9),
      role: "system",
      content: `Archivo${fileList.length > 1 ? "s" : ""} cargado${fileList.length > 1 ? "s" : ""}: ${fileList.map((f) => f.name).join(", ")}`,
      timestamp: new Date(),
      attachments,
    };

    setMessages((prev) => [...prev, systemMessage]);
    simulateAgentProcessing(`Analizar archivo: ${fileList[0]?.name}`);
  };

  const sendMessage = () => {
    if (!messageInput.trim()) return;

    const userMessage: ChatMessage = {
      id: Math.random().toString(36).substr(2, 9),
      role: "user",
      content: messageInput,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setMessageInput("");
    simulateAgentProcessing(messageInput);
  };

  const simulateAgentProcessing = (input: string) => {
    setIsProcessing(true);

    // Reset agents
    setAgents((prev) =>
      prev.map((agent) => ({ ...agent, status: "working" as const, logs: [] }))
    );

    // Stage 1: Receiving (all agents)
    agents.forEach((agent, index) => {
      setTimeout(() => {
        setAgents((prev) =>
          prev.map((a) =>
            a.id === agent.id
              ? {
                  ...a,
                  logs: [
                    ...a.logs,
                    {
                      id: Math.random().toString(36).substr(2, 9),
                      stage: "receiving",
                      content: `Recibí: "${input.substring(0, 40)}${input.length > 40 ? "..." : ""}"`,
                      timestamp: new Date(),
                    },
                  ],
                }
              : a
          )
        );
      }, index * 200);
    });

    // Stage 2: Analyzing
    setTimeout(() => {
      agents.forEach((agent, index) => {
        setTimeout(() => {
          setAgents((prev) =>
            prev.map((a) =>
              a.id === agent.id
                ? {
                    ...a,
                    logs: [
                      ...a.logs,
                      {
                        id: Math.random().toString(36).substr(2, 9),
                        stage: "analyzing",
                        content: `Analizando desde perspectiva de ${agent.type}...`,
                        timestamp: new Date(),
                      },
                    ],
                  }
                : a
            )
          );
        }, index * 300);
      });
    }, 1000);

    // Stage 3: Reasoning with visualization
    setTimeout(() => {
      const reasoningContent: Record<string, string> = {
        research: "Identifico necesidad de investigación profunda. Puedo analizar fuentes y generar informe.",
        writing: "Detecto oportunidad de crear documento formal. Propongo generar paper técnico.",
        communication: "Veo necesidad de comunicación externa. Puedo redactar emails profesionales.",
        creative: "Encuentro potencial creativo. Propongo generar visualizaciones o contenido artístico.",
      };

      agents.forEach((agent, index) => {
        setTimeout(() => {
          // Generate mini visualization for research agent
          const miniData: DataPoint[] = agent.type === "research" 
            ? [
                { name: "A", value: 30 },
                { name: "B", value: 50 },
                { name: "C", value: 70 },
              ]
            : [];

          setAgents((prev) =>
            prev.map((a) =>
              a.id === agent.id
                ? {
                    ...a,
                    logs: [
                      ...a.logs,
                      {
                        id: Math.random().toString(36).substr(2, 9),
                        stage: "reasoning",
                        content: reasoningContent[agent.type],
                        timestamp: new Date(),
                        ...(agent.type === "research" && miniData.length > 0
                          ? {
                              visualization: {
                                type: "bar" as ChartType,
                                data: miniData,
                                title: "Datos Preliminares",
                                description: "Análisis inicial",
                                source: "Procesamiento interno",
                              },
                            }
                          : {}),
                      },
                    ],
                  }
                : a
            )
          );
        }, index * 400);
      });
    }, 2500);

    // Stage 4: Proposing (one agent)
    setTimeout(() => {
      const selectedAgent = agents[Math.floor(Math.random() * agents.length)];

      setAgents((prev) =>
        prev.map((a) =>
          a.id === selectedAgent.id
            ? {
                ...a,
                logs: [
                  ...a.logs,
                  {
                    id: Math.random().toString(36).substr(2, 9),
                    stage: "proposing",
                    content: "Propongo crear documento detallado. ¿Apruebas?",
                    timestamp: new Date(),
                  },
                ],
              }
            : a
        )
      );

      // Agent response in chat with visualization
      setTimeout(() => {
        // Generate sample data based on agent type
        const sampleData: DataPoint[] = selectedAgent.type === "research" 
          ? [
              { name: "Enero", value: 45 },
              { name: "Febrero", value: 62 },
              { name: "Marzo", value: 58 },
              { name: "Abril", value: 73 },
              { name: "Mayo", value: 81 },
            ]
          : selectedAgent.type === "creative"
          ? [
              { name: "Concepto A", value: 35 },
              { name: "Concepto B", value: 25 },
              { name: "Concepto C", value: 40 },
            ]
          : [
              { name: "Fase 1", value: 30 },
              { name: "Fase 2", value: 50 },
              { name: "Fase 3", value: 70 },
              { name: "Fase 4", value: 90 },
            ];

        const chartType: ChartType = selectedAgent.type === "creative" ? "pie" : selectedAgent.type === "research" ? "line" : "bar";

        setMessages((prev) => [
          ...prev,
          {
            id: Math.random().toString(36).substr(2, 9),
            role: "agent",
            content: `He analizado tu solicitud. Aquí están mis hallazgos visualizados:`,
            agentName: selectedAgent.name,
            agentType: selectedAgent.type,
            timestamp: new Date(),
            visualization: {
              type: chartType,
              data: sampleData,
              title: "Análisis de Datos",
              description: "Resultados del análisis realizado",
              source: `Análisis de ${selectedAgent.name}`,
            },
          },
        ]);

        // Mark all as done
        setAgents((prev) =>
          prev.map((a) => ({
            ...a,
            status: "done" as const,
            logs: [
              ...a.logs,
              {
                id: Math.random().toString(36).substr(2, 9),
                stage: "done",
                content: a.id === selectedAgent.id ? "Propuesta enviada" : "Análisis completado",
                timestamp: new Date(),
              },
            ],
          }))
        );

        setIsProcessing(false);
      }, 500);
    }, 4500);
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / (1024 * 1024)).toFixed(1) + " MB";
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 flex">
      {/* Left Column: Chat */}
      <div className="w-1/2 flex flex-col border-r border-slate-800">
        {/* Header */}
        <div className="p-6 border-b border-slate-800">
          <h1 className="text-2xl font-bold text-white mb-1">Chat</h1>
          <p className="text-slate-400 text-sm">Conversa con tu equipo de IA</p>
        </div>

        {/* Messages */}
        <ScrollArea className="flex-1 p-6" ref={chatScrollRef}>
          <div className="space-y-4">
            {messages.map((message) => {
              const Icon = message.agentType ? agentIcons[message.agentType] : null;

              return (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`flex gap-3 ${message.role === "user" ? "flex-row-reverse" : ""}`}
                >
                  {/* Avatar */}
                  {message.role !== "user" && (
                    <div
                      className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center border ${
                        message.agentType
                          ? `${agentColors[message.agentType].bg} ${agentColors[message.agentType].border}`
                          : "bg-slate-800 border-slate-700"
                      }`}
                    >
                      {Icon ? <Icon className="w-5 h-5" /> : <Brain className="w-5 h-5 text-slate-400" />}
                    </div>
                  )}

                  {/* Content */}
                  <div className={`flex-1 ${message.role === "user" ? "text-right" : ""}`}>
                    {message.agentName && (
                      <p className="text-xs text-slate-500 mb-1 font-medium">{message.agentName}</p>
                    )}

                    <div className={`${message.role === "user" ? "text-right" : ""}`}>
                      <div
                        className={`inline-block max-w-[85%] rounded-2xl px-4 py-3 ${
                          message.role === "user"
                            ? "bg-gradient-to-r from-blue-600 to-purple-600 text-white"
                            : message.role === "system"
                            ? "bg-slate-800/50 text-slate-400 border border-slate-700"
                            : "bg-slate-800 text-slate-200 border border-slate-700"
                        }`}
                      >
                        <p className="text-sm leading-relaxed">{message.content}</p>

                        {message.attachments && message.attachments.length > 0 && (
                          <div className="mt-2 pt-2 border-t border-slate-700 space-y-1">
                            {message.attachments.map((file, idx) => (
                              <div key={idx} className="flex items-center gap-2 text-xs">
                                <Paperclip className="w-3 h-3" />
                                <span>{file.name}</span>
                                <span className="text-slate-500">({formatFileSize(file.size)})</span>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>

                      {/* Visualization */}
                      {message.visualization && (
                        <div className="mt-3 max-w-[85%] inline-block">
                          <DataVisualization
                            type={message.visualization.type}
                            data={message.visualization.data}
                            title={message.visualization.title}
                            description={message.visualization.description}
                            source={message.visualization.source}
                          />
                        </div>
                      )}
                    </div>

                    <p className="text-xs text-slate-600 mt-1">{message.timestamp.toLocaleTimeString()}</p>
                  </div>

                  {/* User Avatar */}
                  {message.role === "user" && (
                    <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center text-white font-bold text-sm">
                      TÚ
                    </div>
                  )}
                </motion.div>
              );
            })}

            {isProcessing && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-3">
                <div className="flex-shrink-0 w-10 h-10 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center">
                  <Brain className="w-5 h-5 text-slate-400 animate-pulse" />
                </div>
                <div className="flex-1">
                  <div className="inline-block bg-slate-800 border border-slate-700 rounded-2xl px-4 py-3">
                    <div className="flex items-center gap-2">
                      <div className="flex gap-1">
                        <span className="w-2 h-2 bg-slate-500 rounded-full animate-bounce" />
                        <span className="w-2 h-2 bg-slate-500 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                        <span className="w-2 h-2 bg-slate-500 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                      </div>
                      <span className="text-sm text-slate-400">Procesando...</span>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}
          </div>
        </ScrollArea>

        {/* Input */}
        <div className="p-6 border-t border-slate-800">
          <div className="flex gap-3">
            <input ref={fileInputRef} type="file" multiple onChange={handleFileSelect} className="hidden" />
            <Button
              onClick={() => fileInputRef.current?.click()}
              variant="outline"
              size="icon"
              className="border-slate-700 hover:border-slate-600"
            >
              <Paperclip className="w-5 h-5" />
            </Button>

            <Input
              value={messageInput}
              onChange={(e) => setMessageInput(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && !e.shiftKey && sendMessage()}
              placeholder="Escribe un mensaje..."
              className="flex-1 bg-slate-800 border-slate-700 text-white"
            />

            <Button onClick={sendMessage} disabled={!messageInput.trim() || isProcessing} className="bg-gradient-to-r from-blue-600 to-purple-600">
              <Send className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </div>

      {/* Right Column: Agents */}
      <div className="w-1/2 flex flex-col bg-slate-950/50">
        {/* Header */}
        <div className="p-6 border-b border-slate-800">
          <h1 className="text-2xl font-bold text-white mb-1">Equipo Trabajando</h1>
          <p className="text-slate-400 text-sm">Observa el proceso en tiempo real</p>
        </div>

        {/* Agents Grid */}
        <ScrollArea className="flex-1 p-6">
          <div className="grid grid-cols-2 gap-4">
            {agents.map((agent) => {
              const Icon = agentIcons[agent.type];
              const colors = agentColors[agent.type];

              return (
                <motion.div key={agent.id} layout>
                  <Card className={`${colors.bg} border ${colors.border}`}>
                    <CardHeader className="pb-3">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Icon className={`w-5 h-5 ${colors.text}`} />
                          <h3 className="font-semibold text-white text-sm">{agent.name}</h3>
                        </div>
                        <div className="flex items-center gap-2">
                          {agent.status === "working" && (
                            <Activity className={`w-4 h-4 ${colors.text} animate-pulse`} />
                          )}
                          <div className={`w-2 h-2 rounded-full ${agent.status === "working" ? colors.dot + " animate-pulse" : agent.status === "done" ? "bg-green-500" : "bg-slate-600"}`} />
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <ScrollArea className="h-[200px]">
                        {agent.logs.length === 0 ? (
                          <p className="text-xs text-slate-500 italic">En espera...</p>
                        ) : (
                          <div className="space-y-2">
                            {agent.logs.map((log) => {
                              const StageIcon = stageIcons[log.stage];
                              return (
                                <motion.div
                                  key={log.id}
                                  initial={{ opacity: 0, x: -10 }}
                                  animate={{ opacity: 1, x: 0 }}
                                  className="text-xs"
                                >
                                  <div className="flex items-start gap-2 mb-1">
                                    <StageIcon className={`w-3 h-3 ${colors.text} flex-shrink-0 mt-0.5`} />
                                    <Badge variant="outline" className="text-xs border-current">
                                      {stageLabels[log.stage]}
                                    </Badge>
                                  </div>
                                  <p className="text-slate-300 leading-relaxed ml-5">{log.content}</p>
                                  {log.visualization && (
                                    <div className="ml-5 mt-2">
                                      <DataVisualization
                                        type={log.visualization.type}
                                        data={log.visualization.data}
                                        title={log.visualization.title}
                                        description={log.visualization.description}
                                        source={log.visualization.source}
                                      />
                                    </div>
                                  )}
                                  <p className="text-slate-600 text-xs mt-1 ml-5">
                                    {log.timestamp.toLocaleTimeString()}
                                  </p>
                                </motion.div>
                              );
                            })}
                          </div>
                        )}
                      </ScrollArea>
                    </CardContent>
                  </Card>
                </motion.div>
              );
            })}
          </div>
        </ScrollArea>
      </div>
    </div>
  );
}
