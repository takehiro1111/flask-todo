import os

from flask import Flask
flask_app = Flask(__name__)

def create_app(app):
  app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))
  
  # CLIコマンドを登録
  from app.commands.db import create_tables_command, drop_tables_command
  app.cli.add_command(create_tables_command)
  app.cli.add_command(drop_tables_command)

  from app.views.auth import auth_bp
  app.register_blueprint(auth_bp)
  
  from app.views.crud import crud_bp
  app.register_blueprint(crud_bp)
  
  return app

todo_app = create_app(flask_app)
