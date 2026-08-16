import os
basedir = os.path.abspath(os.path.dirname(__file__))

def build_database_url():
    url = os.environ.get('DATABASE_URL', '')
    if url: return url
    host = os.environ.get('DB_HOST', '')
    user = os.environ.get('DB_USER', '')
    password = os.environ.get('DB_PASSWORD', '')
    port = os.environ.get('DB_PORT', '3306')
    name = os.environ.get('DB_NAME', '')
    if host and user and name and password:
        return f'mysql+pymysql://{user}:{password}@{host}:{port}/{name}?charset=utf8mb4'
    return f'sqlite:///{os.path.join(basedir, "dev.db")}'

_db_url = build_database_url()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-change-me')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-change-me')
    SQLALCHEMY_DATABASE_URI = _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    SQLALCHEMY_ENGINE_OPTIONS = (
        {'connect_args': {'check_same_thread': False}}
        if 'sqlite' in _db_url
        else {'pool_pre_ping': True, 'pool_recycle': 3600}
    )
