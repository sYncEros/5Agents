/**
 * AgentCard Component - Displays individual agent status and activity
 * Following Single Responsibility Principle
 */

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { motion } from "framer-motion";
import { Loader2 } from "lucide-react";

export interface AgentCardProps {
  name: string;
  description: string;
  icon: string;
  color: string;
  status: "idle" | "thinking" | "active" | "coordinating";
  currentTask?: string;
  lastMessage?: string;
  confidence?: number;
  keywords?: string[];
}

const statusConfig = {
  idle: {
    label: "En espera",
    color: "bg-gray-500",
    animation: false,
  },
  thinking: {
    label: "Pensando",
    color: "bg-yellow-500",
    animation: true,
  },
  active: {
    label: "Activo",
    color: "bg-green-500",
    animation: true,
  },
  coordinating: {
    label: "Coordinando",
    color: "bg-blue-500",
    animation: true,
  },
};

export function AgentCard({
  name,
  description,
  icon,
  color,
  status,
  currentTask,
  lastMessage,
  confidence,
  keywords = [],
}: AgentCardProps) {
  const statusInfo = statusConfig[status];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      whileHover={{ scale: 1.02 }}
      className="h-full"
    >
      <Card className="h-full border-2 hover:shadow-lg transition-all duration-300" style={{ borderColor: color }}>
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              <div
                className="text-4xl flex items-center justify-center w-12 h-12 rounded-lg"
                style={{ backgroundColor: `${color}20` }}
              >
                {icon}
              </div>
              <div>
                <CardTitle className="text-lg">{name}</CardTitle>
                <CardDescription className="text-xs mt-1">{description}</CardDescription>
              </div>
            </div>
            <div className="flex items-center gap-2">
              {statusInfo.animation && (
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                >
                  <Loader2 className="w-4 h-4" style={{ color }} />
                </motion.div>
              )}
              <Badge className={`${statusInfo.color} text-white text-xs`}>
                {statusInfo.label}
              </Badge>
            </div>
          </div>
        </CardHeader>

        <CardContent className="space-y-3">
          {/* Current Task */}
          {currentTask && (
            <div className="space-y-1">
              <p className="text-xs font-semibold text-muted-foreground">Tarea actual:</p>
              <p className="text-sm" style={{ color }}>
                {currentTask}
              </p>
            </div>
          )}

          {/* Last Message */}
          {lastMessage && (
            <div className="space-y-1">
              <p className="text-xs font-semibold text-muted-foreground">Último análisis:</p>
              <p className="text-sm line-clamp-3 text-foreground/80">
                {lastMessage}
              </p>
            </div>
          )}

          {/* Keywords */}
          {keywords.length > 0 && (
            <div className="space-y-2">
              <p className="text-xs font-semibold text-muted-foreground">Palabras clave:</p>
              <div className="flex flex-wrap gap-1">
                {keywords.slice(0, 5).map((keyword, index) => (
                  <Badge
                    key={index}
                    variant="outline"
                    className="text-xs"
                    style={{ borderColor: color, color }}
                  >
                    {keyword}
                  </Badge>
                ))}
              </div>
            </div>
          )}

          {/* Confidence Score */}
          {confidence !== undefined && (
            <div className="space-y-1">
              <div className="flex justify-between items-center">
                <p className="text-xs font-semibold text-muted-foreground">Confianza:</p>
                <p className="text-xs font-bold" style={{ color }}>
                  {Math.round(confidence * 100)}%
                </p>
              </div>
              <div className="w-full bg-muted rounded-full h-2">
                <motion.div
                  className="h-2 rounded-full"
                  style={{ backgroundColor: color }}
                  initial={{ width: 0 }}
                  animate={{ width: `${confidence * 100}%` }}
                  transition={{ duration: 0.5 }}
                />
              </div>
            </div>
          )}

          {/* Pulse indicator when active */}
          {status !== "idle" && (
            <div className="flex items-center gap-2 pt-2">
              <motion.div
                className="w-2 h-2 rounded-full"
                style={{ backgroundColor: color }}
                animate={{ opacity: [1, 0.3, 1] }}
                transition={{ duration: 2, repeat: Infinity }}
              />
              <p className="text-xs text-muted-foreground">
                {status === "thinking" && "Procesando información..."}
                {status === "active" && "Generando análisis..."}
                {status === "coordinating" && "Sincronizando con otros agentes..."}
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}
