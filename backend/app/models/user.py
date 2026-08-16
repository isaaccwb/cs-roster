from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 't_users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column('col_email', db.String(100), unique=True, nullable=False)
    password_hash = db.Column('col_password_hash', db.String(256), nullable=False)
    name = db.Column('col_name', db.String(50), nullable=False, default='')
    is_active = db.Column('col_is_active', db.Integer, nullable=False, default=1)
    can_edit_scheduler = db.Column('col_can_edit_scheduler', db.Integer, nullable=False, default=0)
    created_at = db.Column('col_created_at', db.DateTime, default=datetime.utcnow)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'is_active': self.is_active,
            'can_edit_scheduler': self.can_edit_scheduler,
        }
