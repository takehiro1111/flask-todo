from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


from app.models.session import Session
from app.models.create_tables import Todos
from utils.messages import ERROR_MESSAGES

class TodoProcess:
  def __init__(self):
    self.session = Session()
    
  def select_todo_of_login_user(self, id):
    """ログイン時のTodoの取得"""
    try:
      todo = self.session.query(Todos).filter(Todos.user_id==id, Todos.deleted_at == None).all()
      return todo
    
    except SQLAlchemyError as e:
      self.session.rollback()
      raise ValueError(f"{ERROR_MESSAGES["todos_model"]["FETCH_FAILED"]}:{e}") from e
    
  def insert_todo_record(self,title, body, user_id):
    """Todoの新規作成"""
    try:
      new_record = Todos(title=title, body=body, user_id=user_id)
      insert_todo_record = self.session.add(new_record)
      self.session.commit()
      
      return insert_todo_record
    
    except SQLAlchemyError as e:
      self.session.rollback()
      raise ValueError(f"{ERROR_MESSAGES["todos_model"]["INSERT_FAILED"]}:{e}") from e
    
  def select_todo_by_id(self, todo_id: int):
    """IDが一致するTodoの取得"""
    try:
      todo = self.session.query(Todos).filter(Todos.id == todo_id, Todos.deleted_at == None).first()
      return todo
    except SQLAlchemyError as e:
      self.session.rollback()
      raise ValueError(ERROR_MESSAGES["todos_model"]["GET_BY_ID_FAILED"].format(todo_id))
    
  def update_todo_by_id(self,title, body, todo_id: int):
    """IDが一致するTodoの更新"""
    try:
      todo = self.session.query(Todos).filter(Todos.id == todo_id, Todos.deleted_at == None).first()
      todo.title = title
      todo.body = body
      self.session.commit()
      return todo

    except SQLAlchemyError as e:
      self.session.rollback()
      raise ValueError(ERROR_MESSAGES["todos_model"]["UPDATE_FAILED"].format(todo_id))
    
  def delete_todo_by_id(self, todo_id: int):
    """IDが一致するTodoの論理削除"""
    try:      
      # 論理削除
      todo_to_delete = self.session.query(Todos).filter(Todos.id == todo_id, Todos.deleted_at == None).first()
      
      if todo_to_delete:
        todo_to_delete.deleted_at = datetime.now(ZoneInfo("Asia/Tokyo"))
        self.session.commit()
      
      return todo_to_delete
      
    except SQLAlchemyError as e:
      self.session.rollback()
      raise ValueError(ERROR_MESSAGES["todos_model"]["DELETE_FAILED"].format(todo_id))

  def close(self):
    self.session.close()
