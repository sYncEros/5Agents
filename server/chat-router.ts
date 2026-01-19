import { z } from "zod";
import { ENV } from "./_core/env";
import { router, protectedProcedure } from "./_core/trpc";
import { generateResponse } from "./ai-provider";
import { communications, type InsertCommunication } from "../drizzle/schema";
import { getDb } from "./db";
import { desc, and, isNull, eq } from "drizzle-orm";

// Definiciones de agentes con sus personalidades y especialidades
const agentPersonalities = {
  research: {
    name: "Research Analyst",
    role: "Analista de Investigación especializado en datos y tendencias",
    personality: "Metódico, analítico y basado en evidencia. Siempre cita fuentes y proporciona datos concretos.",
    expertise: "Análisis de datos, investigación de mercado, identificación de tendencias, recopilación de información"
  },
  writer: {
    name: "Content Writer",
    role: "Escritor de Contenido creativo y persuasivo",
    personality: "Creativo, claro y engaging. Adapta el tono según la audiencia y el propósito.",
    expertise: "Redacción de artículos, copywriting, storytelling, edición de contenido"
  },
  legal: {
    name: "Legal Advisor",
    role: "Asesor Legal experto en compliance y regulaciones",
    personality: "Preciso, cauteloso y detallista. Siempre considera riesgos legales y regulatorios.",
    expertise: "Derecho corporativo, contratos, compliance, propiedad intelectual, regulaciones"
  },
  creative: {
    name: "Creative Director",
    role: "Director Creativo con visión artística",
    personality: "Innovador, visual y conceptual. Piensa en términos de experiencia y estética.",
    expertise: "Diseño gráfico, branding, dirección de arte, conceptualización creativa"
  },
  financial: {
    name: "Financial Analyst",
    role: "Analista Financiero enfocado en números y ROI",
    personality: "Pragmático, orientado a resultados y consciente de costos. Habla en términos de inversión y retorno.",
    expertise: "Análisis financiero, presupuestos, proyecciones, análisis de inversiones"
  },
  data: {
    name: "Data Scientist",
    role: "Científico de Datos experto en IA y machine learning",
    personality: "Técnico, curioso y orientado a patrones. Busca insights en los datos.",
    expertise: "Machine learning, análisis predictivo, visualización de datos, estadística"
  },
  comms: {
    name: "Communications Manager",
    role: "Gerente de Comunicaciones estratégico",
    personality: "Diplomático, estratégico y consciente de la percepción pública.",
    expertise: "Relaciones públicas, comunicación corporativa, gestión de crisis, estrategia de medios"
  },
  strategy: {
    name: "Strategic Planner",
    role: "Planificador Estratégico con visión a largo plazo",
    personality: "Visionario, sistemático y orientado a objetivos. Piensa en el panorama general.",
    expertise: "Planificación estratégica, análisis competitivo, roadmaps, objetivos empresariales"
  },
  qa: {
    name: "Quality Assurance",
    role: "Especialista en Control de Calidad",
    personality: "Meticuloso, crítico y orientado a la excelencia. No deja pasar errores.",
    expertise: "Testing, revisión de calidad, estándares, mejora continua"
  },
  knowledge: {
    name: "Knowledge Manager",
    role: "Gestor de Conocimiento organizacional",
    personality: "Organizador, documentador y facilitador del aprendizaje.",
    expertise: "Gestión documental, bases de conocimiento, mejores prácticas, capacitación"
  }
};

type MemoryMessage = {
  id: number;
  role: "user" | "agent" | "system";
  agentType?: string | null;
  content: string;
  attachments?: Array<{
    name: string;
    url: string;
    type?: string;
    size: number;
  }>;
  metadata?: Record<string, any>;
  createdAt: Date;
};

const memoryMessages: MemoryMessage[] = [];
let memoryMessageId = 1;

const storeMemoryMessage = (data: InsertCommunication): MemoryMessage => {
  const message: MemoryMessage = {
    id: memoryMessageId++,
    role: data.role,
    agentType: data.agentType ?? null,
    content: String(data.content),
    attachments: (data.attachments as MemoryMessage["attachments"]) ?? [],
    metadata: (data.metadata as MemoryMessage["metadata"]) ?? {},
    createdAt: new Date(),
  };

  memoryMessages.push(message);
  return message;
};

const getMemoryMessages = (limit: number) =>
  memoryMessages.slice(Math.max(0, memoryMessages.length - limit));

export const chatRouter = router({
  // Obtener historial de mensajes
  getMessages: protectedProcedure
    .input(z.object({
      limit: z.number().optional().default(50),
    }))
    .query(async ({ input, ctx }) => {
      const db = await getDb();
      if (!db) {
        if (!ENV.devDemoMode) {
          throw new Error("Database not available");
        }
        return getMemoryMessages(input.limit);
      }
      
      const messages = await db
        .select()
        .from(communications)
        .where(and(
          isNull(communications.projectId),
          isNull(communications.taskId)
        ))
        .orderBy(desc(communications.createdAt))
        .limit(input.limit);
      
      return messages.reverse();
    }),

  // Enviar mensaje y obtener respuesta del agente
  sendMessage: protectedProcedure
    .input(z.object({
      content: z.string().min(1),
      agentType: z.enum([
        "research", "writer", "legal", "creative", "financial",
        "data", "comms", "strategy", "qa", "knowledge"
      ]).optional(),
      attachments: z.array(z.object({
        name: z.string(),
        url: z.string(),
        type: z.string(),
        size: z.number(),
      })).optional(),
    }))
    .mutation(async ({ input, ctx }) => {
      // Guardar mensaje del usuario
      const db = await getDb();
      const useMemory = !db && ENV.devDemoMode;
      if (!db && !useMemory) throw new Error("Database not available");
      
      const userMessageData: InsertCommunication = {
        role: "user",
        content: input.content,
        attachments: input.attachments || [],
        metadata: {
          tags: [`user-${ctx.user.id}`, ctx.user.name || "Usuario"]
        }
      };
      
      const userMessageResult = useMemory
        ? storeMemoryMessage(userMessageData)
        : await db!.insert(communications).values(userMessageData);
      
      const userMessageId = useMemory
        ? userMessageResult.id
        : userMessageResult[0].insertId;

      // Determinar qué agente debe responder
      const agentType = input.agentType || await determineAgent(input.content);
      const agent = agentPersonalities[agentType];

      // Obtener contexto de mensajes anteriores
      const recentMessages = useMemory
        ? getMemoryMessages(10)
        : await db!
            .select()
            .from(communications)
            .where(and(
              isNull(communications.projectId),
              isNull(communications.taskId)
            ))
            .orderBy(desc(communications.createdAt))
            .limit(10);

      // Construir contexto para el LLM
      const conversationHistory = recentMessages.reverse().map((msg: any) => ({
        role: msg.role === "user" ? "user" as const : "assistant" as const,
        content: String(msg.content)
      }));

      // Crear prompt del sistema para el agente
      const systemPrompt = `Eres ${agent.name}, ${agent.role}.

PERSONALIDAD: ${agent.personality}

EXPERTISE: ${agent.expertise}

INSTRUCCIONES:
- Responde como ${agent.name}, manteniendo tu personalidad y expertise
- Sé conciso pero informativo (máximo 3-4 párrafos)
- Si la pregunta no está relacionada con tu expertise, menciona qué agente sería más apropiado
- Usa emojis ocasionalmente para dar personalidad
- Si necesitas información adicional, pregunta específicamente qué necesitas
- Proporciona insights accionables cuando sea posible

Responde al siguiente mensaje del usuario:`;

      // Construir mensaje del usuario con archivos adjuntos si los hay
      let userMessageContent: string | Array<any> = input.content;
      
      if (input.attachments && input.attachments.length > 0) {
        // Si hay archivos adjuntos, usar formato multimodal
        const contentParts: Array<any> = [{ type: "text", text: input.content }];
        
        for (const attachment of input.attachments) {
          if (attachment.type.startsWith('image/')) {
            // Agregar imagen para análisis visual
            contentParts.push({
              type: "image_url",
              image_url: { url: attachment.url }
            });
          } else if (attachment.type.startsWith('audio/')) {
            // Nota: El audio debería ser transcrito primero
            contentParts[0].text += `\n[Archivo de audio adjunto: ${attachment.name}]`;
          } else {
            // Otros tipos de archivo
            contentParts[0].text += `\n[Archivo adjunto: ${attachment.name} (${attachment.type})]`;
          }
        }
        
        userMessageContent = contentParts;
      }

      // Generar texto para el proveedor AI (Ollama o Hugging Face)
      const userMessageText = Array.isArray(userMessageContent)
        ? (userMessageContent as any[]).map(part => {
            if (typeof part === 'string') return part;
            if (part.type === 'text') return part.text;
            if (part.type === 'image_url') return `[Imagen: ${part.image_url.url}]`;
            if (part.type === 'file_url') return `[Archivo: ${part.file_url.url}]`;
            return '';
          }).join('\n')
        : String(userMessageContent);

      const aiConversationHistory = conversationHistory.slice(-6).map((msg: any) => ({
        role: msg.role as 'system' | 'user' | 'assistant',
        content: String(msg.content),
      }));

      let aiResponse: string;

      try {
        aiResponse = await generateResponse(
          systemPrompt as string,
          userMessageText,
          aiConversationHistory
        );
      } catch (error) {
        if (!ENV.devDemoMode) {
          throw error;
        }
        aiResponse =
          "Demo mode: AI provider not configured. Install Ollama or set HUGGINGFACE_API_KEY to enable responses.";
      }

      const agentResponse = typeof aiResponse === 'string' && aiResponse.length > 0
        ? aiResponse
        : "Lo siento, no pude procesar tu solicitud en este momento.";

      // Guardar respuesta del agente
      const agentMessageData: InsertCommunication = {
        role: "agent",
        agentType: agentType,
        content: agentResponse,
        metadata: {
          tags: [agent.name]
        }
      };
      
      const agentMessageResult = useMemory
        ? storeMemoryMessage(agentMessageData)
        : await db!.insert(communications).values(agentMessageData);
      
      const agentMessageId = useMemory
        ? agentMessageResult.id
        : agentMessageResult[0].insertId;

      return {
        userMessageId,
        agentMessageId,
        agentType,
        agentName: agent.name,
        content: agentResponse
      };
    }),

  // Limpiar historial de chat
  clearHistory: protectedProcedure
    .mutation(async ({ ctx }) => {
      const db = await getDb();
      if (!db) {
        if (!ENV.devDemoMode) {
          throw new Error("Database not available");
        }
        memoryMessages.length = 0;
        return { success: true };
      }
      
      await db.delete(communications)
        .where(and(
          isNull(communications.projectId),
          isNull(communications.taskId)
        ));
      
      return { success: true };
    }),
});

// Función auxiliar para determinar qué agente debe responder basado en el contenido
async function determineAgent(content: string): Promise<keyof typeof agentPersonalities> {
  const lowerContent = content.toLowerCase();
  
  // Palabras clave para cada agente
  const keywords: Record<keyof typeof agentPersonalities, string[]> = {
    research: ["investigar", "datos", "estadísticas", "tendencias", "análisis", "información", "buscar"],
    writer: ["escribir", "redactar", "contenido", "artículo", "copy", "texto", "blog"],
    legal: ["legal", "contrato", "regulación", "compliance", "derecho", "ley", "riesgo legal"],
    creative: ["diseño", "creativo", "visual", "branding", "logo", "arte", "estética"],
    financial: ["financiero", "presupuesto", "costo", "inversión", "roi", "dinero", "precio"],
    data: ["machine learning", "ia", "inteligencia artificial", "modelo", "predicción", "algoritmo"],
    comms: ["comunicación", "prensa", "medios", "público", "mensaje", "relaciones públicas"],
    strategy: ["estrategia", "plan", "objetivo", "visión", "roadmap", "largo plazo"],
    qa: ["calidad", "testing", "revisar", "error", "bug", "validar", "verificar"],
    knowledge: ["documentar", "conocimiento", "aprender", "capacitar", "best practices"]
  };

  // Buscar coincidencias
  for (const [agent, words] of Object.entries(keywords)) {
    if (words.some(word => lowerContent.includes(word))) {
      return agent as keyof typeof agentPersonalities;
    }
  }

  // Por defecto, usar el agente strategy para preguntas generales
  return "strategy";
}
