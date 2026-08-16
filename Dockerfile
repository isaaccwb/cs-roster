# ---- 阶段1: 构建前端 ----
FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# ---- 阶段2: 最终镜像 ----
FROM python:3.12-slim
WORKDIR /app

# 安装 nginx 和 supervisor
RUN apt-get update && \
    apt-get install -y --no-install-recommends nginx supervisor && \
    rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# 版本号文件（前后端共用）
COPY VERSION ./VERSION

# 复制后端代码
COPY backend/ ./backend/

# 复制前端构建产物到 nginx 目录
COPY --from=frontend-build /app/frontend/dist /usr/share/nginx/html

# 复制 nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf
RUN rm -f /etc/nginx/sites-enabled/default

# 复制 supervisor 配置
COPY supervisord.conf /etc/supervisor/conf.d/app.conf

# 暴露端口
EXPOSE 8000

# 启动 supervisor（同时管理 nginx + gunicorn）
CMD ["supervisord", "-n", "-c", "/etc/supervisor/conf.d/app.conf"]
