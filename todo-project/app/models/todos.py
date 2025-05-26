from datetime import datetime
from zoneinfo import ZoneInfo

from app.models.session import SessionLocal
from app.models.create_tables import Todos
from utils.messages import ERROR_MESSAGES

class Todo:
  def __init__(self):
    self.session = SessionLocal()
    
  def find_by_user(self, id):
    """ログイン時のTodoの取得"""
    return (
      self.session.query(Todos).filter(Todos.user_id==id, Todos.deleted_at == None).all()
    )
    
  def insert_todo(self, title, body, user_id):
    """Todoの新規作成"""
    new_record = Todos(title=title, body=body, user_id=user_id)
    self.session.add(new_record)      
    self.session.commit()
    return new_record
    
  def select_todo_by_id(self, todo_id: int):
    """IDが一致するTodoの取得"""
    return (
      self.session.query(Todos).filter(Todos.id == todo_id, Todos.deleted_at == None).first()
    )
    
  def update_todo_by_id(self,title, body, todo_id: int):
    """IDが一致するTodoの更新"""
    result = self.session.query(Todos).filter(
            Todos.id == todo_id,
            Todos.deleted_at == None
        ).update({
            Todos.title: title,
            Todos.body: body,
            Todos.updated_at: datetime.now(ZoneInfo("Asia/Tokyo"))
        }, synchronize_session=False)
        
    if result == 0:
        raise ValueError(ERROR_MESSAGES["user_model"]["TODO_ID_NOT_FOUND"].format(todo_id))
      
    self.session.commit()
    return result
    
  def delete_todo_by_id(self, todo_id: int):
    """IDが一致するTodoの論理削除"""
    result = self.session.query(Todos).filter(
            Todos.id == todo_id, 
            Todos.deleted_at == None
    ).update({
            Todos.deleted_at: datetime.now(ZoneInfo("Asia/Tokyo"))
      }, synchronize_session=False)
    
    if result == 0:
        raise ValueError(ERROR_MESSAGES["user_model"]["TODO_ID_NOT_FOUND"].format(todo_id))
      
    self.session.commit()
    return result
