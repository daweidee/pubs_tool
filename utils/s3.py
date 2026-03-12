"""S3 工具模块"""
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from werkzeug.utils import secure_filename
from datetime import datetime

from config import settings


def create_s3_client():
    """
    基于 config/settings.py 中的静态配置创建 S3 客户端，
    不再依赖环境变量里的 AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY / AWS_REGION。
    """
    client_kwargs: dict = {}

    if settings.AWS_REGION:
        client_kwargs["region_name"] = settings.AWS_REGION

    # 如果在配置文件中显式配置了 AK/SK，则优先使用
    if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
        client_kwargs["aws_access_key_id"] = settings.AWS_ACCESS_KEY_ID
        client_kwargs["aws_secret_access_key"] = settings.AWS_SECRET_ACCESS_KEY

    if getattr(settings, "AWS_SESSION_TOKEN", None):
        client_kwargs["aws_session_token"] = settings.AWS_SESSION_TOKEN

    return boto3.client("s3", **client_kwargs)


def build_s3_key(filename: str) -> str:
    """构建 S3 对象键"""
    prefix = settings.S3_PREFIX
    safe_name = secure_filename(filename) or "file"
    # 仅用"当前时间"命名：YYYYMMDD_HHMMSS_mmm + 原扩展名
    # 说明：毫秒用于降低同一秒内多次上传的重名概率
    ext = ""
    if "." in safe_name:
        ext = "." + safe_name.rsplit(".", 1)[-1]
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    key = f"{ts}{ext}"
    return f"{prefix}/{key}" if prefix else key


def upload_file_to_s3(file_obj, filename: str):
    """
    上传文件到 S3
    
    Args:
        file_obj: 文件对象
        filename: 原始文件名
        
    Returns:
        dict: 包含 bucket, key, presigned_url 的字典
        
    Raises:
        (BotoCoreError, ClientError): S3 上传失败时抛出
    """
    bucket = settings.S3_BUCKET
    if not bucket:
        raise ValueError("未配置环境变量 S3_BUCKET")
    
    key = build_s3_key(filename)
    
    extra_args = {}
    content_type = file_obj.mimetype
    if content_type:
        extra_args["ContentType"] = content_type
    # 设置对象 ACL：公有可读
    if getattr(settings, "S3_OBJECT_ACL", None):
        extra_args["ACL"] = settings.S3_OBJECT_ACL
    
    s3 = create_s3_client()
    # 直接流式上传（不落盘）
    s3.upload_fileobj(file_obj, bucket, key, ExtraArgs=extra_args or None)
    
    # 返回一个短期下载链接（默认 1 小时）
    presigned_url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=settings.S3_PRESIGNED_EXPIRES,
    )
    
    return {
        "bucket": bucket,
        "key": key,
        "presigned_url": presigned_url,
    }

