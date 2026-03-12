"""文件上传路由蓝图"""
from flask import Blueprint, jsonify, request
from botocore.exceptions import BotoCoreError, ClientError

from utils.s3 import upload_file_to_s3

bp = Blueprint('upload', __name__, url_prefix='/api')


@bp.route("/upload-s3", methods=["POST"])
def upload_s3_api():
    """
    通过 multipart/form-data 上传文件到 S3。
    配置：
    - config/settings.py: S3_BUCKET, AWS_REGION, S3_OBJECT_ACL 等
    - config/credentials_local.py: 本地 AK/SK（可选；也可使用 IAM Role/AWS CLI 默认凭证链）
    """
    if "file" not in request.files:
        return jsonify({"success": False, "error": "没有收到文件字段 file"}), 400

    f = request.files["file"]
    if not f or not f.filename:
        return jsonify({"success": False, "error": "文件为空或未选择文件"}), 400

    try:
        result = upload_file_to_s3(f, f.filename)
        return jsonify({
            "success": True,
            **result
        })
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 500
    except (BotoCoreError, ClientError) as e:
        return jsonify({"success": False, "error": f"S3 上传失败: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

