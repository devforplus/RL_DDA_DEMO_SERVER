import { Hono } from 'hono';
import { zValidator } from '@hono/zod-validator';
import { drizzle } from 'drizzle-orm/d1';
import { eq } from 'drizzle-orm';
import { events, sessions } from '../db/schema';
import { eventsBatchRequestSchema } from '../lib/schemas';
import { verifyIngestToken, extractBearerToken } from '../lib/auth';

type Env = {
  DB: D1Database;
  INGEST_SECRET: string;
};

const eventsRouter = new Hono<{ Bindings: Env }>();

eventsRouter.post('/batch', zValidator('json', eventsBatchRequestSchema), async (c) => {
  const body = c.req.valid('json');
  const db = drizzle(c.env.DB);
  
  // 토큰 검증
  const authorization = c.req.header('Authorization') || null;
  const token = extractBearerToken(authorization);
  
  if (!token) {
    return c.json({ error: 'Missing bearer token' }, 401);
  }
  
  let payload;
  try {
    payload = await verifyIngestToken(c.env.INGEST_SECRET, token);
  } catch (error) {
    return c.json({ error: 'Invalid or expired token' }, 403);
  }
  
  if (payload.sid !== body.session_id) {
    return c.json({ error: 'Session mismatch' }, 403);
  }
  
  // 세션 확인
  const session = await db
    .select({ id: sessions.id })
    .from(sessions)
    .where(eq(sessions.id, body.session_id))
    .get();
  
  if (!session) {
    return c.json({ error: 'Session not found' }, 404);
  }
  
  // 이벤트 삽입
  if (body.events.length > 0) {
    await db.insert(events).values(
      body.events.map((e) => ({
        sessionId: body.session_id,
        tMs: e.t_ms,
        type: e.type,
        payload: e.payload as any,
      }))
    );
  }
  
  return c.json({ accepted: true, count: body.events.length });
});

export default eventsRouter;

