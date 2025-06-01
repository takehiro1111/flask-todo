from zoneinfo import ZoneInfo
from datetime import datetime
from typing import Optional

from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session


class DeleteMixin:
  deleted_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, nullable=True, server_default=None, index=True)

  @classmethod
  def active_query(cls, session: Session):
    """論理削除されていないレコードをフィルタリングするクエリを返す"""
    return session.query(cls).filter(cls.deleted_at.is_(None))
    
  def soft_delete(self, tz="Asia/Tokyo"):
    """論理削除（deleted_atを現在時刻で更新）/ 呼び出し元でcommitを行う。"""
    self.deleted_at = datetime.now(ZoneInfo(tz))

class TodosBaseModeMixin:
  def _base_query_by_todo_id(self, session: Session, todo_id):
    """todo_idでfilterする場合"""
    from app.models.create_tables import Todos
    return Todos.active_query(session).filter(Todos.id == todo_id)
  
  def _base_query_by_user_id(self, session: Session, user_id):
    """user_idでfilterする場合"""
    from app.models.create_tables import Todos
    return Todos.active_query(session).filter(Todos.user_id == user_id)

class UsersBaseModeMixin:
  def _base_query_by_user_id(self, session: Session, id):
    """主キーのidでユーザーをfilterする場合"""
    from app.models.create_tables import Users
    return Users.active_query(session).filter(Users.id == id)
  
  def _base_query_by_email(self, session: Session, email):
    """メールアドレスでユーザーをfilterする場合"""
    from app.models.create_tables import Users
    return Users.active_query(session).filter(Users.email == email)
