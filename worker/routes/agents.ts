import { Hono } from 'hono';

const agentsRouter = new Hono();

agentsRouter.get('', (c) => {
  // 정적 에이전트 목록 (나중에 DB로 이동 가능)
  return c.json([
    {
      id: 'agent-beginner',
      skill: 'beginner',
      model_version: 'v1',
      description: '초급 에이전트',
    },
    {
      id: 'agent-intermediate',
      skill: 'intermediate',
      model_version: 'v1',
      description: '중급 에이전트',
    },
    {
      id: 'agent-advanced',
      skill: 'advanced',
      model_version: 'v1',
      description: '고급 에이전트',
    },
  ]);
});

export default agentsRouter;

