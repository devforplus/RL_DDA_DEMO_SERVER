import { text, integer, real, sqliteTable, index, uniqueIndex } from 'drizzle-orm/sqlite-core';

/**
 * 유틸리티 함수: 32자 hex UUID 생성
 */
export function generateId(): string {
  return crypto.randomUUID().replace(/-/g, '');
}

/**
 * 참가자 테이블
 */
export const participants = sqliteTable('participants', {
  id: text('id').primaryKey().$defaultFn(generateId),
  createdAt: integer('created_at', { mode: 'timestamp' })
    .notNull()
    .$defaultFn(() => new Date()),
  locale: text('locale'),
  userAgentHash: text('user_agent_hash'),
  cohort: text('cohort'),
});

/**
 * 세션 테이블
 */
export const sessions = sqliteTable(
  'sessions',
  {
    id: text('id').primaryKey().$defaultFn(generateId),
    participantId: text('participant_id')
      .notNull()
      .references(() => participants.id),
    
    mode: text('mode', { enum: ['human', 'agent'] }).notNull(),
    agentSkill: text('agent_skill', { enum: ['beginner', 'intermediate', 'advanced'] }),
    gameVersion: text('game_version'),
    modelVersion: text('model_version'),
    seed: integer('seed'),
    
    startedAt: integer('started_at', { mode: 'timestamp' })
      .notNull()
      .$defaultFn(() => new Date()),
    endedAt: integer('ended_at', { mode: 'timestamp' }),
    durationMs: integer('duration_ms'),
    result: text('result', { mode: 'json' }).$type<Record<string, unknown>>(),
  },
  (table) => ({
    participantIdIdx: index('idx_sessions_participant_id').on(table.participantId),
  })
);

/**
 * 이벤트 테이블
 */
export const events = sqliteTable(
  'events',
  {
    id: integer('id').primaryKey({ autoIncrement: true }),
    sessionId: text('session_id')
      .notNull()
      .references(() => sessions.id),
    tMs: integer('t_ms').notNull(),
    type: text('type').notNull(),
    payload: text('payload', { mode: 'json' }).notNull().$type<Record<string, unknown>>(),
  },
  (table) => ({
    sessionIdIdx: index('idx_events_session_id').on(table.sessionId),
    sessionTIdx: index('idx_events_session_t').on(table.sessionId, table.tMs),
  })
);

/**
 * 리플레이 테이블
 */
export const replays = sqliteTable(
  'replays',
  {
    id: text('id').primaryKey().$defaultFn(generateId),
    sessionId: text('session_id')
      .notNull()
      .references(() => sessions.id),
    storageUrl: text('storage_url').notNull(),
    framesCount: integer('frames_count'),
    durationMs: integer('duration_ms'),
    compression: text('compression'),
    schemaVersion: text('schema_version'),
    generatedBy: text('generated_by'),
    checksum: text('checksum'),
    createdAt: integer('created_at', { mode: 'timestamp' })
      .notNull()
      .$defaultFn(() => new Date()),
  },
  (table) => ({
    sessionIdUnique: uniqueIndex('idx_replays_session_id').on(table.sessionId),
  })
);

/**
 * 실험 테이블
 */
export const experiments = sqliteTable('experiments', {
  id: text('id').primaryKey().$defaultFn(generateId),
  name: text('name').notNull(),
  config: text('config', { mode: 'json' }).notNull().$type<Record<string, unknown>>().$default(() => ({})),
  createdAt: integer('created_at', { mode: 'timestamp' })
    .notNull()
    .$defaultFn(() => new Date()),
});

/**
 * 할당 테이블
 */
export const assignments = sqliteTable('assignments', {
  id: text('id').primaryKey().$defaultFn(generateId),
  experimentId: text('experiment_id')
    .notNull()
    .references(() => experiments.id),
  participantId: text('participant_id')
    .notNull()
    .references(() => participants.id),
  arm: text('arm').notNull(),
  assignedAt: integer('assigned_at', { mode: 'timestamp' })
    .notNull()
    .$defaultFn(() => new Date()),
});

/**
 * 게임플레이 테이블
 */
export const gameplays = sqliteTable(
  'gameplays',
  {
    id: text('id').primaryKey().$defaultFn(generateId),
    nickname: text('nickname').notNull(),
    score: integer('score').notNull(),
    finalStage: integer('final_stage').notNull(),
    modelId: text('model_id'),
    
    // 통계 데이터
    totalFrames: integer('total_frames'),
    playDuration: real('play_duration'), // 초 단위
    enemiesDestroyed: integer('enemies_destroyed'),
    shotsFired: integer('shots_fired'),
    hits: integer('hits'),
    deaths: integer('deaths'),
    
    // 프레임 데이터는 JSON으로 저장
    framesData: text('frames_data', { mode: 'json' }).$type<Array<Record<string, unknown>>>(),
    
    createdAt: integer('created_at', { mode: 'timestamp' })
      .notNull()
      .$defaultFn(() => new Date()),
  },
  (table) => ({
    nicknameIdx: index('idx_gameplays_nickname').on(table.nickname),
    scoreIdx: index('idx_gameplays_score').on(table.score),
    modelIdIdx: index('idx_gameplays_model_id').on(table.modelId),
    scoreCreatedIdx: index('idx_gameplays_score_created').on(table.score, table.createdAt),
    modelScoreIdx: index('idx_gameplays_model_score').on(table.modelId, table.score),
    createdAtIdx: index('idx_gameplays_created_at').on(table.createdAt),
  })
);

// 타입 추출
export type Participant = typeof participants.$inferSelect;
export type NewParticipant = typeof participants.$inferInsert;

export type Session = typeof sessions.$inferSelect;
export type NewSession = typeof sessions.$inferInsert;

export type Event = typeof events.$inferSelect;
export type NewEvent = typeof events.$inferInsert;

export type Replay = typeof replays.$inferSelect;
export type NewReplay = typeof replays.$inferInsert;

export type Experiment = typeof experiments.$inferSelect;
export type NewExperiment = typeof experiments.$inferInsert;

export type Assignment = typeof assignments.$inferSelect;
export type NewAssignment = typeof assignments.$inferInsert;

export type GamePlay = typeof gameplays.$inferSelect;
export type NewGamePlay = typeof gameplays.$inferInsert;

