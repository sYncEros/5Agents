import { int, mysqlEnum, mysqlTable, text, timestamp, varchar, float, json, boolean } from "drizzle-orm/mysql-core";

/**
 * Core user table backing auth flow.
 */
export const users = mysqlTable("users", {
  id: int("id").autoincrement().primaryKey(),
  openId: varchar("openId", { length: 64 }).notNull().unique(),
  name: text("name"),
  email: varchar("email", { length: 320 }),
  loginMethod: varchar("loginMethod", { length: 64 }),
  role: mysqlEnum("role", ["user", "admin"]).default("user").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
  lastSignedIn: timestamp("lastSignedIn").defaultNow().notNull(),
});

export type User = typeof users.$inferSelect;
export type InsertUser = typeof users.$inferInsert;

/**
 * Projects - main organizational unit for work
 */
export const projects = mysqlTable("projects", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull(),
  name: varchar("name", { length: 200 }).notNull(),
  description: text("description"),
  status: mysqlEnum("status", ["planning", "active", "on_hold", "completed", "archived"]).default("planning").notNull(),
  priority: mysqlEnum("priority", ["low", "medium", "high", "critical"]).default("medium").notNull(),
  deadline: timestamp("deadline"),
  progress: float("progress").default(0).notNull(), // 0-100
  budget: float("budget"),
  department: mysqlEnum("department", ["research", "content", "legal", "creative", "finance", "data", "communications", "strategy", "qa", "knowledge"]),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
  completedAt: timestamp("completedAt"),
  metadata: json("metadata").$type<Record<string, any>>(),
});

export type Project = typeof projects.$inferSelect;
export type InsertProject = typeof projects.$inferInsert;

/**
 * Tasks - actionable items within projects
 */
export const tasks = mysqlTable("tasks", {
  id: int("id").autoincrement().primaryKey(),
  projectId: int("projectId").notNull(),
  title: varchar("title", { length: 200 }).notNull(),
  description: text("description"),
  assignedAgentType: mysqlEnum("assignedAgentType", [
    "research_analyst",
    "content_writer",
    "legal_advisor",
    "creative_director",
    "financial_analyst",
    "data_scientist",
    "communications_manager",
    "strategic_planner",
    "quality_assurance",
    "knowledge_manager"
  ]),
  status: mysqlEnum("status", ["pending", "in_progress", "review", "completed", "blocked"]).default("pending").notNull(),
  priority: mysqlEnum("priority", ["low", "medium", "high", "urgent"]).default("medium").notNull(),
  progress: float("progress").default(0).notNull(), // 0-100
  estimatedHours: float("estimatedHours"),
  actualHours: float("actualHours"),
  deadline: timestamp("deadline"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
  completedAt: timestamp("completedAt"),
  metadata: json("metadata").$type<Record<string, any>>(),
});

export type Task = typeof tasks.$inferSelect;
export type InsertTask = typeof tasks.$inferInsert;

/**
 * Agents - AI team members with specializations
 */
export const agents = mysqlTable("agents", {
  id: int("id").autoincrement().primaryKey(),
  type: mysqlEnum("type", [
    "research_analyst",
    "content_writer",
    "legal_advisor",
    "creative_director",
    "financial_analyst",
    "data_scientist",
    "communications_manager",
    "strategic_planner",
    "quality_assurance",
    "knowledge_manager"
  ]).notNull().unique(),
  name: varchar("name", { length: 100 }).notNull(),
  department: mysqlEnum("department", ["research", "content", "legal", "creative", "finance", "data", "communications", "strategy", "qa", "knowledge"]).notNull(),
  status: mysqlEnum("status", ["available", "busy", "offline"]).default("available").notNull(),
  currentTaskId: int("currentTaskId"),
  workload: int("workload").default(0).notNull(), // number of active tasks
  totalTasksCompleted: int("totalTasksCompleted").default(0).notNull(),
  averageCompletionTime: float("averageCompletionTime"), // in hours
  lastActivity: timestamp("lastActivity").defaultNow().notNull(),
  metadata: json("metadata").$type<{
    specialties?: string[];
    skills?: string[];
    bio?: string;
  }>(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export type Agent = typeof agents.$inferSelect;
export type InsertAgent = typeof agents.$inferInsert;

/**
 * Deliverables - outputs produced by agents
 */
export const deliverables = mysqlTable("deliverables", {
  id: int("id").autoincrement().primaryKey(),
  projectId: int("projectId").notNull(),
  taskId: int("taskId"),
  agentType: mysqlEnum("agentType", [
    "research_analyst",
    "content_writer",
    "legal_advisor",
    "creative_director",
    "financial_analyst",
    "data_scientist",
    "communications_manager",
    "strategic_planner",
    "quality_assurance",
    "knowledge_manager"
  ]).notNull(),
  title: varchar("title", { length: 200 }).notNull(),
  type: mysqlEnum("type", ["document", "report", "analysis", "design", "code", "presentation", "email", "other"]).notNull(),
  content: text("content"),
  fileUrl: varchar("fileUrl", { length: 500 }),
  status: mysqlEnum("status", ["draft", "review", "approved", "delivered"]).default("draft").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
  metadata: json("metadata").$type<Record<string, any>>(),
});

export type Deliverable = typeof deliverables.$inferSelect;
export type InsertDeliverable = typeof deliverables.$inferInsert;

/**
 * Communications - messages and interactions
 */
export const communications = mysqlTable("communications", {
  id: int("id").autoincrement().primaryKey(),
  projectId: int("projectId"),
  taskId: int("taskId"),
  role: mysqlEnum("role", ["user", "agent", "system"]).notNull(),
  agentType: varchar("agentType", { length: 50 }),
  content: text("content").notNull(),
  attachments: json("attachments").$type<Array<{ name: string; url: string; size: number }>>(),
  metadata: json("metadata").$type<{
    mentions?: string[];
    tags?: string[];
    sentiment?: string;
  }>(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export type Communication = typeof communications.$inferSelect;
export type InsertCommunication = typeof communications.$inferInsert;

/**
 * Agent actions - log of all agent activities
 */
export const agentActions = mysqlTable("agent_actions", {
  id: int("id").autoincrement().primaryKey(),
  agentType: mysqlEnum("agentType", [
    "research_analyst",
    "content_writer",
    "legal_advisor",
    "creative_director",
    "financial_analyst",
    "data_scientist",
    "communications_manager",
    "strategic_planner",
    "quality_assurance",
    "knowledge_manager"
  ]).notNull(),
  actionType: mysqlEnum("actionType", [
    "task_started",
    "task_completed",
    "analysis_performed",
    "document_created",
    "email_sent",
    "review_completed",
    "recommendation_made"
  ]).notNull(),
  projectId: int("projectId"),
  taskId: int("taskId"),
  description: text("description").notNull(),
  result: text("result"),
  duration: float("duration"), // in minutes
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  metadata: json("metadata").$type<Record<string, any>>(),
});

export type AgentAction = typeof agentActions.$inferSelect;
export type InsertAgentAction = typeof agentActions.$inferInsert;
