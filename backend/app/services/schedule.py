import json

from ..models.schedule import ScheduleState
from ..extensions import db


class ScheduleService:

    @staticmethod
    def get_state() -> dict | None:
        row = ScheduleState.query.filter_by(key='current').first()
        if not row:
            return None
        return row.to_dict()

    @staticmethod
    def save_state(data: dict, updated_by: str) -> dict:
        row = ScheduleState.query.filter_by(key='current').first()
        json_str = json.dumps(data, ensure_ascii=False)
        if row:
            row.data = json_str
            row.updated_by = updated_by
        else:
            row = ScheduleState(key='current', data=json_str, updated_by=updated_by)
            db.session.add(row)
        db.session.commit()
        return row.to_dict()
