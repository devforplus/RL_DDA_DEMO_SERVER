import { Hono } from 'hono';
import { zValidator } from '@hono/zod-validator';
import { drizzle } from 'drizzle-orm/d1';
import { eq } from 'drizzle-orm';
import { participants, sessions } from '../db/schema';
import { sessionStartRequestSchema, sessionEndRequestSchema } from '../lib/schemas';
import { signIngestToken } from '../lib/auth';

type Env = {
  DB: D1Database;
  INGEST_SECRET: string;
};

const sessionsRouter = new Hono<{ Bindings: Env }>();

sessionsRouter.post('/start', zValidator('json', sessionStartRequestSchema), async (c) => {
  const body = c.req.valid('json');
  const db = drizzle(c.env.DB);
  
  // 참가자 확인
  const participant = await db
    .select()
    .from(participants)
    .where(eq(participants.id, body.participant_id))
    .get();
  
  if (!participant) {
    return c.json({ error: 'Participant not found' }, 404);
  }
  
  // 세션 생성
  const result = await db.insert(sessions).values({
    participantId: body.participant_id,
    mode: body.mode,
    agentSkill: body.agent_skill,
    gameVersion: body.game_version,
    modelVersion: body.model_version,
    seed: body.seed,
  }).returning();
  
  const session = result[0];
  
  // 토큰 생성
  const token = await signIngestToken(c.env.INGEST_SECRET, session.id, 3600);
  
  return c.json({
    session_id: session.id,
    ingest_token: token,
  });
});

sessionsRouter.post('/end', zValidator('json', sessionEndRequestSchema), async (c) => {
  const body = c.req.valid('json');
  const db = drizzle(c.env.DB);
  
  // 세션 확인 및 업데이트
  const session = await db
    .select()
    .from(sessions)
    .where(eq(sessions.id, body.session_id))
    .get();
  
  if (!session) {
    return c.json({ error: 'Session not found' }, 404);
  }
  
  await db
    .update(sessions)
    .set({
      endedAt: new Date(),
      durationMs: body.duration_ms,
      result: body.result as any,
    })
    .where(eq(sessions.id, body.session_id));
  
  return c.json({ ok: true });
});

export default sessionsRouter;

