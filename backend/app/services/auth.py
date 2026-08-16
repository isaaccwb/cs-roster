from datetime import datetime, timedelta
from jose import jwt
import os

from ..models.user import User

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
ALGORITHM = 'HS256'
TOKEN_EXPIRE_HOURS = 24


class AuthService:

    @staticmethod
    def login(email: str, password: str) -> dict | None:
        user = User.query.filter_by(email=email.lower().strip(), is_active=1).first()
        if not user or not user.check_password(password):
            return None

        token = jwt.encode(
            {
                'sub': str(user.id),
                'email': user.email,
                'exp': datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS),
            },
            SECRET_KEY,
            algorithm=ALGORITHM,
        )
        return {'token': token, 'user': user.to_dict()}

    @staticmethod
    def get_user_info(user_id: int) -> dict | None:
        user = User.query.get(user_id)
        if not user or not user.is_active:
            return None
        return user.to_dict()
