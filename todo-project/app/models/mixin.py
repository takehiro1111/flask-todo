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
