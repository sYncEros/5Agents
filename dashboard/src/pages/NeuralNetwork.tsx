import { useState, useCallback, useEffect, useRef } from "react";
import { trpc } from "../lib/trpc";
import { motion, AnimatePresence } from "framer-motion";
import {
  X,
  Activity,
  Brain,
  FileText,
  Zap,
  Send,
  MessageSquare,
  Plus,
  CheckCircle2,
  Clock,
  AlertCircle,
  Upload,
  Image as ImageIcon,
  Mic,
  Video,
  FileUp,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const agentDefinitions = [
  {
    id: "research",
    label: "Research Analyst",
    dept: "Research",
    color: "#3b82f6",
    icon: "🔬",
    specialty: "Análisis de datos y tendencias",
  },
  {
    id: "writer",
    label: "Content Writer",
    dept: "Content",
    color: "#8b5cf6",
    icon: "✍️",
    specialty: "Creación de contenido",
  },
  {
    id: "legal",
    label: "Legal Advisor",
    dept: "Legal",
    color: "#ef4444",
    icon: "⚖️",
    specialty: "Asesoría legal y compliance",
  },
  {
    id: "creative",
    label: "Creative Director",
    dept: "Creative",
    color: "#f59e0b",
    icon: "🎨",
    specialty: "Diseño y creatividad",
  },
  {
    id: "financial",
    label: "Financial Analyst",
    dept: "Finance",
    color: "#10b981",
    icon: "💰",
    specialty: "Análisis financiero",
  },
  {
    id: "data",
    label: "Data Scientist",
    dept: "Data",
    color: "#06b6d4",
    icon: "📊",
    specialty: "Ciencia de datos e IA",
  },
  {
    id: "comms",
    label: "Communications",
    dept: "Comms",
    color: "#ec4899",
    icon: "📢",
    specialty: "Comunicación estratégica",
  },
  {
    id: "strategy",
    label: "Strategic Planner",
    dept: "Strategy",
    color: "#6366f1",
    icon: "🎯",
    specialty: "Planificación estratégica",
  },
  {
    id: "qa",
    label: "Quality Assurance",
    dept: "QA",
    color: "#14b8a6",
    icon: "✅",
    specialty: "Control de calidad",
  },
  {
    id: "knowledge",
    label: "Knowledge Manager",
    dept: "Knowledge",
    color: "#a855f7",
    icon: "📚",
    specialty: "Gestión del conocimiento",
  },
];

type Message = {
  id: string;
  text: string;
  sender: "user" | "agent";
  agentId?: string;
  timestamp: string;
};

type Task = {
  id: string;
  title: string;
  description: string;
  assignedTo: string;
  status: "pending" | "in-progress" | "completed";
  createdAt: string;
};

export default function NeuralNetwork() {
  const [selectedAgent, setSelectedAgent] = useState<any>(null);
  const [showChat, setShowChat] = useState(false);
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      text: "¡Hola! Soy tu asistente AI. Puedo ayudarte a coordinar tareas entre los agentes. ¿En qué puedo ayudarte?",
      sender: "agent",
      timestamp: new Date().toISOString(),
    },
  ]);
  const [inputMessage, setInputMessage] = useState("");
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTask, setNewTask] = useState({
    title: "",
    description: "",
    assignedTo: "",
  });
  const [activeAgents, setActiveAgents] = useState<Set<string>>(new Set());

  // Simular actividad de agentes
  useEffect(() => {
    const interval = setInterval(() => {
      const randomAgent =
        agentDefinitions[Math.floor(Math.random() * agentDefinitions.length)];
      setActiveAgents((prev) => {
        const newSet = new Set(prev);
        if (newSet.has(randomAgent.id)) {
          newSet.delete(randomAgent.id);
        } else {
          newSet.add(randomAgent.id);
        }
        return newSet;
      });
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  const sendMessageMutation = trpc.chat.sendMessage.useMutation();
  const uploadFileMutation = trpc.upload.uploadFile.useMutation();
  const transcribeAudioMutation = trpc.upload.transcribeAudio.useMutation();
  const [isTyping, setIsTyping] = useState(false);
  const [uploadingFile, setUploadingFile] = useState(false);
  const [attachedFiles, setAttachedFiles] = useState<
    Array<{ name: string; url: string; type: string; size: number }>
  >([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isTyping) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputMessage,
      sender: "user",
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    const messageToSend = inputMessage;
    setInputMessage("");
    setIsTyping(true);

    try {
      const response = await sendMessageMutation.mutateAsync({
        content: messageToSend,
        attachments: attachedFiles.length > 0 ? attachedFiles : undefined,
      });

      // Limpiar archivos adjuntos después de enviar
      setAttachedFiles([]);

      const agentMessage: Message = {
        id: response.agentMessageId.toString(),
        text: response.content,
        sender: "agent",
        agentId: response.agentType,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, agentMessage]);

      // Marcar el agente como activo temporalmente
      setActiveAgents((prev) => new Set(prev).add(response.agentType));
      setTimeout(() => {
        setActiveAgents((prev) => {
          const newSet = new Set(prev);
          newSet.delete(response.agentType);
          return newSet;
        });
      }, 3000);
    } catch (error) {
      console.error("Error sending message:", error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "Lo siento, hubo un error al procesar tu mensaje. Por favor intenta de nuevo.",
        sender: "agent",
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleCreateTask = () => {
    if (!newTask.title || !newTask.assignedTo) return;
    const task: Task = {
      id: Date.now().toString(),
      ...newTask,
      status: "pending",
      createdAt: new Date().toISOString(),
    };
    setTasks([...tasks, task]);
    setNewTask({ title: "", description: "", assignedTo: "" });
    setShowTaskForm(false);
  };

  const getAgentData = (agent: any) => {
    if (!agent)
      return {
        thoughts: [],
        outputs: [],
        metrics: { tasksCompleted: 0, tasksInProgress: 0, tasksPending: 0 },
      };

    const agentTasks = tasks.filter((t) => t.assignedTo === agent.id);
    return {
      thoughts: [
        `Analizando patrones en ${agent.dept}...`,
        `Optimizando proceso de ${agent.specialty.toLowerCase()}...`,
        `Colaborando con otros agentes del equipo...`,
      ],
      outputs: [
        `Informe de ${agent.dept} - Actualizado hace 2 min`,
        `Análisis de tendencias - Completado`,
        `Recomendaciones estratégicas - En progreso`,
      ],
      metrics: {
        tasksCompleted: agentTasks.filter((t) => t.status === "completed")
          .length,
        tasksInProgress: agentTasks.filter((t) => t.status === "in-progress")
          .length,
        tasksPending: agentTasks.filter((t) => t.status === "pending").length,
      },
    };
  };

  return (
    <div className="h-screen w-full flex bg-gray-950">
      {/* Visualización de Agentes */}
      <div className="flex-1 relative overflow-auto p-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-5 gap-6">
            {agentDefinitions.map((agent) => (
              <motion.div
                key={agent.id}
                className="cursor-pointer"
                onClick={() => setSelectedAgent(agent)}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <Card
                  className="p-6 flex flex-col items-center gap-3 border-2 transition-all duration-300"
                  style={{
                    background: `linear-gradient(135deg, ${agent.color}ee, ${agent.color}99)`,
                    borderColor: activeAgents.has(agent.id)
                      ? agent.color
                      : "rgba(255,255,255,0.2)",
                    boxShadow: activeAgents.has(agent.id)
                      ? `0 0 30px ${agent.color}88`
                      : "0 4px 12px rgba(0,0,0,0.3)",
                  }}
                >
                  <div className="text-5xl mb-2">{agent.icon}</div>
                  <h3 className="text-white font-bold text-center text-sm leading-tight">
                    {agent.label}
                  </h3>
                  <Badge
                    variant="secondary"
                    className="text-xs bg-white/20 text-white border-0"
                  >
                    {agent.dept}
                  </Badge>
                  {activeAgents.has(agent.id) && (
                    <motion.div
                      className="flex items-center gap-1 text-white text-xs"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                    >
                      <Activity className="w-3 h-3 animate-pulse" />
                      <span>Activo</span>
                    </motion.div>
                  )}
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* Panel Lateral */}
      <AnimatePresence>
        {selectedAgent && (
          <motion.div
            initial={{ x: 400, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: 400, opacity: 0 }}
            className="w-96 bg-gray-900 border-l border-gray-800 flex flex-col overflow-hidden"
          >
            {/* Header */}
            <div
              className="p-4 border-b border-gray-800 flex items-center justify-between"
              style={{
                background: `linear-gradient(135deg, ${selectedAgent.color}33, transparent)`,
              }}
            >
              <div className="flex items-center gap-3">
                <div className="text-3xl">{selectedAgent.icon}</div>
                <div>
                  <h2 className="text-white font-bold">
                    {selectedAgent.label}
                  </h2>
                  <p className="text-gray-400 text-xs">
                    {selectedAgent.specialty}
                  </p>
                </div>
              </div>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setSelectedAgent(null)}
              >
                <X className="w-4 h-4 text-gray-400" />
              </Button>
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {/* Pensamientos */}
              <div className="bg-gray-800 rounded-lg p-3">
                <div className="flex items-center gap-2 mb-3">
                  <Brain className="w-4 h-4 text-purple-400" />
                  <h3 className="font-semibold text-white text-sm">
                    Pensamientos Actuales
                  </h3>
                </div>
                <div className="space-y-2">
                  {getAgentData(selectedAgent).thoughts.map((thought, i) => (
                    <div
                      key={i}
                      className="text-gray-300 text-xs bg-gray-900 rounded p-2"
                    >
                      {thought}
                    </div>
                  ))}
                </div>
              </div>

              {/* Outputs */}
              <div className="bg-gray-800 rounded-lg p-3">
                <div className="flex items-center gap-2 mb-3">
                  <FileText className="w-4 h-4 text-blue-400" />
                  <h3 className="font-semibold text-white text-sm">
                    Outputs Recientes
                  </h3>
                </div>
                <div className="space-y-2">
                  {getAgentData(selectedAgent).outputs.map((output, i) => (
                    <div
                      key={i}
                      className="text-gray-300 text-xs bg-gray-900 rounded p-2 flex items-start gap-2"
                    >
                      <CheckCircle2 className="w-3 h-3 text-green-400 flex-shrink-0 mt-0.5" />
                      <span>{output}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Métricas */}
              <div className="bg-gray-800 rounded-lg p-3">
                <div className="flex items-center gap-2 mb-3">
                  <Zap className="w-4 h-4 text-yellow-400" />
                  <h3 className="font-semibold text-white text-sm">
                    Métricas de Rendimiento
                  </h3>
                </div>
                <div className="grid grid-cols-3 gap-2">
                  <div className="bg-gray-900 rounded p-2 text-center">
                    <p className="text-lg font-bold text-green-400">
                      {getAgentData(selectedAgent).metrics.tasksCompleted}
                    </p>
                    <p className="text-[10px] text-gray-400">Completadas</p>
                  </div>
                  <div className="bg-gray-900 rounded p-2 text-center">
                    <p className="text-lg font-bold text-yellow-400">
                      {getAgentData(selectedAgent).metrics.tasksInProgress}
                    </p>
                    <p className="text-[10px] text-gray-400">En Progreso</p>
                  </div>
                  <div className="bg-gray-900 rounded p-2 text-center">
                    <p className="text-lg font-bold text-gray-400">
                      {getAgentData(selectedAgent).metrics.tasksPending}
                    </p>
                    <p className="text-[10px] text-gray-400">Pendientes</p>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Botones de Acción Flotantes */}
      <div className="fixed bottom-6 right-6 flex flex-col gap-3 z-40">
        <Button
          onClick={() => setShowChat(!showChat)}
          size="lg"
          className="rounded-full w-14 h-14 shadow-2xl bg-gradient-to-br from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700"
        >
          <MessageSquare className="w-6 h-6" />
        </Button>
        <Button
          onClick={() => setShowTaskForm(true)}
          size="lg"
          variant="secondary"
          className="rounded-full w-14 h-14 shadow-xl"
        >
          <Plus className="w-6 h-6" />
        </Button>
      </div>

      {/* Chat Modal */}
      <AnimatePresence>
        {showChat && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="absolute top-20 right-4 w-96 h-[500px] bg-gray-900 border border-gray-800 rounded-lg shadow-2xl flex flex-col z-50"
          >
            <div className="p-4 border-b border-gray-800 flex items-center justify-between">
              <h3 className="text-white font-bold">Chat con AI Team</h3>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setShowChat(false)}
              >
                <X className="w-4 h-4" />
              </Button>
            </div>
            <div className="flex-1 overflow-y-auto p-4 space-y-3">
              {messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg p-3 ${msg.sender === "user" ? "bg-blue-600 text-white" : "bg-gray-800 text-gray-200"}`}
                  >
                    <p className="text-sm">{msg.text}</p>
                  </div>
                </div>
              ))}
              {isTyping && (
                <div className="flex items-start gap-3 mb-4">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white font-bold">
                    AI
                  </div>
                  <div className="flex-1">
                    <div className="bg-gray-800 rounded-lg p-3 inline-block">
                      <div className="flex gap-1">
                        <div
                          className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"
                          style={{ animationDelay: "0ms" }}
                        ></div>
                        <div
                          className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"
                          style={{ animationDelay: "150ms" }}
                        ></div>
                        <div
                          className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"
                          style={{ animationDelay: "300ms" }}
                        ></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
            <div className="p-4 border-t border-gray-800">
              {/* Archivos adjuntos */}
              {attachedFiles.length > 0 && (
                <div className="mb-2 flex flex-wrap gap-2">
                  {attachedFiles.map((file, idx) => (
                    <div
                      key={idx}
                      className="bg-gray-800 rounded px-2 py-1 text-xs flex items-center gap-2"
                    >
                      {file.type.startsWith("image/") && (
                        <ImageIcon className="w-3 h-3" />
                      )}
                      {file.type.startsWith("audio/") && (
                        <Mic className="w-3 h-3" />
                      )}
                      {file.type.startsWith("video/") && (
                        <Video className="w-3 h-3" />
                      )}
                      {!file.type.startsWith("image/") &&
                        !file.type.startsWith("audio/") &&
                        !file.type.startsWith("video/") && (
                          <FileUp className="w-3 h-3" />
                        )}
                      <span className="text-gray-300 truncate max-w-[100px]">
                        {file.name}
                      </span>
                      <button
                        onClick={() =>
                          setAttachedFiles((files) =>
                            files.filter((_, i) => i !== idx),
                          )
                        }
                        className="text-gray-500 hover:text-white"
                      >
                        <X className="w-3 h-3" />
                      </button>
                    </div>
                  ))}
                </div>
              )}
              <div className="flex gap-2">
                <input
                  type="file"
                  ref={fileInputRef}
                  className="hidden"
                  accept="image/*,audio/*,video/*,.pdf,.txt,.md,.docx"
                  onChange={async (e) => {
                    const file = e.target.files?.[0];
                    if (!file) return;

                    // Validar tamaño (máximo 16MB)
                    if (file.size > 16 * 1024 * 1024) {
                      alert("El archivo es demasiado grande. Máximo 16MB.");
                      return;
                    }

                    setUploadingFile(true);

                    try {
                      // Convertir archivo a base64
                      const reader = new FileReader();
                      const fileData = await new Promise<string>(
                        (resolve, reject) => {
                          reader.onload = () => {
                            const base64 = reader.result as string;
                            resolve(base64.split(",")[1]); // Remover prefijo data:...
                          };
                          reader.onerror = reject;
                          reader.readAsDataURL(file);
                        },
                      );

                      // Subir a S3
                      const uploadResult = await uploadFileMutation.mutateAsync(
                        {
                          fileName: file.name,
                          fileType: file.type,
                          fileData,
                        },
                      );

                      // Si es audio, transcribir automáticamente
                      if (file.type.startsWith("audio/")) {
                        const transcription =
                          await transcribeAudioMutation.mutateAsync({
                            audioUrl: uploadResult.url,
                          });

                        // Agregar transcripción al input
                        setInputMessage((prev) =>
                          prev
                            ? `${prev}\n\n[Transcripción del audio]: ${transcription.text}`
                            : `[Transcripción del audio]: ${transcription.text}`,
                        );
                      }

                      setAttachedFiles((prev) => [...prev, uploadResult]);
                    } catch (error) {
                      console.error("Error uploading file:", error);
                      alert(
                        "Error al subir el archivo. Por favor intenta de nuevo.",
                      );
                    } finally {
                      setUploadingFile(false);
                      e.target.value = "";
                    }
                  }}
                />
                <Button
                  onClick={() => fileInputRef.current?.click()}
                  size="icon"
                  variant="ghost"
                  disabled={uploadingFile}
                >
                  {uploadingFile ? (
                    <Activity className="w-4 h-4 animate-spin" />
                  ) : (
                    <Upload className="w-4 h-4" />
                  )}
                </Button>
                <Input
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
                  placeholder="Escribe un mensaje..."
                  className="flex-1"
                />
                <Button
                  onClick={handleSendMessage}
                  size="icon"
                  disabled={isTyping}
                >
                  <Send className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Task Form Modal */}
      <AnimatePresence>
        {showTaskForm && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 bg-black/50 flex items-center justify-center p-4"
            onClick={() => setShowTaskForm(false)}
          >
            <motion.div
              initial={{ scale: 0.95 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.95 }}
              className="bg-gray-900 border border-gray-800 rounded-lg p-6 w-full max-w-md"
              onClick={(e) => e.stopPropagation()}
            >
              <h3 className="text-white font-bold text-lg mb-4">
                Crear Nueva Tarea
              </h3>
              <div className="space-y-4">
                <div>
                  <label className="text-gray-400 text-sm mb-1 block">
                    Título
                  </label>
                  <Input
                    value={newTask.title}
                    onChange={(e) =>
                      setNewTask({ ...newTask, title: e.target.value })
                    }
                    placeholder="Título de la tarea"
                  />
                </div>
                <div>
                  <label className="text-gray-400 text-sm mb-1 block">
                    Descripción
                  </label>
                  <Textarea
                    value={newTask.description}
                    onChange={(e) =>
                      setNewTask({ ...newTask, description: e.target.value })
                    }
                    placeholder="Descripción detallada"
                    rows={3}
                  />
                </div>
                <div>
                  <label className="text-gray-400 text-sm mb-1 block">
                    Asignar a
                  </label>
                  <select
                    value={newTask.assignedTo}
                    onChange={(e) =>
                      setNewTask({ ...newTask, assignedTo: e.target.value })
                    }
                    className="w-full bg-gray-800 border border-gray-700 rounded-md px-3 py-2 text-white"
                  >
                    <option value="">Seleccionar agente</option>
                    {agentDefinitions.map((agent) => (
                      <option key={agent.id} value={agent.id}>
                        {agent.icon} {agent.label}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="flex gap-2 pt-2">
                  <Button onClick={handleCreateTask} className="flex-1">
                    Crear Tarea
                  </Button>
                  <Button
                    onClick={() => setShowTaskForm(false)}
                    variant="outline"
                    className="flex-1"
                  >
                    Cancelar
                  </Button>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
