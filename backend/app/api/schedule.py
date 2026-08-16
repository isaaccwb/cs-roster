from flask import Blueprint, request, g

from ..models.user import User
from ..services.schedule import ScheduleService
from ..utils.response import success, error
from ..utils.auth import login_required

schedule_bp = Blueprint('schedule', __name__, url_prefix='/api/scheduler')


@schedule_bp.route('/state', methods=['GET'])
@login_required
def get_state():
    try:
        result = ScheduleService.get_state()
        return success(result)
    except Exception as e:
        return error(str(e))


@schedule_bp.route('/state', methods=['PUT'])
@login_required
def save_state():
    try:
        user = User.query.get(g.current_user_id)
        if not user or not user.can_edit_scheduler:
            return error('无排班编辑权限，请联系管理员开通', code=403), 403
        body = request.get_json()
        if not body or 'data' not in body:
            return error('缺少 data 字段')
        data = body['data']
        updated_by = g.current_user_email or str(g.current_user_id)
        result = ScheduleService.save_state(data, updated_by)
        return success(result, msg='保存成功')
    except Exception as e:
        return error(str(e))
