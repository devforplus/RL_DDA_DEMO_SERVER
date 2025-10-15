# EC2 SSH 터널을 통한 RDS 연결

퍼블릭 액세스가 비활성화된 RDS에 안전하게 연결하는 방법입니다.

## 사전 요구사항

- 같은 VPC 내에 EC2 인스턴스가 있어야 함
- EC2에 SSH 접근 가능 (키 페어 필요)
- EC2의 보안 그룹이 RDS에 접근 가능해야 함

## SSH 터널 설정

### 1. EC2 보안 그룹 확인

EC2 인스턴스가 RDS에 접근할 수 있도록 설정:

1. RDS 보안 그룹 → 인바운드 규칙
2. 타입: `MySQL/Aurora`, 포트: `3306`
3. 소스: EC2 보안 그룹 ID (예: `sg-0d477b7590e30553b`)

### 2. SSH 터널 생성

**Windows (CMD/PowerShell):**

```bash
ssh -i "your-key.pem" -L 3306:rldda-mysql.c9oeooq4qva3.ap-southeast-2.rds.amazonaws.com:3306 ec2-user@your-ec2-public-ip -N
```

**Linux/Mac:**

```bash
ssh -i ~/.ssh/your-key.pem -L 3306:rldda-mysql.c9oeooq4qva3.ap-southeast-2.rds.amazonaws.com:3306 ec2-user@your-ec2-public-ip -N
```

**설명:**
- `-i "your-key.pem"`: EC2 SSH 키
- `-L 3306:RDS엔드포인트:3306`: 로컬 3306 포트를 RDS 3306으로 포워딩
- `-N`: SSH 세션만 유지 (셸 실행 안 함)

### 3. .env 파일 설정

SSH 터널을 통해 연결하므로 localhost 사용:

```env
APP_DB_HOST=127.0.0.1
APP_DB_PORT=3306
APP_DB_USER=admin
APP_DB_PASSWORD=your-rds-password
APP_DB_NAME=rldda
```

### 4. 연결 테스트

새 터미널에서 (SSH 터널은 유지):

```bash
rye run python scripts/setup_rds_database.py
```

## 자동화 (선택사항)

### SSH Config 설정

`~/.ssh/config` 파일에 추가:

```
Host rds-tunnel
    HostName your-ec2-public-ip
    User ec2-user
    IdentityFile ~/.ssh/your-key.pem
    LocalForward 3306 rldda-mysql.c9oeooq4qva3.ap-southeast-2.rds.amazonaws.com:3306
```

이후 간단하게 연결:

```bash
ssh -N rds-tunnel
```

## 장단점

### 장점 ✅
- RDS를 인터넷에 노출하지 않음 (보안)
- VPN 없이도 안전한 연결 가능
- 기존 EC2 인프라 활용

### 단점 ❌
- SSH 터널 세션을 계속 유지해야 함
- EC2 인스턴스가 필요함
- 설정이 다소 복잡함

