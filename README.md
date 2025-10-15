# rl-dda-demo-back

Backend service for RL DDA demo. Tech stack: FastAPI, SQLAlchemy (async), Alembic, MySQL. Managed with Rye.

## Quick start (dev)

1) Install Rye and sync deps

```bash
rye sync
```

2) Set environment

Create `.env` in project root (see below example).

Example `.env`:

```
APP_DB_HOST=127.0.0.1
APP_DB_PORT=3306
APP_DB_USER=app
APP_DB_PASSWORD=app
APP_DB_NAME=rldda
# or: APP_DATABASE_URL=mysql+aiomysql://app:app@127.0.0.1:3306/rldda
```

3) Run dev server

```bash
rye run uvicorn src.main:app --reload
```

## Configuration

Environment variables (prefixed with `APP_`):

### Database
- `APP_DB_HOST`, `APP_DB_PORT`, `APP_DB_USER`, `APP_DB_PASSWORD`, `APP_DB_NAME`
- or `APP_DATABASE_URL` (e.g., `mysql+aiomysql://user:pass@host:3306/dbname`)

### CORS
기본값으로 다음 도메인들이 허용됩니다:
- `https://devfor.plus`, `https://www.devfor.plus` (프로덕션)
- `http://localhost:5173`, `http://localhost:3000` (로컬 개발)
- `https://*.vercel.app` (Vercel 프리뷰 배포)

환경변수로 재정의 가능:
- `APP_CORS_ORIGINS`: JSON 배열 형태 (예: `["https://example.com"]`)
- `APP_CORS_ORIGIN_REGEX`: 정규식 패턴 (예: `https://.*\.example\.com`)

### Security
- `APP_INGEST_SECRET`: 데이터 수집 엔드포인트 인증 토큰 (기본값: `change-me`)

### Storage (S3/MinIO)
- `APP_S3_ENDPOINT_URL`, `APP_S3_REGION_NAME`
- `APP_S3_ACCESS_KEY_ID`, `APP_S3_SECRET_ACCESS_KEY`
- `APP_S3_BUCKET`

## Project layout

- `src/main.py`: FastAPI app entry
- `src/config.py`: Settings
- `src/db/`: DB engine/session and metadata base
- `src/api/`: Routers and schemas

## Database and migrations

### 로컬 개발 (Docker MySQL)

로컬에서 Docker를 사용하여 개발하는 경우:

```bash
# MySQL 컨테이너 시작
docker compose up -d db

# .env 파일 설정
APP_DB_HOST=127.0.0.1
APP_DB_PORT=3307  # docker-compose.yml에서 3307로 매핑됨
APP_DB_USER=app
APP_DB_PASSWORD=app
APP_DB_NAME=rldda
```

### AWS RDS 연결

프로덕션 또는 RDS를 사용하는 경우:

```bash
# .env 파일 설정
APP_DB_HOST=rldda-mysql.c9oeooq4qva3.ap-southeast-2.rds.amazonaws.com
APP_DB_PORT=3306
APP_DB_USER=<RDS 마스터 유저명>
APP_DB_PASSWORD=<RDS 마스터 비밀번호>
APP_DB_NAME=rldda
```

**RDS 연결 전 확인사항:**

#### 옵션 A: 퍼블릭 액세스 활성화 (개발/테스트 권장) ⭐

가장 간단한 방법입니다:

1. **RDS 퍼블릭 액세스 활성화**:
   - RDS → 데이터베이스 → `rldda-mysql` → "수정"
   - "연결" → "추가 구성" → "퍼블릭 액세스 가능" → "예"
   - "즉시 적용" 선택 후 저장

2. **보안 그룹 설정** (필수!):
   - RDS 보안 그룹 → 인바운드 규칙 편집
   - 타입: MySQL/Aurora (3306), 소스: **내 IP** (현재 IP만 허용)
   - ⚠️ 보안을 위해 `0.0.0.0/0` (전체 허용)은 사용하지 마세요

3. **.env 파일 설정**:
   ```env
   APP_DB_HOST=rldda-mysql.c9oeooq4qva3.ap-southeast-2.rds.amazonaws.com
   APP_DB_PORT=3306
   APP_DB_USER=<RDS 마스터 유저명>
   APP_DB_PASSWORD=<RDS 비밀번호>
   APP_DB_NAME=rldda
   ```

#### 옵션 B: SSH 터널 사용 (프로덕션 권장)

퍼블릭 액세스를 활성화하지 않고 EC2를 통해 안전하게 연결:

- 상세 가이드: [docs/RDS_SSH_TUNNEL.md](docs/RDS_SSH_TUNNEL.md)
- 요구사항: 같은 VPC 내 EC2 인스턴스 필요

**RDS 설정 자동화 스크립트:**

```bash
# RDS 연결 테스트 및 데이터베이스 자동 생성
rye run python scripts/setup_rds_database.py
```

이 스크립트는 다음을 수행합니다:
- RDS 연결 테스트
- `rldda` 데이터베이스가 없으면 자동 생성
- MySQL 버전 확인

### 마이그레이션 실행

데이터베이스 연결 후 마이그레이션을 실행합니다:

```bash
# 마이그레이션 자동 생성 (필요시)
rye run alembic revision -m "migration description" --autogenerate

# 마이그레이션 적용
rye run alembic upgrade head
```

### 연결 테스트

데이터베이스 연결을 테스트하려면:

```bash
# 서버 시작 시 연결 로그 확인
rye run uvicorn src.main:app --reload

# 또는 헬스체크 엔드포인트 확인
curl http://localhost:8000/health
```


