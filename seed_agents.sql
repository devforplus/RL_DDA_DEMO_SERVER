-- AI 에이전트들의 고정된 점수와 생존 시간(step) 데이터를 초기화합니다.
-- 기존 데이터가 있다면 삭제하고 새로 삽입합니다.

DELETE FROM gameplays WHERE nickname IN ('beginner', 'medium', 'master');

INSERT INTO gameplays (id, nickname, score, final_stage, total_frames, play_duration, created_at)
VALUES
  -- beginner: 441 step, 400 score (약 7.35초)
  ('ai_beginner', 'beginner', 400, 1, 441, 7.35, 1700000000000),
  
  -- medium: 1018 step, 1200 score (약 16.97초)
  ('ai_medium', 'medium', 1200, 2, 1018, 16.97, 1700000000000),
  
  -- master: 1353 step, 1400 score (약 22.55초)
  ('ai_master', 'master', 1400, 3, 1353, 22.55, 1700000000000);

