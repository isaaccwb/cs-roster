import os
from flask import Blueprint
from app.extensions import db

health_bp = Blueprint('health', __name__, url_prefix='/api')


@health_bp.route('/health')
def health_check():
    version = _read_version()
    try:
        db.session.execute(db.text('SELECT 1'))
        return {'code': 0, 'msg': 'ok', 'data': {'status': 'healthy', 'version': version, 'database': 'connected'}}
    except Exception:
        return {'code': -1, 'msg': 'unhealthy', 'data': {'status': 'unhealthy', 'version': version, 'database': 'disconnected'}}, 503


def _read_version():
    version_file = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'VERSION')
    try:
        with open(version_file) as f:
            return f.read().strip()
    except FileNotFoundError:
        return 'unknown'
