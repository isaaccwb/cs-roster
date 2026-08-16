from ..models.user import User
from ..extensions import db


class UserService:

    @staticmethod
    def get_list(page: int, page_size: int, keyword: str = '') -> dict:
        query = User.query
        if keyword:
            query = query.filter(
                db.or_(
                    User.name.like(f'%{keyword}%'),
                    User.email.like(f'%{keyword}%'),
                )
            )
        query = query.order_by(User.created_at.desc())
        paginated = query.paginate(page=page, per_page=page_size, error_out=False)
        return {
            'list': [item.to_dict() for item in paginated.items],
            'total': paginated.total,
            'page': page,
            'page_size': page_size
        }

    @staticmethod
    def create(data: dict) -> dict:
        email = data.get('email', '').lower().strip()
        if not email:
            raise ValueError('邮箱不能为空')

        existing = User.query.filter_by(email=email).first()
        if existing:
            raise ValueError('该邮箱已存在')

        password = data.get('password', '').strip()
        if not password or len(password) < 6:
            raise ValueError('密码长度至少6位')

        user = User(
            email=email,
            name=data.get('name', '').strip(),
            is_active=1,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user.to_dict()

    @staticmethod
    def update(user_id: int, data: dict) -> dict | None:
        user = User.query.get(user_id)
        if not user:
            return None

        if 'name' in data:
            user.name = data['name'].strip()
        if 'email' in data:
            new_email = data['email'].lower().strip()
            if new_email != user.email:
                existing = User.query.filter_by(email=new_email).first()
                if existing:
                    raise ValueError('该邮箱已被其他用户使用')
                user.email = new_email
        if 'is_active' in data:
            user.is_active = 1 if data['is_active'] else 0
        if 'can_edit_scheduler' in data:
            user.can_edit_scheduler = 1 if data['can_edit_scheduler'] else 0

        db.session.commit()
        return user.to_dict()

    @staticmethod
    def reset_password(user_id: int, new_password: str) -> bool:
        user = User.query.get(user_id)
        if not user:
            return False

        if not new_password or len(new_password) < 6:
            raise ValueError('密码长度至少6位')

        user.set_password(new_password)
        db.session.commit()
        return True

    @staticmethod
    def delete(user_id: int) -> bool:
        user = User.query.get(user_id)
        if not user:
            return False
        user.is_active = 0
        db.session.commit()
        return True
