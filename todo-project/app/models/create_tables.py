from datetime import datetime
from sqlalchemy import String, Integer, Text, TIMESTAMP,ForeignKey
from sqlalchemy.sql import text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import TINYINT as Tinyint
from typing import List, Optional

from app.models.session import engine, Base

# テーブルの作成
class Users(Base):
  __tablename__ = "users"
  __table_args__=({"mysql_charset": "utf8mb4"})
  id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String(100), nullable=False)
  email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
  password_hash: Mapped[str] = mapped_column(String(500), nullable=False)
  created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
  updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
  deleted_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, nullable=True, server_default=None)
  
  todos: Mapped[List["Todos"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Todos(Base):
  __tablename__ = "todos"
  id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  title: Mapped[str] = mapped_column(String(100), nullable=False)
  body: Mapped[str] = mapped_column(Text, nullable=True)
  is_completed: Mapped[bool] = mapped_column(Tinyint(1), server_default="1", index=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
  created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), index=True)
  updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), index=True)
  deleted_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, nullable=True, server_default=None, index=True)
  
  user: Mapped["Users"] = relationship(back_populates="todos")
  
# テーブルを作成
Base.metadata.create_all(engine)
