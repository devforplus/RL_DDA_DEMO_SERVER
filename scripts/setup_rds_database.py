#!/usr/bin/env python3
"""
RDS MySQL 데이터베이스 설정 스크립트

이 스크립트는 RDS에 연결하여 데이터베이스를 생성하고 연결을 테스트합니다.
.env 파일의 설정을 사용합니다.
"""

import sys
import asyncio
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

import aiomysql
from config import get_settings


async def setup_database():
    """RDS 데이터베이스 설정 및 테스트"""
    settings = get_settings()

    print(f"🔌 RDS 연결 시도...")
    print(f"   Host: {settings.db_host}")
    print(f"   Port: {settings.db_port}")
    print(f"   User: {settings.db_user}")
    print(f"   Database: {settings.db_name}")
    print()

    try:
        # 1. mysql 시스템 데이터베이스에 연결 (db_name 없이)
        print("📡 RDS 서버 연결 테스트...")
        conn = await aiomysql.connect(
            host=settings.db_host,
            port=settings.db_port,
            user=settings.db_user,
            password=settings.db_password,
            autocommit=True,
        )

        async with conn.cursor() as cursor:
            # 2. 데이터베이스 존재 확인
            await cursor.execute(
                "SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = %s",
                (settings.db_name,),
            )
            result = await cursor.fetchone()

            if result:
                print(f"✅ 데이터베이스 '{settings.db_name}'가 이미 존재합니다.")
            else:
                # 3. 데이터베이스 생성
                print(f"📝 데이터베이스 '{settings.db_name}' 생성 중...")
                await cursor.execute(
                    f"CREATE DATABASE {settings.db_name} "
                    "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                )
                print(f"✅ 데이터베이스 '{settings.db_name}' 생성 완료!")

            # 4. 데이터베이스 선택 후 연결 테스트
            await cursor.execute(f"USE {settings.db_name}")
            await cursor.execute("SELECT 1")
            await cursor.fetchone()

            # 5. 버전 정보 확인
            await cursor.execute("SELECT VERSION()")
            version = await cursor.fetchone()
            print(f"✅ MySQL 버전: {version[0]}")

        conn.close()

        print()
        print("=" * 60)
        print("🎉 RDS 데이터베이스 설정 완료!")
        print("=" * 60)
        print()
        print("다음 단계:")
        print("  1. 마이그레이션 실행:")
        print("     rye run alembic upgrade head")
        print()
        print("  2. 서버 시작:")
        print("     rye run uvicorn src.main:app --reload")
        print()

        return True

    except aiomysql.Error as e:
        print()
        print("❌ RDS 연결 실패!")
        print(f"   에러: {e}")
        print()
        print("확인사항:")
        print("  1. .env 파일의 RDS 연결 정보가 정확한가요?")
        print("  2. RDS 보안 그룹에서 현재 IP가 허용되어 있나요?")
        print("  3. RDS 인스턴스가 실행 중인가요?")
        print("  4. 퍼블릭 액세스가 활성화되어 있나요? (외부 접근 시)")
        print()
        return False

    except Exception as e:
        print()
        print(f"❌ 예상치 못한 오류: {e}")
        print()
        return False


if __name__ == "__main__":
    success = asyncio.run(setup_database())
    sys.exit(0 if success else 1)
