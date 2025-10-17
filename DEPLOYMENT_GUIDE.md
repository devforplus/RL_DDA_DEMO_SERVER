# Cloudflare 프로덕션 배포 가이드

## 현재 상태
- ✅ 로컬 개발 환경: 완료
- ⏳ 프로덕션 배포: 선택사항

## 로컬 개발 (현재 작동 중)

```bash
# 로컬 서버 실행
pnpm dev

# API 테스트
curl http://localhost:8787/health
curl http://localhost:8787/api/agents
```

**로컬 환경은 완전히 작동합니다!** 프론트엔드 개발을 바로 시작할 수 있습니다.

---

## 프로덕션 배포 (나중에 필요할 때)

### 1. Cloudflare Dashboard에서 D1 데이터베이스 생성

Wrangler CLI에서 인증 문제가 있으므로, **웹 인터페이스 사용**을 권장합니다:

1. **Cloudflare Dashboard 로그인**
   - https://dash.cloudflare.com
   - 계정: ijihyeon164@gmail.com

2. **Workers & Pages 선택**

3. **왼쪽 메뉴에서 D1 클릭**

4. **"Create database" 버튼 클릭**
   - Database name: `rl-dda-demo-db`
   - Location: 자동 선택 (가까운 위치)

5. **생성 완료 후 Database ID 복사**
   - 예: `12345678-1234-1234-1234-123456789abc`

### 2. wrangler.toml 업데이트

```toml
[[d1_databases]]
binding = "DB"
database_name = "rl-dda-demo-db"
database_id = "여기에-복사한-Database-ID-붙여넣기"
```

### 3. 프로덕션 마이그레이션 실행

```bash
pnpm db:migrate:prod
```

### 4. R2 버킷 생성

**Dashboard에서:**
1. R2 메뉴로 이동
2. "Create bucket" 클릭
3. Bucket name: `rl-dda-demo-replays`

**또는 CLI로 (인증 문제 해결된 경우):**
```bash
pnpm wrangler r2 bucket create rl-dda-demo-replays
```

### 5. 환경 변수 설정 (프로덕션)

```bash
# INGEST_SECRET 설정
pnpm wrangler secret put INGEST_SECRET
# 프롬프트가 나오면 안전한 랜덤 문자열 입력
```

### 6. 배포

```bash
pnpm deploy
```

### 7. 커스텀 도메인 연결

**Dashboard에서:**
1. 배포된 Worker 선택
2. "Settings" > "Triggers" > "Custom Domains"
3. "Add Custom Domain" 클릭
4. 이미 등록한 도메인 입력
5. DNS 레코드 자동 설정됨

---

## 문제 해결

### Wrangler 인증 오류

**증상:**
```
[ERROR] Authentication error [code: 10000]
```

**해결 방법:**
1. **Cloudflare Dashboard 사용** (권장)
   - 웹 인터페이스로 모든 설정 가능

2. **재로그인 시도**
   ```bash
   pnpm wrangler logout
   pnpm wrangler login
   ```

3. **API Token 사용** (고급)
   - Dashboard > My Profile > API Tokens
   - "Edit Cloudflare Workers" 템플릿 사용
   - `.env`에 추가: `CLOUDFLARE_API_TOKEN=your-token`

### 로컬 개발만 계속하기

프로덕션 배포 없이 로컬에서만 개발하려면:

```bash
# 이것만 실행하면 됩니다
pnpm dev
```

모든 API가 `http://localhost:8787`에서 작동합니다!

---

## 권장 워크플로우

### Phase 1: 로컬 개발 (현재) ✅
- 로컬 서버로 프론트엔드 연동
- 기능 개발 및 테스트
- Git으로 버전 관리

### Phase 2: 프로덕션 배포 (필요할 때)
- Cloudflare Dashboard에서 리소스 생성
- `wrangler.toml`에 ID 입력
- 배포 실행
- 도메인 연결

---

## 비용

- **로컬 개발**: 무료
- **Cloudflare Workers**: 무료 티어로 충분
  - 100,000 요청/일
  - D1: 5GB 저장공간
  - R2: 10GB 저장공간

---

## 다음 단계

**지금 바로 할 수 있는 것:**
1. 로컬 서버 실행 (`pnpm dev`)
2. 프론트엔드에서 `http://localhost:8787/api/...` 연동
3. 기능 개발 진행

**나중에 배포할 때:**
1. 위 가이드 따라 Dashboard에서 설정
2. `wrangler.toml` 업데이트
3. 배포 실행

