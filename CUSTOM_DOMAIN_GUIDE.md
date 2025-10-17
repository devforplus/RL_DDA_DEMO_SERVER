# 커스텀 도메인 연결 가이드

## 문제 상황
- ❌ `https://api.devfor.plus` → 522 에러 (연결 안됨)
- ✅ `https://rl-dda-demo-back.ijihyeon164.workers.dev` → 정상 작동

## 원인
커스텀 도메인이 Worker에 연결되지 않았습니다.

---

## 🔧 해결 방법: Cloudflare Dashboard에서 설정

### 1단계: Dashboard 접속

https://dash.cloudflare.com → 로그인

### 2단계: Worker 선택

1. 왼쪽 메뉴에서 **"Workers & Pages"** 클릭
2. **"rl-dda-demo-back"** Worker 선택

### 3단계: Custom Domain 추가

1. **"Settings"** 탭 클릭
2. **"Triggers"** 섹션으로 스크롤
3. **"Custom Domains"** 박스 찾기
4. **"Add Custom Domain"** 버튼 클릭

### 4단계: 도메인 입력

1. 도메인 입력: **`api.devfor.plus`**
2. **"Add Custom Domain"** 클릭

### 5단계: DNS 자동 설정 확인

- Cloudflare가 자동으로 DNS 레코드를 설정합니다
- 몇 분 정도 기다리면 활성화됩니다

---

## ✅ 확인 방법

DNS 전파 후 (1-5분):

```bash
curl https://api.devfor.plus/health
# {"status":"ok"} 응답이 나오면 성공!
```

---

## 📋 설정 완료 후

프론트엔드 환경 변수:

```env
# 프로덕션
VITE_API_URL=https://api.devfor.plus

# 로컬 개발 (선택사항)
VITE_API_URL=http://localhost:8787
```

---

## 🚨 임시 해결책

커스텀 도메인 설정 전까지 Worker URL 직접 사용:

```env
# 임시로 이렇게 사용
VITE_API_URL=https://rl-dda-demo-back.ijihyeon164.workers.dev
```

이 URL은 **지금 바로 작동**합니다!

---

## 🔍 문제 해결

### DNS 전파가 안 되는 경우

1. **DNS 레코드 확인**
   - Cloudflare Dashboard → DNS → Records
   - `api.devfor.plus` CNAME 레코드가 있는지 확인

2. **프록시 상태 확인**
   - DNS 레코드의 "Proxy status"가 "Proxied"(주황색 구름)인지 확인

3. **캐시 초기화**
   - 브라우저 캐시 삭제
   - 시크릿 모드로 테스트

### 522 에러가 계속 발생하는 경우

1. **Worker 배포 상태 확인**
   ```bash
   pnpm wrangler deployments list
   ```

2. **Worker 재배포**
   ```bash
   pnpm wrangler deploy
   ```

3. **커스텀 도메인 제거 후 재추가**
   - Dashboard에서 도메인 삭제
   - 다시 추가

---

## 📊 현재 상태

| URL | 상태 | 용도 |
|-----|------|------|
| `https://rl-dda-demo-back.ijihyeon164.workers.dev` | ✅ 작동 | 임시 사용 가능 |
| `https://api.devfor.plus` | ❌ 522 에러 | 연결 필요 |

---

## 💡 권장 사항

1. **지금**: Worker URL로 프론트엔드 연동하여 개발 진행
2. **나중에**: 여유 있을 때 Dashboard에서 커스텀 도메인 설정
3. **배포 전**: 커스텀 도메인 설정 완료 확인

---

## 🎯 결론

**바로 해결하려면**: 프론트엔드에서 Worker URL 사용
**근본적 해결**: Cloudflare Dashboard에서 커스텀 도메인 추가 (5분 소요)

