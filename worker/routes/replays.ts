import { Hono } from 'hono';
import { drizzle } from 'drizzle-orm/d1';
import { eq } from 'drizzle-orm';
import { replays } from '../db/schema';

type Env = {
  DB: D1Database;
  R2: R2Bucket;
};

const replaysRouter = new Hono<{ Bindings: Env }>();

replaysRouter.get('/:replay_id', async (c) => {
  const replayId = c.req.param('replay_id');
  const db = drizzle(c.env.DB);
  
  const replay = await db
    .select()
    .from(replays)
    .where(eq(replays.id, replayId))
    .get();
  
  if (!replay) {
    return c.json({ error: 'Replay not found' }, 404);
  }
  
  // R2 presigned URL 생성 (3600초 = 1시간)
  const expiresIn = 3600;
  
  // R2에서 객체 가져오기
  const object = await c.env.R2.get(replay.storageUrl);
  
  if (!object) {
    return c.json({ error: 'Replay file not found in storage' }, 404);
  }
  
  // R2 signed URL 생성 (Cloudflare R2는 직접 presigned URL을 제공하지 않으므로
  // 대신 임시 접근 URL을 생성하거나, 직접 데이터를 반환할 수 있습니다)
  // 여기서는 메타데이터를 반환하고, 실제 파일은 별도 엔드포인트에서 제공
  
  return c.json({
    id: replay.id,
    session_id: replay.sessionId,
    frames_count: replay.framesCount,
    duration_ms: replay.durationMs,
    compression: replay.compression,
    schema_version: replay.schemaVersion,
    generated_by: replay.generatedBy,
    checksum: replay.checksum,
    created_at: replay.createdAt ? new Date(replay.createdAt).toISOString() : null,
    // R2의 경우 직접 다운로드 URL 제공 방식이 다르므로 별도 엔드포인트 필요
    url: `/api/replays/${replayId}/download`,
    expires_in: expiresIn,
  });
});

// R2에서 실제 파일 다운로드
replaysRouter.get('/:replay_id/download', async (c) => {
  const replayId = c.req.param('replay_id');
  const db = drizzle(c.env.DB);
  
  const replay = await db
    .select()
    .from(replays)
    .where(eq(replays.id, replayId))
    .get();
  
  if (!replay) {
    return c.json({ error: 'Replay not found' }, 404);
  }
  
  const object = await c.env.R2.get(replay.storageUrl);
  
  if (!object) {
    return c.json({ error: 'Replay file not found in storage' }, 404);
  }
  
  // R2 객체를 직접 반환
  return new Response(object.body, {
    headers: {
      'Content-Type': object.httpMetadata?.contentType || 'application/octet-stream',
      'Content-Length': object.size.toString(),
      'Cache-Control': 'public, max-age=3600',
    },
  });
});

export default replaysRouter;

