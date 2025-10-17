import { Hono } from 'hono';
import { drizzle } from 'drizzle-orm/d1';
import { participants } from '../db/schema';

type Env = {
  DB: D1Database;
};

const participantsRouter = new Hono<{ Bindings: Env }>();

participantsRouter.post('', async (c) => {
  const db = drizzle(c.env.DB);
  
  const result = await db.insert(participants).values({}).returning();
  const participant = result[0];
  
  return c.json({ id: participant.id });
});

export default participantsRouter;

