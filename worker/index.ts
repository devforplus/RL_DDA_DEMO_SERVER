import { Hono } from 'hono';
import healthRouter from './routes/health';
import participantsRouter from './routes/participants';
import sessionsRouter from './routes/sessions';
import eventsRouter from './routes/events';
import agentsRouter from './routes/agents';
import gameplayRouter from './routes/gameplay';
import replaysRouter from './routes/replays';

export type Env = {
  DB: D1Database;
  R2: R2Bucket;
  APP_NAME: string;
  INGEST_SECRET: string;
  CORS_ORIGINS: string;
  CORS_ORIGIN_REGEX: string;
};

const app = new Hono<{ Bindings: Env }>();

// CORS 미들웨어
app.use('*', async (c, next) => {
  const corsOrigins = JSON.parse(c.env.CORS_ORIGINS || '[]') as string[];
  const corsOriginRegex = c.env.CORS_ORIGIN_REGEX;
  const origin = c.req.header('Origin');

  // CORS 검증
  let allowOrigin: string | undefined = undefined;

  if (origin) {
    // 정확한 매칭
    if (corsOrigins.includes(origin)) {
      allowOrigin = origin;
    }

    // 정규식 매칭
    if (!allowOrigin && corsOriginRegex) {
      try {
        const regex = new RegExp(corsOriginRegex);
        if (regex.test(origin)) {
          allowOrigin = origin;
        }
      } catch (e) {
        console.error('Invalid CORS origin regex:', e);
      }
    }
  }

  // CORS 헤더 설정
  if (allowOrigin) {
    c.header('Access-Control-Allow-Origin', allowOrigin);
    c.header('Access-Control-Allow-Credentials', 'true');
    c.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    c.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  }

  // Preflight 요청 처리
  if (c.req.method === 'OPTIONS') {
    return c.body(null, 204);
  }

  return await next();
});

// 라우터 등록
app.route('/', healthRouter);
app.route('/api/participants', participantsRouter);
app.route('/api/session', sessionsRouter);
app.route('/api/events', eventsRouter);
app.route('/api/agents', agentsRouter);
app.route('/api/gameplay', gameplayRouter);
app.route('/api/replays', replaysRouter);

// 404 핸들러
app.notFound((c) => {
  return c.json({ error: 'Not Found' }, 404);
});

// 에러 핸들러
app.onError((err, c) => {
  console.error('Error:', err);
  return c.json(
    {
      error: 'Internal Server Error',
      message: err.message,
    },
    500
  );
});

export default app;

