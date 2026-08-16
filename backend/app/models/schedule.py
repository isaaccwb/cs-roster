import json
from ..extensions import db


class ScheduleState(db.Model):
    __tablename__ = 't_schedule_state'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column('col_key', db.String(50), nullable=False, default='current')
    data = db.Column('col_data', db.Text, nullable=False, default='{}')
    updated_by = db.Column('col_updated_by', db.String(100), nullable=False, default='')
    updated_at = db.Column('col_updated_at', db.DateTime, nullable=False,
                           server_default=db.func.now(), onupdate=db.func.now())

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'key': self.key,
            'data': json.loads(self.data) if self.data else {},
            'updatedBy': self.updated_by,
            'updatedAt': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
        }
