/**
 * AgentAvatar Component - Immersive agent visualization
 * Shows agent presence, activity, thoughts, and conversations
 * Following Single Responsibility Principle
 */

import { motion, AnimatePresence } from "framer-motion";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Loader2, MessageCircle, Brain, Activity } from "lucide-react";
import type {
  AgentPersonality,
  AgentActivity,
} from "../../../shared/agent-personalities";
import { useState, useEffect } from "react";

interface AgentAvatarProps {
  personality: AgentPersonality;
  status: "idle" | "thinking" | "active" | "coordinating";
  currentActivity?: AgentActivity;
  currentThought?: string;
  lastMessage?: string;
  onClick?: () => void;
}

const statusConfig = {
  idle: {
    label: "En espera",
    color: "bg-gray-500",
    icon: null,
    animation: "none",
  },
  thinking: {
    label: "Pensando",
    color: "bg-yellow-500",
    icon: Brain,
    animation: "pulse",
  },
  active: {
    label: "Activo",
    color: "bg-green-500",
    icon: Activity,
    animation: "bounce",
  },
  coordinating: {
    label: "Coordinando",
    color: "bg-blue-500",
    icon: MessageCircle,
    animation: "spin",
  },
};

export function AgentAvatar({
  personality,
  status,
  currentActivity,
  currentThought,
  lastMessage,
  onClick,
}: AgentAvatarProps) {
  const [showThought, setShowThought] = useState(false);
  const [showMessage, setShowMessage] = useState(false);
  const config = statusConfig[status];
  const StatusIcon = config.icon;

  // Show thought bubble periodically when thinking
  useEffect(() => {
    if (status === "thinking" && currentThought) {
      setShowThought(true);
      const timer = setTimeout(() => setShowThought(false), 5000);
      return () => clearTimeout(timer);
    }
  }, [status, currentThought]);

  // Show message bubble when there's a new message
  useEffect(() => {
    if (lastMessage) {
      setShowMessage(true);
      const timer = setTimeout(() => setShowMessage(false), 8000);
      return () => clearTimeout(timer);
    }
  }, [lastMessage]);

  return (
    <motion.div
      className="relative"
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      whileHover={{ scale: 1.02 }}
      transition={{ duration: 0.3 }}
    >
      <Card
        className={`p-6 cursor-pointer transition-all duration-300 border-2 hover:shadow-xl ${
          status === "active" ? "border-green-500" : "border-border"
        }`}
        onClick={onClick}
      >
        {/* Agent Header */}
        <div className="flex items-start gap-4 mb-4">
          {/* Avatar with status indicator */}
          <div className="relative">
            <motion.div
              className="text-5xl"
              animate={
                config.animation === "pulse"
                  ? { scale: [1, 1.1, 1] }
                  : config.animation === "bounce"
                    ? { y: [0, -5, 0] }
                    : {}
              }
              transition={{
                duration: 2,
                repeat: Infinity,
                ease: "easeInOut",
              }}
            >
              {personality.avatar}
            </motion.div>

            {/* Status indicator */}
            <motion.div
              className={`absolute -bottom-1 -right-1 w-4 h-4 rounded-full ${config.color} border-2 border-background`}
              animate={
                config.animation === "pulse" ? { scale: [1, 1.3, 1] } : {}
              }
              transition={{
                duration: 1.5,
                repeat: Infinity,
              }}
            />
          </div>

          {/* Agent Info */}
          <div className="flex-1 min-w-0">
            <h3 className="font-bold text-lg">{personality.name}</h3>
            <div className="flex items-center gap-2 mt-1">
              <Badge variant="outline" className="text-xs">
                {config.label}
              </Badge>
              {StatusIcon && (
                <StatusIcon className="w-3 h-3 text-muted-foreground" />
              )}
            </div>
          </div>
        </div>

        {/* Current Activity */}
        {currentActivity && (
          <motion.div
            className="mb-3 p-3 bg-secondary/50 rounded-lg"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <div className="flex items-center gap-2 text-sm">
              <span className="text-lg">{currentActivity.icon}</span>
              <span className="text-muted-foreground">
                {currentActivity.description}
              </span>
            </div>
          </motion.div>
        )}

        {/* Personality Traits */}
        <div className="flex flex-wrap gap-1 mb-3">
          {personality.personality.traits.slice(0, 3).map((trait) => (
            <Badge key={trait} variant="secondary" className="text-xs">
              {trait}
            </Badge>
          ))}
        </div>

        {/* Communication Style */}
        <p className="text-xs text-muted-foreground line-clamp-2">
          {personality.personality.communicationStyle}
        </p>

        {/* Thinking Animation */}
        {status === "thinking" && (
          <motion.div
            className="flex items-center gap-2 mt-3 text-sm text-yellow-500"
            animate={{ opacity: [0.5, 1, 0.5] }}
            transition={{ duration: 1.5, repeat: Infinity }}
          >
            <Loader2 className="w-4 h-4 animate-spin" />
            <span>Analizando...</span>
          </motion.div>
        )}
      </Card>

      {/* Thought Bubble */}
      <AnimatePresence>
        {showThought && currentThought && (
          <motion.div
            className="absolute -top-2 left-1/2 -translate-x-1/2 -translate-y-full z-10"
            initial={{ opacity: 0, y: 10, scale: 0.8 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.8 }}
            transition={{ duration: 0.3 }}
          >
            <div className="relative bg-yellow-100 dark:bg-yellow-900/30 text-yellow-900 dark:text-yellow-100 px-4 py-2 rounded-lg shadow-lg max-w-xs">
              <Brain className="w-3 h-3 inline mr-1" />
              <span className="text-sm italic">{currentThought}</span>
              {/* Bubble tail */}
              <div className="absolute top-full left-1/2 -translate-x-1/2 w-0 h-0 border-l-8 border-r-8 border-t-8 border-transparent border-t-yellow-100 dark:border-t-yellow-900/30" />
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Message Bubble */}
      <AnimatePresence>
        {showMessage && lastMessage && (
          <motion.div
            className="absolute -bottom-2 left-1/2 -translate-x-1/2 translate-y-full z-10"
            initial={{ opacity: 0, y: -10, scale: 0.8 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 10, scale: 0.8 }}
            transition={{ duration: 0.3 }}
          >
            <div className="relative bg-blue-100 dark:bg-blue-900/30 text-blue-900 dark:text-blue-100 px-4 py-2 rounded-lg shadow-lg max-w-xs">
              <MessageCircle className="w-3 h-3 inline mr-1" />
              <span className="text-sm">{lastMessage}</span>
              {/* Bubble tail */}
              <div className="absolute bottom-full left-1/2 -translate-x-1/2 w-0 h-0 border-l-8 border-r-8 border-b-8 border-transparent border-b-blue-100 dark:border-b-blue-900/30" />
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
