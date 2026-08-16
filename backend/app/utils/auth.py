from functools import wraps
from flask import request, g
from jose import jwt, JWTError
import os
from .response import error


SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
ALGORITHM = 'HS256'


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return error('未登录', code=401), 401

        token = auth_header[7:]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            g.current_user_id = int(payload['sub'])
            g.current_user_email = payload.get('email', '')
        except JWTError:
            return error('登录已过期，请重新登录', code=401), 401

        return f(*args, **kwargs)
    return decorated
