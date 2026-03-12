import os
from typing import Optional


def _get_int(name: str, default: int) -> int:
    v = os.getenv(name)
    if v is None or v == "":
        return default
    try:
        return int(v)
    except ValueError:
        return default


try:
    # 本地私密配置（不会提交到仓库），
    # 请复制 credentials_local.py.example 为 credentials_local.py 并填写真实 AK/SK。
    from . import credentials_local  # type: ignore[attr-defined]
except Exception:
    credentials_local = None  # type: ignore[assignment]


# === S3 / AWS ===
# 说明：
# - 仓库内只保留非敏感的“默认值”或占位符。
# - 真实 AK/SK、桶名等可认为敏感的配置放在本地 credentials_local.py 或环境变量中，不提交到仓库。

# 访问密钥等：优先从本地私密配置读取，其次环境变量，仓库代码中不再写死真实值
_local_ak: Optional[str] = getattr(credentials_local, "AWS_ACCESS_KEY_ID", None) if credentials_local else None
_local_sk: Optional[str] = getattr(credentials_local, "AWS_SECRET_ACCESS_KEY", None) if credentials_local else None
_local_token: Optional[str] = getattr(credentials_local, "AWS_SESSION_TOKEN", None) if credentials_local else None
_local_bucket: Optional[str] = getattr(credentials_local, "S3_BUCKET", None) if credentials_local else None
_local_region: Optional[str] = getattr(credentials_local, "AWS_REGION", None) if credentials_local else None

AWS_ACCESS_KEY_ID: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID", _local_ak or "")
AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY", _local_sk or "")
AWS_SESSION_TOKEN: Optional[str] = os.getenv("AWS_SESSION_TOKEN", _local_token or "")

# S3 桶名称（优先本地私密配置，其次环境变量，最后是仓库内的默认值）
S3_BUCKET: str = os.getenv("S3_BUCKET", _local_bucket or "bucket-test")

# 区域：优先本地私密配置，其次环境变量，最后是默认值 ap-northeast-1
AWS_REGION: str = os.getenv("AWS_REGION", _local_region or "ap-northeast-1")

# 对象 ACL：公有可读（注意：若桶开启了 Object Ownership=Bucket owner enforced，则不能使用 ACL）
S3_OBJECT_ACL: str = os.getenv("S3_OBJECT_ACL", "public-read")

# 仍然允许通过环境变量覆盖前缀/过期时间等“非敏感”配置
S3_PREFIX: str = (os.getenv("S3_PREFIX") or "").strip().strip("/")
S3_PRESIGNED_EXPIRES: int = _get_int("S3_PRESIGNED_EXPIRES", 3600)


# === Flask ===
MAX_CONTENT_LENGTH: int = _get_int("MAX_CONTENT_LENGTH", 20 * 1024 * 1024)  # 20MB


APP_IP = os.getenv("APP_IP", "127.0.0.1")
# 避免与 macOS AirPlay 接收器占用 5000 冲突，改用 5001；可通过 APP_PORT 环境变量覆盖
APP_PORT = _get_int("APP_PORT", 5001)