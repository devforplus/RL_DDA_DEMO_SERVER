from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import boto3

from ..config import settings


@dataclass
class PresignResult:
    url: str
    expires_in: int


class S3Client:
    def __init__(self) -> None:
        self._client = boto3.client(
            "s3",
            endpoint_url=settings.s3_endpoint_url,
            region_name=settings.s3_region_name,
            aws_access_key_id=settings.s3_access_key_id,
            aws_secret_access_key=settings.s3_secret_access_key,
        )
        self._bucket = settings.s3_bucket

    def presign_get(self, key: str, expires_in: int = 3600) -> PresignResult:
        if not self._bucket:
            raise RuntimeError("S3 bucket is not configured")
        url = self._client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self._bucket, "Key": key},
            ExpiresIn=expires_in,
        )
        return PresignResult(url=url, expires_in=expires_in)


