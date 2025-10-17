# 프로덕션 배포 정보

## ✅ 배포 완료

배포 날짜: 2025-10-17

### 프로덕션 URL
```
https://rl-dda-demo-back.ijihyeon164.workers.dev
```

### 리소스

| 리소스 | 이름 | 상태 |
|--------|------|------|
| Worker | rl-dda-demo-back | ✅ 배포됨 |
| D1 Database | rl-dda-demo-db | ✅ 마이그레이션 완료 |
| R2 Bucket | rl-dda-demo-replays | ✅ 생성됨 |
| INGEST_SECRET | (보안 변수) | ✅ 설정됨 |

---

## API 엔드포인트

### 기본 정보
- **베이스 URL**: `https://rl-dda-demo-back.ijihyeon164.workers.dev`
- **환경**: Production
- **리전**: Global (Cloudflare Edge)

### 엔드포인트 목록

#### Health Check
```bash
GET /health
```
응답 예시:
```json
{"status":"ok"}
```

#### Participants
```bash
POST /api/participants
```

#### Sessions
```bash
POST /api/session/start
POST /api/session/end
```

#### Events
```bash
POST /api/events/batch
# Authorization: Bearer <token> 필요
```

#### Agents
```bash
GET /api/agents
```
응답 예시:
```json
[
  {
    "id": "agent-beginner",
    "skill": "beginner",
    "model_version": "v1",
    "description": "초급 에이전트"
  }
]
```

#### Gameplay
```bash
POST /api/gameplay
GET /api/gameplay/rankings?page=1&page_size=10&model_id=beginner
```

#### Replays
```bash
GET /api/replays/:replay_id
GET /api/replays/:replay_id/download
```

---

## CORS 설정

허용된 Origin:
- `https://devfor.plus`
- `https://www.devfor.plus`
- `http://localhost:5173`
- `http://localhost:3000`
- `https://*.vercel.app` (정규식)

---

## 성능 및 제한

### Cloudflare Workers 무료 티어
- ✅ 100,000 요청/일
- ✅ 10ms CPU 시간/요청
- ✅ Global Edge 네트워크

### D1 Database 무료 티어
- ✅ 5GB 저장공간
- ✅ 100,000 쓰기/일
- ✅ 5,000,000 읽기/일

### R2 Storage 무료 티어
- ✅ 10GB 저장공간
- ✅ 1,000,000 클래스 A 작업/월
- ✅ 10,000,000 클래스 B 작업/월

---

## 모니터링

### 실시간 로그
```bash
pnpm logs
```

### Cloudflare Dashboard
1. https://dash.cloudflare.com
2. Workers & Pages > rl-dda-demo-back
3. Logs, Analytics, Metrics 확인 가능

---

## 배포 워크플로우

### 코드 변경 후 배포
```bash
# 1. 타입 체크
pnpm typecheck

# 2. 로컬 테스트
pnpm dev

# 3. 프로덕션 배포
pnpm wrangler deploy
```

### 데이터베이스 스키마 변경
```bash
# 1. 스키마 수정 (worker/db/schema.ts)

# 2. 마이그레이션 생성
pnpm db:generate

# 3. 로컬 테스트
pnpm db:migrate

# 4. 프로덕션 적용
pnpm db:migrate:prod

# 5. Worker 재배포
pnpm wrangler deploy
```

---

## 트러블슈팅

### 배포 실패
```bash
# 로그 확인
pnpm wrangler deployments list

# 특정 배포로 롤백
pnpm wrangler deployments rollback <deployment-id>
```

### 환경 변수 확인
```bash
# Secret 목록 확인
pnpm wrangler secret list

# Secret 삭제
pnpm wrangler secret delete INGEST_SECRET

# Secret 재설정
pnpm wrangler secret put INGEST_SECRET
```

### 데이터베이스 확인
```bash
# D1 데이터베이스 목록
pnpm wrangler d1 list

# 직접 쿼리 실행
pnpm wrangler d1 execute rl-dda-demo-db --remote --command "SELECT * FROM participants LIMIT 10"
```

---

## 보안

### API 키 관리
- ✅ `INGEST_SECRET`은 Wrangler Secret으로 관리됨
- ⚠️ Git에 커밋되지 않음
- ⚠️ Dashboard에서도 볼 수 없음 (보안상 안전)

### CORS
- ✅ 허용된 Origin만 접근 가능
- ✅ Credentials 지원
- ✅ Preflight 요청 처리

### 인증
- ✅ HMAC-SHA256 기반 토큰
- ✅ 1시간 유효기간
- ✅ Session ID 검증

---

## 다음 단계

### 커스텀 도메인 연결
1. Cloudflare Dashboard에서 설정
2. DNS 자동 구성
3. SSL/TLS 자동 설정 (무료)

### 모니터링 강화
- Cloudflare Analytics 활용
- 에러 추적 설정
- 성능 메트릭 확인

### 스케일링
- 무료 티어 한도 모니터링
- 필요시 유료 플랜 고려
- 캐싱 전략 최적화

---

## 연락처

- Cloudflare 계정: ijihyeon164@gmail.com
- Worker 이름: rl-dda-demo-back
- Account ID: 0c5edd25d79bcbefe1c4384d0a3f25e4

---

## 변경 이력

### 2025-10-17
- ✅ 초기 프로덕션 배포
- ✅ D1 데이터베이스 마이그레이션
- ✅ R2 버킷 생성
- ✅ 환경 변수 설정
- ✅ API 엔드포인트 테스트 완료

