import os

from flask import Flask, g
from flask_login import LoginManager
from utils.logger import logger
from datetime import timedelta

flask_app = Flask(__name__)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = "このページにアクセスするにはログインが必要です。"
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
    """Flask-Loginのためのユーザーロード関数"""
    from app.models.users import User
    try:
        user_model = User()
        return user_model.select_user_by_id(int(user_id))
    except ValueError as e:
        logger.error(f"ユーザーロード中のエラー:数:{e}")
        return None
    except Exception as e:
        logger.error(f"予期せぬエラー: {e}")
        return None

def create_app(app):
    app.config['SECRET_KEY'] = 'a_very_secret_key_for_development_only'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=14)
    login_manager.init_app(app)

    # CLIコマンドを登録
    from app.commands.db import create_tables_command, drop_tables_command
    app.cli.add_command(create_tables_command)
    app.cli.add_command(drop_tables_command)
    
    from app.views.index_view import index_bp
    app.register_blueprint(index_bp)

    from app.views.auth_view import auth_bp
    app.register_blueprint(auth_bp)

    from app.views.todos_view import todo_bp
    app.register_blueprint(todo_bp)

    from app.views.user_view import user_bp
    app.register_blueprint(user_bp)
    
    from app.handlers.error_handlers import error_handlers
    error_handlers(app)

    @app.teardown_appcontext
    def close_db_session(exception=None):
        if hasattr(g, 'todo_model'):
            g.todo_model.session.close()
        
        if hasattr(g, 'user_model'):
            g.user_model.session.close()

    return app

todo_app = create_app(flask_app)
