import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from flask import g, current_app

load_dotenv()

db_user = os.environ.get('DB_USER', 'root')
db_pass = os.environ.get('DB_PASSWORD', 'root')
db_host = os.environ.get('DB_HOST', 'localhost')
db_port = os.environ.get('DB_PORT', '3306')
db_name = os.environ.get('DB_NAME', 'fk_todos')
charset = os.environ.get('DB_CHARSET', 'utf8mb4')
collation = os.environ.get('DB_COLLATION', 'utf8mb4_general_ci')

engine = create_engine(
  f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}?charset={charset}&collation={collation}",
  echo=True,
  )

# セッションファクトリー作成
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

"""セッション管理"""
@contextmanager
def db_session():
  """DBセッションを管理するコンテキストマネージャ"""
  from app.models.todos import Todo
  from app.models.users import User
  
  if hasattr(g, 'todo_model') and hasattr(g, 'user_model'):
      # 既に作成済みの場合はそれを再利用
      todo_model = g.todo_model
      user_model = g.user_model
  else:
    todo_model = Todo()
    user_model = User()
    
    g.todo_model = todo_model
    g.user_model = user_model
  
    if current_app.config.get('DEBUG', False):
        current_app.logger.debug('新しいデータベースセッションを作成しました')

  try:
      yield todo_model, user_model
  except Exception:
      todo_model.session.rollback() 
      user_model.session.rollback()
      raise
  finally:
    pass
      # todo_model.session.close()  
      # user_model.session.close()
