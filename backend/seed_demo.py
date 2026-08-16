from app import create_app
from app.extensions import db
from app.models.user import User
app = create_app()
with app.app_context():
    db.create_all()
    for u in [
        {'email':'admin@example.com','name':'Admin','password':'demo123456','can_edit_scheduler':1},
        {'email':'viewer@example.com','name':'Viewer','password':'demo123456','can_edit_scheduler':0},
    ]:
        if not User.query.filter_by(email=u['email']).first():
            user = User(email=u['email'],name=u['name'],is_active=1,can_edit_scheduler=u['can_edit_scheduler'])
            user.set_password(u['password'])
            db.session.add(user)
    db.session.commit()
    print('[seed] Done.')
