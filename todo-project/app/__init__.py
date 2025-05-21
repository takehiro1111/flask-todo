import os

from flask import Flask
from flask_login import LoginManager, UserMixin, login_user, logout_user

flask_app = Flask(__name__)

def create_app(app):
  app.config['SECRET_KEY'] = 'a_very_secret_key_for_development_only'
  
  # CLIコマンドを登録
  from app.commands.db import create_tables_command, drop_tables_command
  app.cli.add_command(create_tables_command)
  app.cli.add_command(drop_tables_command)

  from app.views.auth_view import auth_bp
  app.register_blueprint(auth_bp)
  
  from app.views.todo_view import crud_bp
  app.register_blueprint(crud_bp)
  
  return app

todo_app = create_app(flask_app)
