"""主页面路由蓝图"""
from flask import Blueprint, render_template

bp = Blueprint('main', __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/getpassword")
def getpassword():
    return render_template("index.html")


@bp.route("/upload")
def upload_page():
    return render_template("upload.html")


@bp.route("/timestamp")
def timestamp_page():
    return render_template("timestamp.html")


@bp.route("/hello")
def hello():
    return "Hello, world"

