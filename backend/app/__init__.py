import logging
import decimal
from flask import Flask, request
from flask.json.provider import DefaultJSONProvider
from .extensions import db, migrate, cors


class CustomJSONProvider(DefaultJSONProvider):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super().default(o)

config = {
    'development': 'config.DevelopmentConfig',
    'production': 'config.ProductionConfig',
    'testing': 'config.TestingConfig'
}


def create_app(config_name='development'):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.json_provider_class = CustomJSONProvider
    app.json = CustomJSONProvider(app)
    app.config.from_object(config[config_name])

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    )
    app.json.ensure_ascii = False

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    if 'sqlite' not in app.config.get('SQLALCHEMY_DATABASE_URI', ''):
        from sqlalchemy import event
        with app.app_context():
            @event.listens_for(db.engine, 'connect')
            def set_charset(dbapi_conn, connection_record):
                cursor = dbapi_conn.cursor()
                cursor.execute("SET NAMES utf8mb4")
                cursor.close()

    from . import models  # noqa: F401 — ensure all models are registered with SQLAlchemy
    from .api import register_blueprints
    register_blueprints(app)

    @app.before_request
    def log_request():
        logging.getLogger('app.request').info(f'→ {request.method} {request.path}')

    @app.after_request
    def log_response(response):
        logging.getLogger('app.request').info(f'← {request.method} {request.path} [{response.status_code}]')
        return response

    register_error_handlers(app)

    with app.app_context():
        _test_db_connection(app)

    return app


def _test_db_connection(app):
    """启动时测试数据库连通性，输出诊断日志"""
    uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    logger = logging.getLogger(__name__)
    if 'sqlite' in uri:
        logger.info('[db-check] 使用 SQLite，跳过连通性测试')
        return
    try:
        result = db.session.execute(db.text('SELECT 1'))
        result.close()
        logger.info('[db-check] ✓ MySQL 连接成功')
        db.session.rollback()
    except Exception as e:
        logger.error(f'[db-check] ✗ MySQL 连接失败: {e}')


def register_error_handlers(app):
    from .utils.response import error

    @app.errorhandler(404)
    def not_found(e):
        return error('资源不存在', code=-1), 404

    @app.errorhandler(500)
    def internal_error(e):
        logging.getLogger(__name__).error(f'[500] {request.method} {request.path}: {e}', exc_info=True)
        return error(f'服务器内部错误: {str(e)}', code=500), 500

    @app.errorhandler(Exception)
    def unhandled_exception(e):
        logging.getLogger(__name__).error(f'[Unhandled] {request.method} {request.path}: {e}', exc_info=True)
        return error(f'服务器内部错误: {str(e)}', code=500), 500

    @app.errorhandler(405)
    def method_not_allowed(e):
        return error('请求方法不允许', code=-1), 405
