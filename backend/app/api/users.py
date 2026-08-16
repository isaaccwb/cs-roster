from flask import Blueprint, request
from ..services.user import UserService
from ..utils.response import success, error
from ..utils.auth import login_required

users_bp = Blueprint('users', __name__, url_prefix='/api/users')


@users_bp.route('/list', methods=['GET'])
@login_required
def get_user_list():
    try:
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)
        keyword = request.args.get('keyword', '')
        result = UserService.get_list(page, page_size, keyword)
        return success(result)
    except Exception as e:
        return error(str(e))


@users_bp.route('/create', methods=['POST'])
@login_required
def create_user():
    try:
        data = request.get_json()
        result = UserService.create(data)
        return success(result, msg='创建成功')
    except ValueError as e:
        return error(str(e))
    except Exception as e:
        return error(str(e))


@users_bp.route('/update/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    try:
        data = request.get_json()
        result = UserService.update(user_id, data)
        if not result:
            return error('用户不存在')
        return success(result, msg='更新成功')
    except ValueError as e:
        return error(str(e))
    except Exception as e:
        return error(str(e))


@users_bp.route('/reset-password/<int:user_id>', methods=['POST'])
@login_required
def reset_password(user_id):
    try:
        data = request.get_json()
        new_password = data.get('password', '')
        result = UserService.reset_password(user_id, new_password)
        if not result:
            return error('用户不存在')
        return success(msg='密码重置成功')
    except ValueError as e:
        return error(str(e))
    except Exception as e:
        return error(str(e))


@users_bp.route('/delete/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    try:
        result = UserService.delete(user_id)
        if not result:
            return error('用户不存在')
        return success(msg='已停用')
    except Exception as e:
        return error(str(e))
