CREATE TABLE `agent_assignments` (
	`id` int AUTO_INCREMENT NOT NULL,
	`objectiveId` int NOT NULL,
	`agentType` enum('research','design','connections','tracking','wellness','impact') NOT NULL,
	`status` enum('idle','thinking','active','coordinating') NOT NULL DEFAULT 'idle',
	`currentTask` text,
	`lastActivity` timestamp NOT NULL DEFAULT (now()),
	`assignedAt` timestamp NOT NULL DEFAULT (now()),
	`metadata` json,
	CONSTRAINT `agent_assignments_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `agent_conversations` (
	`id` int AUTO_INCREMENT NOT NULL,
	`objectiveId` int,
	`agentType` enum('research','design','connections','tracking','wellness','impact','coordinator') NOT NULL,
	`role` enum('system','agent','user') NOT NULL,
	`content` text NOT NULL,
	`metadata` json,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	CONSTRAINT `agent_conversations_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `coordination_cycles` (
	`id` int AUTO_INCREMENT NOT NULL,
	`userId` int NOT NULL,
	`cycleType` enum('daily','weekly','on_demand') NOT NULL,
	`status` enum('running','completed','failed') NOT NULL DEFAULT 'running',
	`summary` text,
	`agentsInvolved` json,
	`objectivesAnalyzed` int DEFAULT 0,
	`synergiesDetected` int DEFAULT 0,
	`wellnessScore` float,
	`startedAt` timestamp NOT NULL DEFAULT (now()),
	`completedAt` timestamp,
	`metadata` json,
	CONSTRAINT `coordination_cycles_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `coral_chat_messages` (
	`id` int AUTO_INCREMENT NOT NULL,
	`userId` int NOT NULL,
	`role` enum('user','agent','system') NOT NULL,
	`agentType` varchar(50),
	`content` text NOT NULL,
	`metadata` json,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	CONSTRAINT `coral_chat_messages_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `objectives` (
	`id` int AUTO_INCREMENT NOT NULL,
	`userId` int NOT NULL,
	`title` varchar(200) NOT NULL,
	`description` text,
	`dimension` enum('personal','professional','vital') NOT NULL,
	`priority` enum('low','medium','high') NOT NULL DEFAULT 'medium',
	`status` enum('active','paused','completed','archived') NOT NULL DEFAULT 'active',
	`progress` float NOT NULL DEFAULT 0,
	`deadline` timestamp,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	`completedAt` timestamp,
	`metadata` json,
	CONSTRAINT `objectives_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `synergies` (
	`id` int AUTO_INCREMENT NOT NULL,
	`userId` int NOT NULL,
	`objective1Id` int NOT NULL,
	`objective2Id` int NOT NULL,
	`synergyType` enum('resource_sharing','skill_overlap','timeline_alignment','impact_multiplier','knowledge_transfer') NOT NULL,
	`strength` float NOT NULL,
	`description` text,
	`detectedBy` varchar(50) NOT NULL,
	`status` enum('detected','acknowledged','active','dismissed') NOT NULL DEFAULT 'detected',
	`detectedAt` timestamp NOT NULL DEFAULT (now()),
	`metadata` json,
	CONSTRAINT `synergies_id` PRIMARY KEY(`id`)
);
