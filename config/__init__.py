"""
配置包：集中管理 S3 / AWS 相关配置。

用法：
  from config import settings
  settings.S3_BUCKET
"""

from .settings import (  # noqa: F401
    AWS_REGION,
    MAX_CONTENT_LENGTH,
    S3_BUCKET,
    S3_PREFIX,
    S3_PRESIGNED_EXPIRES,
)


