from app.models.session import SessionLocal
from app.models.create_tables import Todos
from utils.messages import ERROR_MESSAGES

class Todo:
  def __init__(self):
    self.session = SessionLocal()
    
  def _base_query_by_todo_id(self, todo_id):
    """todo_idでfilterする場合"""
    return Todos.active_query(self.session).filter(Todos.id == todo_id)
  
  def _base_query_by_user_id(self, user_id):
    """user_idでfilterする場合"""
    return Todos.active_query(self.session).filter(Todos.user_id == user_id)
    
  def find_by_user(self, user_id):
    """ログイン時のTodoの取得"""
    return (
      self._base_query_by_user_id(user_id).all()
    )
    
  def insert_todo(self, title, body, user_id):
    """Todoの新規作成"""
    new_record = Todos(title=title, body=body, user_id=user_id)
    self.session.add(new_record)      
    self.session.commit()
    return new_record
    
  def select_todo_by_id(self, todo_id: int):
    """IDが一致するTodoの取得"""
    return self._base_query_by_todo_id(todo_id).first()
    
  def update_todo_by_id(self,title, body, todo_id: int):
    """IDが一致するTodoの更新"""
    todo_to_update = self._base_query_by_todo_id(todo_id).first()
        
    if not todo_to_update:
        raise ValueError(ERROR_MESSAGES["user_model"]["TODO_ID_NOT_FOUND"].format(todo_id))
      
    todo_to_update.title = title
    todo_to_update.body = body
    self.session.commit()
    return todo_to_update
    
  def soft_delete_todo_by_id(self, todo_id: int):
    """IDが一致するTodoの論理削除"""    
    todo_to_delete = self._base_query_by_todo_id(todo_id).first()
    
    if not todo_to_delete:
        raise ValueError(ERROR_MESSAGES["user_model"]["TODO_ID_NOT_FOUND"].format(todo_id))

    todo_to_delete.soft_delete()
    self.session.commit()
    return True
