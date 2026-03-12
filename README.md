## Flask 工具小站

基于 Flask 的小工具集合，包含：

- **密码生成器**：前端可视化配置（长度、字符类型），调用后端 `/api/generate-password` 生成随机强密码。
- **S3 文件上传**：在页面选择文件，一键上传到 Amazon S3，返回对象 Key 与临时下载链接 `/api/upload-s3`。
- **时间戳转换**：时间戳 ↔ 标准时间的双向转换，支持毫秒/秒单位、复制功能等。

---

## 功能概览

- **页面路由（`blueprints/main.py`）**
  - `/`、`/getpassword`：密码生成页面（`templates/index.html`）
  - `/upload`：上传 S3 页面（`templates/upload.html`）
  - `/timestamp`：时间戳转换页面（`templates/timestamp.html`）
  - `/hello`：简单健康检查接口

- **API 路由**
  - `POST /api/generate-password`（`blueprints/password.py`）
    - 请求 JSON 参数：
      - `length`：密码长度，默认 `16`，最小 `4`，最大 `128`
      - `include_uppercase`：是否包含大写字母，默认 `true`
      - `include_lowercase`：是否包含小写字母，默认 `true`
      - `include_digits`：是否包含数字，默认 `true`
      - `include_special`：是否包含特殊符号，默认 `true`
    - 响应示例：
      - 成功：`{"success": true, "password": "..." }`
      - 失败：`{"success": false, "error": "错误信息" }`
  - `POST /api/upload-s3`（`blueprints/upload.py`）
    - 表单字段：`file`（multipart/form-data）
    - 成功时返回：`bucket`、`key` 和 `presigned_url`（临时下载链接）

---

## 运行环境

- Python 3.12（或兼容 3.10+）
- 依赖见 `requirements.txt`：
  - `flask`
  - `boto3`

建议在本地使用虚拟环境：

```bash
cd flask_app
python3 -m venv .venv
source .venv/bin/activate  # Windows 使用: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 配置说明

### 1. 应用与上传限制（`config/settings.py`）

- `MAX_CONTENT_LENGTH`：上传文件大小限制，默认 20MB，可通过环境变量覆盖：

```bash
export MAX_CONTENT_LENGTH=$((20 * 1024 * 1024))
```

- 运行 IP 与端口：
  - `APP_IP`：默认 `127.0.0.1`，可用环境变量 `APP_IP` 覆盖。
  - `APP_PORT`：默认 `5001`，可用环境变量 `APP_PORT` 覆盖（避免与 macOS AirPlay 占用 5000）。

### 2. AWS / S3 配置

所有 S3 相关配置都集中在 `config/settings.py`，并**优先从本地私密文件或环境变量读取**，避免将真实密钥提交到仓库。

读取优先级（从高到低）：

1. 本地私密文件 `config/credentials_local.py`（已在 `.gitignore` 中，不会提交）
2. 环境变量（例如 `AWS_ACCESS_KEY_ID`、`S3_BUCKET` 等）
3. 仓库中的默认值（仅作占位 / 测试用途）

主要配置项：

- `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` / `AWS_SESSION_TOKEN`
- `S3_BUCKET`：S3 桶名称
- `AWS_REGION`：区域，例如 `ap-northeast-1`
- `S3_OBJECT_ACL`：对象 ACL，默认 `public-read`
- `S3_PREFIX`：上传目录前缀（可选）
- `S3_PRESIGNED_EXPIRES`：预签名 URL 过期时间（秒），默认 3600

### 3. 本地私密配置（推荐）

复制示例文件并填写自己的值：

```bash
cp config/credentials_local.py.example config/credentials_local.py
```

编辑 `config/credentials_local.py`，示例结构如下：

```python
AWS_ACCESS_KEY_ID = "你的AK"
AWS_SECRET_ACCESS_KEY = "你的SK"
AWS_SESSION_TOKEN = None  # 如使用 STS，则填写临时 Token

S3_BUCKET = "your-bucket-name"
AWS_REGION = "ap-northeast-1"
```

> 提示：`config/credentials_local.py` 已在 `.gitignore` 中，适合放本地开发密钥。

### 4. 环境变量脚本（可选）

`config/env.sh` 提供了一个简单的 shell 脚本示例，可用于本地快速导出环境变量：

```bash
source config/env.sh
```

根据需要编辑其中的：

- `S3_BUCKET`
- `AWS_REGION`
- 以及注释里的 `S3_PREFIX`、`S3_PRESIGNED_EXPIRES` 等。

---

## 启动项目

在项目根目录（包含 `app.py` 的目录）执行：

```bash
cd flask_app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 配置 AWS / S3（任选其一或组合）
# 1) 使用 config/credentials_local.py
cp config/credentials_local.py.example config/credentials_local.py
vim config/credentials_local.py  # 或任意编辑器填入自己的 AK/SK、S3_BUCKET、AWS_REGION

# 2) 或使用环境变量（示例）
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
export S3_BUCKET="your-bucket"
export AWS_REGION="ap-northeast-1"

python app.py
```

默认将启动在 `http://127.0.0.1:5001/`。

---

## 主要代码结构

- `app.py`：Flask 应用入口，创建 app 并注册所有蓝图。
- `config/`
  - `settings.py`：全局配置（Flask、S3 等），从环境变量与本地私密文件读取。
  - `credentials_local.py.example`：本地私密配置示例（复制为 `credentials_local.py` 使用）。
  - `env.sh`：本地开发环境变量脚本示例。
- `blueprints/`
  - `main.py`：页面路由（首页、上传页、时间戳工具页等）。
  - `password.py`：密码生成 API。
  - `upload.py`：上传文件到 S3 的 API。
- `templates/`
  - `base.html`：基础布局与样式。
  - `index.html`：密码生成器页面。
  - `upload.html`：S3 上传页面。
  - `timestamp.html`：时间戳转换工具页面。
- `utils/`
  - `password.py`：密码生成工具函数。
  - `s3.py`：S3 上传与对象键构造工具。

---

## 注意事项

- **不要把真实 AWS 密钥直接写进仓库中的 `settings.py` 或其他被追踪文件**。
- 如不使用显式 AK/SK，可以使用：
  - IAM Role（在 EC2 / ECS / Lambda 等环境）
  - 本地已配置好的 AWS CLI 凭证（`~/.aws/credentials`）
- 上传到 S3 时，默认对象 ACL 为 `public-read`，请根据自己的安全要求进行调整。

