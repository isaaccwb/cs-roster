import os
import sys
from pathlib import Path
from dotenv import load_dotenv

basedir = Path(__file__).resolve().parent

# 本地 python run.py 默认 development；线上 gunicorn 由平台注入 FLASK_ENV=production
env = os.environ.get('FLASK_ENV', 'development')

env_file = basedir / ('.env.production' if env == 'production' else '.env')
loaded = load_dotenv(env_file, override=True)

print(f"[startup] FLASK_ENV={env}", flush=True)
print(f"[startup] env_file={env_file} exists={env_file.exists()} loaded={loaded}", flush=True)
print(f"[startup] DB_HOST={os.environ.get('DB_HOST', '(not set)')}", flush=True)

from app import create_app

config_name = env
app = create_app(config_name)

print(f"[startup] DATABASE_URI={app.config['SQLALCHEMY_DATABASE_URI'][:80]}...", flush=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=True)
