CREATE TABLE `agent_actions` (
	`id` int AUTO_INCREMENT NOT NULL,
	`agentType` enum('research_analyst','content_writer','legal_advisor','creative_director','financial_analyst','data_scientist','communications_manager','strategic_planner','quality_assurance','knowledge_manager') NOT NULL,
	`actionType` enum('task_started','task_completed','analysis_performed','document_created','email_sent','review_completed','recommendation_made') NOT NULL,
	`projectId` int,
	`taskId` int,
	`description` text NOT NULL,
	`result` text,
	`duration` float,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`metadata` json,
	CONSTRAINT `agent_actions_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `agents` (
	`id` int AUTO_INCREMENT NOT NULL,
	`type` enum('research_analyst','content_writer','legal_advisor','creative_director','financial_analyst','data_scientist','communications_manager','strategic_planner','quality_assurance','knowledge_manager') NOT NULL,
	`name` varchar(100) NOT NULL,
	`department` enum('research','content','legal','creative','finance','data','communications','strategy','qa','knowledge') NOT NULL,
	`status` enum('available','busy','offline') NOT NULL DEFAULT 'available',
	`currentTaskId` int,
	`workload` int NOT NULL DEFAULT 0,
	`totalTasksCompleted` int NOT NULL DEFAULT 0,
	`averageCompletionTime` float,
	`lastActivity` timestamp NOT NULL DEFAULT (now()),
	`metadata` json,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	CONSTRAINT `agents_id` PRIMARY KEY(`id`),
	CONSTRAINT `agents_type_unique` UNIQUE(`type`)
);
--> statement-breakpoint
CREATE TABLE `communications` (
	`id` int AUTO_INCREMENT NOT NULL,
	`projectId` int,
	`taskId` int,
	`role` enum('user','agent','system') NOT NULL,
	`agentType` varchar(50),
	`content` text NOT NULL,
	`attachments` json,
	`metadata` json,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	CONSTRAINT `communications_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `deliverables` (
	`id` int AUTO_INCREMENT NOT NULL,
	`projectId` int NOT NULL,
	`taskId` int,
	`agentType` enum('research_analyst','content_writer','legal_advisor','creative_director','financial_analyst','data_scientist','communications_manager','strategic_planner','quality_assurance','knowledge_manager') NOT NULL,
	`title` varchar(200) NOT NULL,
	`type` enum('document','report','analysis','design','code','presentation','email','other') NOT NULL,
	`content` text,
	`fileUrl` varchar(500),
	`status` enum('draft','review','approved','delivered') NOT NULL DEFAULT 'draft',
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	`metadata` json,
	CONSTRAINT `deliverables_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `projects` (
	`id` int AUTO_INCREMENT NOT NULL,
	`userId` int NOT NULL,
	`name` varchar(200) NOT NULL,
	`description` text,
	`status` enum('planning','active','on_hold','completed','archived') NOT NULL DEFAULT 'planning',
	`priority` enum('low','medium','high','critical') NOT NULL DEFAULT 'medium',
	`deadline` timestamp,
	`progress` float NOT NULL DEFAULT 0,
	`budget` float,
	`department` enum('research','content','legal','creative','finance','data','communications','strategy','qa','knowledge'),
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	`completedAt` timestamp,
	`metadata` json,
	CONSTRAINT `projects_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `tasks` (
	`id` int AUTO_INCREMENT NOT NULL,
	`projectId` int NOT NULL,
	`title` varchar(200) NOT NULL,
	`description` text,
	`assignedAgentType` enum('research_analyst','content_writer','legal_advisor','creative_director','financial_analyst','data_scientist','communications_manager','strategic_planner','quality_assurance','knowledge_manager'),
	`status` enum('pending','in_progress','review','completed','blocked') NOT NULL DEFAULT 'pending',
	`priority` enum('low','medium','high','urgent') NOT NULL DEFAULT 'medium',
	`progress` float NOT NULL DEFAULT 0,
	`estimatedHours` float,
	`actualHours` float,
	`deadline` timestamp,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	`completedAt` timestamp,
	`metadata` json,
	CONSTRAINT `tasks_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
DROP TABLE `agent_assignments`;--> statement-breakpoint
DROP TABLE `agent_conversations`;--> statement-breakpoint
DROP TABLE `coordination_cycles`;--> statement-breakpoint
DROP TABLE `coral_chat_messages`;--> statement-breakpoint
DROP TABLE `objectives`;--> statement-breakpoint
DROP TABLE `synergies`;