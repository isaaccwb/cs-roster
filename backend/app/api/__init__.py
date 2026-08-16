def register_blueprints(app):
    from .auth import auth_bp
    from .health import health_bp
    from .users import users_bp
    from .schedule import schedule_bp
    from .upload import upload_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(schedule_bp)
    app.register_blueprint(upload_bp)
