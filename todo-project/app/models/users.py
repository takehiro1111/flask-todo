from datetime import datetime
from zoneinfo import ZoneInfo

from app.models.session import Session
from app.models.create_tables import Users
from utils.messages import ERROR_MESSAGES

class User:
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
    except Exception as e:
      print(f"Exception:{e}")
    
  def select_user_for_login(self, email:str):    
    """ユーザー情報の取得"""
    return(
      self.session.query(Users).filter(Users.email==email).first()
    )
  
  def select_user_by_id(self, user_id:int):    
    """ユーザー情報の取得"""
    return(
      self.session.query(Users).filter(Users.id==user_id).first()
    )
    
  def update_user_by_id(self, user_id, name, email, password_hash):
    """ユーザー情報の更新"""
    result = self.session.query(Users).filter(Users.id==user_id).update({
      Users.name: name, Users.email: email, Users.password_hash: password_hash
    }, synchronize_session=False)
    
    if result == 0:
      raise ValueError(ERROR_MESSAGES["user_model"]["USER_ID_NOT_FOUND"].format(user_id))
    
    self.session.commit()
    return result
  
  def delete_user_by_id(self, user_id: int):
    """ユーザー情報の論理削除"""
    result = self.session.query(Users).filter(Users.id == user_id, Users.deleted_at == None).delete({
      Users.deleted_at: datetime.now(ZoneInfo("Asia/Tokyo"))
    }, synchronize_session=False)
    
    if result == 0:
      raise ValueError(ERROR_MESSAGES["user_model"]["USER_ID_NOT_FOUND"].format(user_id))
    
    self.session.commit()
    return result
