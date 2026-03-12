from flask import Flask

from config import settings
from blueprints import main, password, upload

'''
cd /Users/hypergo/PyCursor/20250903/flask_app
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
'''


def create_app() -> Flask:
    """创建并配置 Flask 应用"""
    app = Flask(__name__)
    
    # 限制上传大小（默认 20MB）
    app.config["MAX_CONTENT_LENGTH"] = settings.MAX_CONTENT_LENGTH
    
    # 注册蓝图
    app.register_blueprint(main.bp)
    app.register_blueprint(password.bp)
    app.register_blueprint(upload.bp)
    
    return app


app = create_app()


if __name__ == "__main__":
    app.run(host=settings.APP_IP, port=settings.APP_PORT, debug=True)
