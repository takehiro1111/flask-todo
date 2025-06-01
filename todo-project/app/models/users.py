from app.models.session import SessionLocal
from app.models.create_tables import Users
from utils.messages import ERROR_MESSAGES

class User:
  def __init__(self):
    self.session = SessionLocal()
    
  def _base_query_by_user_id(self, id):
    """主キーのidでユーザーをfilterする場合"""
    return Users.active_query(self.session).filter(Users.id == id)
  
  def _base_query_by_email(self, email):
    """メールアドレスでユーザーをfilterする場合"""
    return Users.active_query(self.session).filter(Users.email == email)

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
    user_to_update_by_id = self._base_query_by_user_id(user_id).first()
    
    if not user_to_update_by_id:
      raise ValueError(ERROR_MESSAGES["user_model"]["USER_ID_NOT_FOUND"].format(user_id))
    
    user_to_update_by_id.name = name
    user_to_update_by_id.email = email
    user_to_update_by_id.password_hash = password_hash
    
    self.session.commit()
    return user_to_update_by_id
  
  def reset_password_hash_by_email(self, email, mew_password_hash):
    """ユーザー情報の更新"""
    user_to_update_by_email = self._base_query_by_email(email).first()
    
    if not user_to_update_by_email:
      raise ValueError(ERROR_MESSAGES["user_model"]["USER_ID_NOT_FOUND"].format(email))
    
    user_to_update_by_email.password_hash = mew_password_hash
    self.session.commit()
    
    return user_to_update_by_email
  
  def soft_delete_user_by_id(self, user_id: int):
    """ユーザー情報の論理削除"""
    user_to_soft_delete = self._base_query_by_user_id(user_id).first()
    
    if not user_to_soft_delete:
      raise ValueError(ERROR_MESSAGES["user_model"]["USER_ID_NOT_FOUND"].format(user_id))
    
    user_to_soft_delete.soft_delete()
    self.session.commit()
    
    return user_to_soft_delete
