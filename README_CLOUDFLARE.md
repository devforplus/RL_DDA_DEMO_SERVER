# RL DDA Demo Backend - Cloudflare Workers

TypeScript + Cloudflare Workers + D1 + R2를 사용한 백엔드 서비스입니다.

## 기술 스택

- **프레임워크**: Hono (Cloudflare Workers 최적화)
- **데이터베이스**: Cloudflare D1 (SQLite)
- **스토리지**: Cloudflare R2 (S3 호환)
- **ORM**: Drizzle ORM
- **검증**: Zod
- **빌드 도구**: Wrangler

## 프로젝트 구조

```
worker/
├── db/
│   └── schema.ts          # Drizzle ORM 스키마 정의
├── lib/
│   ├── auth.ts           # 인증 토큰 관리 (HMAC-SHA256)
│   ├── cors.ts           # CORS 유틸리티
│   └── schemas.ts        # Zod 스키마 정의
├── routes/
│   ├── health.ts         # 헬스체크
│   ├── participants.ts   # 참가자 관리
│   ├── sessions.ts       # 세션 관리
│   ├── events.ts         # 이벤트 수집
│   ├── agents.ts         # AI 에이전트 목록
│   ├── gameplay.ts       # 게임플레이 제출 및 랭킹
│   └── replays.ts        # 리플레이 다운로드
└── index.ts              # 메인 Worker 엔트리포인트
```

## 시작하기

### 1. 패키지 설치

```bash
pnpm install
```

### 2. D1 데이터베이스 생성

#### 로컬 개발
로컬 개발 환경에서는 Wrangler가 자동으로 로컬 D1 데이터베이스를 생성합니다.

#### 프로덕션
```bash
# D1 데이터베이스 생성
pnpm wrangler d1 create rl-dda-demo-db

# 출력된 database_id를 wrangler.toml에 복사
# [[d1_databases]]
# database_id = "여기에-복사"
```

### 3. 마이그레이션 실행

#### 로컬 개발
```bash
# 스키마에서 마이그레이션 생성
pnpm db:generate

# 로컬 DB에 마이그레이션 적용
pnpm db:migrate
```

#### 프로덕션
```bash
# 프로덕션 DB에 마이그레이션 적용
pnpm db:migrate:prod
```

### 4. R2 버킷 생성

```bash
# R2 버킷 생성
pnpm wrangler r2 bucket create rl-dda-demo-replays
```

### 5. 환경 변수 설정

`wrangler.toml`에서 환경 변수를 설정하거나, `.dev.vars` 파일을 생성합니다:

```bash
# .dev.vars (로컬 개발용, .gitignore에 포함됨)
INGEST_SECRET=your-secret-key-here
```

프로덕션 환경 변수는 Cloudflare Dashboard에서 설정하거나 wrangler secrets를 사용합니다:

```bash
pnpm wrangler secret put INGEST_SECRET
```

### 6. 개발 서버 실행

```bash
pnpm dev
```

서버가 `http://localhost:8787`에서 실행됩니다.

### 7. 배포

```bash
pnpm deploy
```

## API 엔드포인트

### Health Check
- `GET /health` - 서버 상태 확인

### Participants
- `POST /api/participants` - 참가자 생성

### Sessions
- `POST /api/session/start` - 세션 시작
- `POST /api/session/end` - 세션 종료

### Events
- `POST /api/events/batch` - 이벤트 배치 수집 (인증 필요)

### Agents
- `GET /api/agents` - AI 에이전트 목록 조회

### Gameplay
- `POST /api/gameplay` - 게임플레이 데이터 제출
- `GET /api/gameplay/rankings` - 랭킹 조회
  - Query params: `page`, `page_size`, `model_id`

### Replays
- `GET /api/replays/:replay_id` - 리플레이 메타데이터 조회
- `GET /api/replays/:replay_id/download` - 리플레이 파일 다운로드

## 주요 변경 사항 (Python -> TypeScript)

### 데이터베이스
- **MySQL** → **D1 (SQLite)**
- **SQLAlchemy** → **Drizzle ORM**
- `CHAR(32)` → `TEXT`
- `DateTime(timezone=True)` → `INTEGER (timestamp)`
- `JSON` → `TEXT (JSON mode)`

### 프레임워크
- **FastAPI** → **Hono**
- **Pydantic** → **Zod**
- Dependency Injection → Context-based bindings

### 스토리지
- **AWS S3 (boto3)** → **Cloudflare R2**
- Presigned URLs → 직접 다운로드 엔드포인트

### 인증
- Python의 HMAC 구현 → Web Crypto API 사용

## 개발 도구

### 타입 체크
```bash
pnpm typecheck
```

### Drizzle Studio (DB GUI)
```bash
pnpm db:studio
```

### Wrangler 로그 확인
```bash
pnpm wrangler tail
```

## CORS 설정

CORS는 `wrangler.toml`의 환경 변수로 설정됩니다:

```toml
[vars]
CORS_ORIGINS = '["https://devfor.plus","https://www.devfor.plus","http://localhost:5173"]'
CORS_ORIGIN_REGEX = "https://.*\\.vercel\\.app"
```

## 보안

### Ingest Token
이벤트 수집 API는 세션별 HMAC-SHA256 토큰으로 보호됩니다:
- 세션 시작 시 토큰 발급
- 1시간 유효기간
- Authorization Bearer 헤더로 전달

### 환경 변수
민감한 정보는 반드시 환경 변수로 관리:
- `INGEST_SECRET`: 토큰 생성/검증용 비밀키

## 마이그레이션 가이드 (기존 MySQL → D1)

### 1. 데이터 내보내기
```bash
# MySQL에서 데이터 내보내기
mysqldump -u user -p rldda > backup.sql
```

### 2. 데이터 변환
MySQL 덤프를 SQLite 호환 형식으로 변환 (수동 또는 도구 사용)

### 3. D1으로 임포트
```bash
# SQLite 파일 생성 후
pnpm wrangler d1 execute rl-dda-demo-db --file=./import.sql --remote
```

## 문제 해결

### D1 마이그레이션 실패
```bash
# 마이그레이션 상태 확인
pnpm wrangler d1 migrations list rl-dda-demo-db --local

# 특정 마이그레이션만 실행
pnpm wrangler d1 execute rl-dda-demo-db --file=migrations/0000_xxx.sql --local
```

### R2 연결 문제
- `wrangler.toml`의 R2 바인딩 이름이 `R2`인지 확인
- 버킷이 생성되었는지 확인

### 타입 에러
```bash
# node_modules 재설치
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

## 성능 최적화

### D1 쿼리 최적화
- 인덱스 활용 (schema.ts에 정의됨)
- 배치 작업 사용
- 필요한 컬럼만 SELECT

### R2 캐싱
- `Cache-Control` 헤더 설정
- Cloudflare CDN 자동 캐싱 활용

### Worker 최적화
- 번들 크기 최소화
- 불필요한 의존성 제거
- Edge에서 실행되므로 지연시간 최소화

## 라이선스

ISC

## 기여

기존 FastAPI 프로젝트와 API 호환성을 유지하면서 개선하고 있습니다.

