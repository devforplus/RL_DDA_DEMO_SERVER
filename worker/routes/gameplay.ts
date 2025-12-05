import { Hono } from 'hono';
import { zValidator } from '@hono/zod-validator';
import { drizzle } from 'drizzle-orm/d1';
import { desc, eq, count } from 'drizzle-orm';
import { gameplays } from '../db/schema';
import { gamePlaySubmitRequestSchema } from '../lib/schemas';

type Env = {
  DB: D1Database;
};

const gameplayRouter = new Hono<{ Bindings: Env }>();

// 중복을 방지할 AI 에이전트 닉네임 목록
const AI_AGENT_NICKNAMES = ['beginner', 'medium', 'master'];

gameplayRouter.post('', zValidator('json', gamePlaySubmitRequestSchema), async (c) => {
  const body = c.req.valid('json');
  const db = drizzle(c.env.DB);
  
  try {
    // AI 에이전트 닉네임인 경우, 저장하지 않고 성공 응답 반환
    if (AI_AGENT_NICKNAMES.includes(body.nickname)) {
      return c.json({
        id: 'skipped-ai-agent',
        message: `AI 에이전트(${body.nickname})의 데이터는 저장되지 않았습니다.`,
      });
    }

    // 일반 유저인 경우 새로 삽입
    const result = await db.insert(gameplays).values({
      nickname: body.nickname,
      score: body.score,
      finalStage: body.final_stage,
      modelId: body.model_id,
      totalFrames: body.statistics.total_frames,
      playDuration: body.statistics.play_duration,
      enemiesDestroyed: body.statistics.enemies_destroyed,
      shotsFired: body.statistics.shots_fired,
      hits: body.statistics.hits,
      deaths: body.statistics.deaths,
      framesData: body.frames as any,
    }).returning();
    
    const gameplay = result[0];
    
    return c.json({
      id: gameplay.id,
      message: '게임 플레이 데이터가 성공적으로 저장되었습니다.',
    });
  } catch (error) {
    console.error('Error saving gameplay:', error);
    return c.json(
      {
        error: `게임 플레이 데이터 저장 중 오류가 발생했습니다: ${error instanceof Error ? error.message : String(error)}`,
      },
      500
    );
  }
});

gameplayRouter.get('/rankings', async (c) => {
  const db = drizzle(c.env.DB);
  
  // 쿼리 파라미터
  const page = parseInt(c.req.query('page') || '1', 10);
  const pageSize = Math.min(parseInt(c.req.query('page_size') || '10', 10), 100);
  const modelId = c.req.query('model_id');
  
  if (page < 1 || pageSize < 1) {
    return c.json({ error: 'Invalid page or page_size' }, 400);
  }
  
  try {
    // 조건 구성
    const conditions = modelId ? eq(gameplays.modelId, modelId) : undefined;
    
    // 전체 개수 조회
    const totalResult = await db
      .select({ count: count() })
      .from(gameplays)
      .where(conditions)
      .get();
    
    const total = totalResult?.count || 0;
    
    // 랭킹 조회
    const offset = (page - 1) * pageSize;
    const rankings = await db
      .select({
        id: gameplays.id,
        nickname: gameplays.nickname,
        score: gameplays.score,
        finalStage: gameplays.finalStage,
        modelId: gameplays.modelId,
        totalFrames: gameplays.totalFrames,
        playDuration: gameplays.playDuration,
        createdAt: gameplays.createdAt,
      })
      .from(gameplays)
      .where(conditions)
      .orderBy(desc(gameplays.score), gameplays.createdAt)
      .limit(pageSize)
      .offset(offset);
    
    // 랭킹 아이템 생성
    const rankingItems = rankings.map((row, idx) => ({
      id: row.id,
      nickname: row.nickname,
      score: row.score,
      final_stage: row.finalStage,
      model_id: row.modelId,
      total_frames: row.totalFrames,
      play_duration: row.playDuration,
      created_at: row.createdAt ? new Date(row.createdAt).toISOString() : '',
      rank: offset + idx + 1,
    }));
    
    return c.json({
      rankings: rankingItems,
      total,
      page,
      page_size: pageSize,
    });
  } catch (error) {
    console.error('Error fetching rankings:', error);
    return c.json(
      {
        error: `랭킹 조회 중 오류가 발생했습니다: ${error instanceof Error ? error.message : String(error)}`,
      },
      500
    );
  }
});

export default gameplayRouter;

