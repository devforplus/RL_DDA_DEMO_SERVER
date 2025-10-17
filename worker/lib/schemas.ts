import { z } from 'zod';

/**
 * Participant 스키마
 */
export const participantSchema = z.object({
  id: z.string(),
});

/**
 * Session Start Request
 */
export const sessionStartRequestSchema = z.object({
  participant_id: z.string(),
  mode: z.enum(['human', 'agent']),
  agent_skill: z.enum(['beginner', 'intermediate', 'advanced']).optional(),
  game_version: z.string().optional(),
  model_version: z.string().optional(),
  seed: z.number().int().optional(),
});

export type SessionStartRequest = z.infer<typeof sessionStartRequestSchema>;

/**
 * Session Start Response
 */
export const sessionStartResponseSchema = z.object({
  session_id: z.string(),
  ingest_token: z.string(),
});

export type SessionStartResponse = z.infer<typeof sessionStartResponseSchema>;

/**
 * Session End Request
 */
export const sessionEndRequestSchema = z.object({
  session_id: z.string(),
  duration_ms: z.number().int().optional(),
  result: z.record(z.string(), z.unknown()).optional(),
});

export type SessionEndRequest = z.infer<typeof sessionEndRequestSchema>;

/**
 * Events Batch Item
 */
export const eventsBatchItemSchema = z.object({
  t_ms: z.number().int(),
  type: z.string(),
  payload: z.record(z.string(), z.unknown()),
});

export type EventsBatchItem = z.infer<typeof eventsBatchItemSchema>;

/**
 * Events Batch Request
 */
export const eventsBatchRequestSchema = z.object({
  session_id: z.string(),
  request_id: z.string().optional(),
  events: z.array(eventsBatchItemSchema),
});

export type EventsBatchRequest = z.infer<typeof eventsBatchRequestSchema>;

/**
 * GamePlay Statistics
 */
export const gamePlayStatisticsSchema = z.object({
  total_frames: z.number().int().optional(),
  play_duration: z.number().optional(),
  enemies_destroyed: z.number().int().optional(),
  shots_fired: z.number().int().optional(),
  hits: z.number().int().optional(),
  deaths: z.number().int().optional(),
});

export type GamePlayStatistics = z.infer<typeof gamePlayStatisticsSchema>;

/**
 * GamePlay Frame
 */
export const gamePlayFrameSchema = z.object({
  frame_number: z.number().int(),
  player_x: z.number(),
  player_y: z.number(),
  player_lives: z.number().int(),
  player_score: z.number().int(),
  current_weapon: z.number().int(),
  input_left: z.number().int(),
  input_right: z.number().int(),
}).passthrough(); // 추가 필드 허용

export type GamePlayFrame = z.infer<typeof gamePlayFrameSchema>;

/**
 * GamePlay Submit Request
 */
export const gamePlaySubmitRequestSchema = z.object({
  nickname: z.string(),
  score: z.number().int(),
  final_stage: z.number().int(),
  model_id: z.string().optional(),
  statistics: gamePlayStatisticsSchema,
  frames: z.array(gamePlayFrameSchema),
});

export type GamePlaySubmitRequest = z.infer<typeof gamePlaySubmitRequestSchema>;

/**
 * GamePlay Submit Response
 */
export const gamePlaySubmitResponseSchema = z.object({
  id: z.string(),
  message: z.string(),
});

export type GamePlaySubmitResponse = z.infer<typeof gamePlaySubmitResponseSchema>;

/**
 * GamePlay Ranking Item
 */
export const gamePlayRankingItemSchema = z.object({
  id: z.string(),
  nickname: z.string(),
  score: z.number().int(),
  final_stage: z.number().int(),
  model_id: z.string().nullable(),
  created_at: z.string(),
  rank: z.number().int(),
});

export type GamePlayRankingItem = z.infer<typeof gamePlayRankingItemSchema>;

/**
 * GamePlay Ranking Response
 */
export const gamePlayRankingResponseSchema = z.object({
  rankings: z.array(gamePlayRankingItemSchema),
  total: z.number().int(),
  page: z.number().int(),
  page_size: z.number().int(),
});

export type GamePlayRankingResponse = z.infer<typeof gamePlayRankingResponseSchema>;

