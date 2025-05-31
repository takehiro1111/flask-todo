from datetime import datetime
from zoneinfo import ZoneInfo

from app.models.session import SessionLocal
from app.models.create_tables import Users
from utils.messages import ERROR_MESSAGES

class User:
  def __init__(self):
    self.session = SessionLocal()
    
  def _base_query(self):
    """selectの共通クエリ"""
    return self.session.query(Users).filter(Users.deleted_at == None)
  
  def _base_query_by_user_id(self, id):
    """主キーのidでユーザーをfilterする場合"""
    return self._base_query().filter(Users.id == id)
  
  def _base_query_by_email(self, email):
    """メールアドレスでユーザーをfilterする場合"""
    return self._base_query().filter(Users.email == email)

  # ユーザー情報の追加
  def insert_user(self, name: str, email: str, password_hash: str):
    """ユーザー情報を登録"""
    new_user = Users(name=name, email=email, password_hash=password_hash)
    self.session.add(new_user)
    
    self.session.commit()
    return new_user
    
  def select_user_by_email(self, email:str):    
    """ユーザー情報の取得"""
    return(
      self._base_query_by_email(email).first()
    )
  
  def select_user_by_id(self, user_id:int):    
    """ユーザー情報の取得"""
    return self._base_query_by_user_id(user_id).first()
    
  def update_user_by_id(self, user_id, name, email, password_hash):
    """ユーザー情報の更新"""
    result = self._base_query_by_user_id(user_id).update({
      Users.name: name, Users.email: email, Users.password_hash: password_hash
    }, synchronize_session=False)
    
    if result == 0:
      raise ValueError(ERROR_MESSAGES["user_model"]["USER_ID_NOT_FOUND"].format(user_id))
    
    self.session.commit()
    return result
  
  def reset_password_hash_by_email(self, email, mew_password_hash):
    """ユーザー情報の更新"""
    result = self._base_query_by_email(email).update({
      Users.password_hash: mew_password_hash
    }, synchronize_session=False)
    
    if result == 0:
      raise ValueError(ERROR_MESSAGES["user_model"]["USER_ID_NOT_FOUND"].format(email))
    
    self.session.commit()
    return result
  
  def delete_user_by_id(self, user_id: int):
    """ユーザー情報の論理削除"""
    result = self._base_query_by_user_id(user_id).update({
      Users.deleted_at: datetime.now(ZoneInfo("Asia/Tokyo"))
    }, synchronize_session=False)
    
    if result == 0:
      raise ValueError(ERROR_MESSAGES["user_model"]["USER_ID_NOT_FOUND"].format(user_id))
    
    self.session.commit()
    return result
