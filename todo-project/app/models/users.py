from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.models.session import Session
from app.models.create_tables import Users
from utils.messages import ERROR_MESSAGES

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
      raise ValueError(ERROR_MESSAGES["user_model"]["REGISTRATION_FAILED"]) from e
    except SQLAlchemyError as e:
      self.session.rollback()
      raise ValueError("ユーザー情報の登録に失敗しました。") from e
    
  def select_user_for_login(self, email:str):    
    """ユーザー情報の取得"""
    try: 
      registered_user = self.session.query(Users).filter(Users.email==email).first()
      self.session.commit()
      
      return registered_user
    except SQLAlchemyError as e:
      self.session.rollback()
      raise ValueError(ERROR_MESSAGES["user_model"]["FETCH_FAILED"]) from e
  
  def select_user_by_id(self, user_id:int):    
    """ユーザー情報の取得"""
    try: 
      # ユーザー情報の取得
      #＃ パスワードの検証はview側で処理する。
      user = self.session.query(Users).filter(Users.id==user_id).first()
      self.session.commit()
      
      return user
    except SQLAlchemyError as e:
      self.session.rollback()
      raise ValueError(ERROR_MESSAGES["user_model"]["FETCH_BY_ID_FAILED"]) from e
    
  def update_user_by_id(self, user_id, name, email, password_hash):
    """ユーザー情報の更新"""
    try:
      updated_user = self.session.query(Users).filter(Users.id==user_id).first()
      updated_user.name = name
      updated_user.email = email
      updated_user.password_hash = password_hash
      
      self.session.commit()
      
      return updated_user
      
    except SQLAlchemyError as e:
      self.session.rollback()
      raise ValueError(ERROR_MESSAGES["user_model"]["UPDATE_FAILED"]) from e
  
  def delete_user_by_id(self, user_id: int):
    """ユーザー情報の削除"""
    try:      
      # 論理削除
      users_to_delete = self.session.query(Users).filter(Users.id == user_id, Users.deleted_at == None).first()
      
      if users_to_delete:
        users_to_delete.deleted_at = datetime.now(ZoneInfo("Asia/Tokyo"))
        self.session.commit()
      
      return users_to_delete
      
    except SQLAlchemyError as e:
      self.session.rollback()
      raise ValueError(ERROR_MESSAGES["user_model"]["DELETE_FAILED"].format("user_id"))
      
    
  def close(self):
    self.session.close()
