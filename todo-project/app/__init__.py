import os

from flask import Flask

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))
  
  # CLIコマンドを登録
  from app.commands.db import create_tables_command, drop_tables_command
  app.cli.add_command(create_tables_command)
  app.cli.add_command(drop_tables_command)

  def register_blue_prints(app):
    from app.views.auth import auth_bp
    app.register_blueprint(auth_bp)

  register_blue_prints(app)
  
  return app


app = create_app()
