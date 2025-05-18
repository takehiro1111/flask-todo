from datetime import datetime
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.models.session import engine, Base, Session
from app.models.create_tables import Users

class UserProcess:
  def __init__(self):
    self.session = Session()

  # ユーザー情報の追加
  def insert_user(self, name: str, email: str, password_hash: str):
    """ユーザー情報を登録"""
    try:
      new_user = Users(name=name, email=email, password_hash=password_hash)
      self.session.add(new_user)
      self.session.commit()
      
      return new_user
      
    except IntegrityError as e:
      self.session.rollback()
      raise ValueError("ユーザー情報の登録に失敗しました。") from e
    except SQLAlchemyError as e:
      self.session.rollback()
      raise ValueError("ユーザー情報の登録に失敗しました。") from e
    
  def select_user_for_login(self, email:str) -> None:    
    """ユーザー情報の取得"""
    try: 
      # ユーザー情報の取得
      #＃ パスワードの検証はview側で処理する。
      registered_user = self.session.query(Users).filter(Users.email==email).first()
      self.session.commit()
      
      print("registered_user", registered_user)
      
      return registered_user
    except SQLAlchemyError as e:
      self.session.rollback()
      raise ValueError("ユーザー情報の取得に失敗しました。") from e
      
    
  def close(self):
    self.session.close()
