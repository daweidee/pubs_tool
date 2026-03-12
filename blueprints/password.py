"""密码生成路由蓝图"""
from flask import Blueprint, jsonify, request

from utils.password import generate_password

bp = Blueprint('password', __name__, url_prefix='/api')


@bp.route("/generate-password", methods=["POST"])
def generate_password_api():
    """生成密码的API端点"""
    try:
        data = request.get_json() or {}
        
        # 获取参数，设置默认值
        length = int(data.get('length', 16))
        include_uppercase = data.get('include_uppercase', True)
        include_lowercase = data.get('include_lowercase', True)
        include_digits = data.get('include_digits', True)
        include_special = data.get('include_special', True)
        
        # 验证长度范围
        if length < 4:
            length = 4
        elif length > 128:
            length = 128
        
        # 验证至少选择一种字符类型
        if not any([include_uppercase, include_lowercase, include_digits, include_special]):
            return jsonify({
                "success": False,
                "error": "至少需要选择一种字符类型"
            }), 400
        
        password = generate_password(
            length=length,
            include_uppercase=include_uppercase,
            include_lowercase=include_lowercase,
            include_digits=include_digits,
            include_special=include_special
        )
        
        return jsonify({
            "success": True,
            "password": password
        })
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": "无效的参数: " + str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

