from flask import Blueprint, request, g
from ..services.auth import AuthService
from ..utils.response import success, error
from ..utils.auth import login_required

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return error('请提供登录信息')

    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not email or not password:
        return error('邮箱和密码不能为空')

    result = AuthService.login(email, password)
    if not result:
        return error('邮箱或密码错误')

    return success(result, msg='登录成功')


@auth_bp.route('/info', methods=['GET'])
@login_required
def get_info():
    user = AuthService.get_user_info(g.current_user_id)
    if not user:
        return error('用户不存在', code=401), 401
    return success(user)
