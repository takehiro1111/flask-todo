from datetime import datetime
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


from app.models.session import engine, Base, Session
from app.models.create_tables import Todos


class TodoProcess:
  def __init__(self):
    self.session = Session()
    
  def select_todo_of_login_user(self, id):
    try:
      todo = self.session.query(Todos).filter(Todos.user_id==id).all()
      return todo
    
    except SQLAlchemyError as e:
      self.session.rollback()
      raise ValueError(f"Todo情報の取得に失敗しました。:{e}") from e
    
  def insert_todo_record(self,title, body, user_id):
    try:
      new_record = Todos(title=title, body=body, user_id=user_id)
      insert_todo_record = self.session.add(new_record)
      self.session.commit()
      
      return insert_todo_record
    
    except SQLAlchemyError as e:
      self.session.rollback()
      raise ValueError(f"Todo情報の取得に失敗しました。:{e}") from e

  def close(self):
    self.session.close()
