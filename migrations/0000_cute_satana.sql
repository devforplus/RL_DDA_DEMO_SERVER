CREATE TABLE `assignments` (
	`id` text PRIMARY KEY NOT NULL,
	`experiment_id` text NOT NULL,
	`participant_id` text NOT NULL,
	`arm` text NOT NULL,
	`assigned_at` integer NOT NULL,
	FOREIGN KEY (`experiment_id`) REFERENCES `experiments`(`id`) ON UPDATE no action ON DELETE no action,
	FOREIGN KEY (`participant_id`) REFERENCES `participants`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE TABLE `events` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`session_id` text NOT NULL,
	`t_ms` integer NOT NULL,
	`type` text NOT NULL,
	`payload` text NOT NULL,
	FOREIGN KEY (`session_id`) REFERENCES `sessions`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE INDEX `idx_events_session_id` ON `events` (`session_id`);--> statement-breakpoint
CREATE INDEX `idx_events_session_t` ON `events` (`session_id`,`t_ms`);--> statement-breakpoint
CREATE TABLE `experiments` (
	`id` text PRIMARY KEY NOT NULL,
	`name` text NOT NULL,
	`config` text NOT NULL,
	`created_at` integer NOT NULL
);
--> statement-breakpoint
CREATE TABLE `gameplays` (
	`id` text PRIMARY KEY NOT NULL,
	`nickname` text NOT NULL,
	`score` integer NOT NULL,
	`final_stage` integer NOT NULL,
	`model_id` text,
	`total_frames` integer,
	`play_duration` real,
	`enemies_destroyed` integer,
	`shots_fired` integer,
	`hits` integer,
	`deaths` integer,
	`frames_data` text,
	`created_at` integer NOT NULL
);
--> statement-breakpoint
CREATE INDEX `idx_gameplays_nickname` ON `gameplays` (`nickname`);--> statement-breakpoint
CREATE INDEX `idx_gameplays_score` ON `gameplays` (`score`);--> statement-breakpoint
CREATE INDEX `idx_gameplays_model_id` ON `gameplays` (`model_id`);--> statement-breakpoint
CREATE INDEX `idx_gameplays_score_created` ON `gameplays` (`score`,`created_at`);--> statement-breakpoint
CREATE INDEX `idx_gameplays_model_score` ON `gameplays` (`model_id`,`score`);--> statement-breakpoint
CREATE INDEX `idx_gameplays_created_at` ON `gameplays` (`created_at`);--> statement-breakpoint
CREATE TABLE `participants` (
	`id` text PRIMARY KEY NOT NULL,
	`created_at` integer NOT NULL,
	`locale` text,
	`user_agent_hash` text,
	`cohort` text
);
--> statement-breakpoint
CREATE TABLE `replays` (
	`id` text PRIMARY KEY NOT NULL,
	`session_id` text NOT NULL,
	`storage_url` text NOT NULL,
	`frames_count` integer,
	`duration_ms` integer,
	`compression` text,
	`schema_version` text,
	`generated_by` text,
	`checksum` text,
	`created_at` integer NOT NULL,
	FOREIGN KEY (`session_id`) REFERENCES `sessions`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE UNIQUE INDEX `idx_replays_session_id` ON `replays` (`session_id`);--> statement-breakpoint
CREATE TABLE `sessions` (
	`id` text PRIMARY KEY NOT NULL,
	`participant_id` text NOT NULL,
	`mode` text NOT NULL,
	`agent_skill` text,
	`game_version` text,
	`model_version` text,
	`seed` integer,
	`started_at` integer NOT NULL,
	`ended_at` integer,
	`duration_ms` integer,
	`result` text,
	FOREIGN KEY (`participant_id`) REFERENCES `participants`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE INDEX `idx_sessions_participant_id` ON `sessions` (`participant_id`);