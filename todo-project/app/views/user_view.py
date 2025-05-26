"""ユーザー詳細,編集の処理に関するview.

- ユーザー詳細
  - GET /user/:id
- ユーザー編集
  - GET /user/:id/edit
  - POST /user/:id
- ユーザー削除
  - POST /user/:id/delete
"""

from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from wtforms import StringField, TextAreaField, SubmitField, validators, PasswordField
from wtforms.validators import DataRequired, InputRequired
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import SQLAlchemyError,IntegrityError


from utils.messages import FLASH_MESSAGES
from app.models.session import db_session
from utils.logger import logger

"""ブループリントの作成"""
user_bp = Blueprint("user", __name__, url_prefix="/user", template_folder="templates")

"""フォームの作成"""
class UpdateUserInfo(FlaskForm):
  name = StringField("名前", validators=[DataRequired(),validators.Length(min=4, max=25)])
  email = TextAreaField("Eメールアドレス",validators=[InputRequired(), validators.Length(min=4, max=500)])
  password = PasswordField("パスワード", validators=[DataRequired(),validators.Length(min=4, max=30)])
  submit = SubmitField(label=("登録"))


"""ルーティングの作成"""
@user_bp.route("/<int:user_id>", methods=["GET", "POST"])
def detail_user(user_id):
  """ユーザー情報の詳細"""
  try:
    with db_session() as (current_todo_model, current_user_model):
      form = UpdateUserInfo()

      if request.method == "POST" and form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password_hash = generate_password_hash(form.password.data)
        
        current_user_model.update_user_by_id(user_id, name, email, password_hash)
        
        flash(FLASH_MESSAGES["users"]["UPDATED_SUCCESS"])
        return redirect(url_for('user.detail_user', user_id=user_id))
      
      user = current_user_model.select_user_by_id(user_id)
      
      return render_template("user/user_detail.html", user=user)
  
  except ValueError as e:
    flash(FLASH_MESSAGES["users"]["INFO_FETCH_ERROR"])
    logger.warning(f"ユーザー情報の取得エラー(ValueError): {e}")
    return redirect(url_for('todos.get_todos'))
      
  except (SQLAlchemyError, IntegrityError) as e:
    flash(FLASH_MESSAGES["user_model"]["FETCH_FAILED"])
    return redirect(url_for('todos.get_todos'))


@user_bp.route("/<int:user_id>/edit", methods=["GET"])
def edit_user(user_id):
  """ユーザー情報の編集"""
  try:
    with db_session() as (current_todo_model, current_user_model):
      form=UpdateUserInfo()
      user = current_user_model.select_user_by_id(user_id)
      
      return render_template("user/user_edit.html", form=form, user=user)
  
  except ValueError as e:
    flash(FLASH_MESSAGES["users"]["INFO_FETCH_ERROR"])
    return redirect(url_for('user.detail_user'))
      
  except (SQLAlchemyError, IntegrityError) as e:
    flash(FLASH_MESSAGES["user_model"]["FETCH_FAILED"])
    return redirect(url_for('user.detail_user'))

@user_bp.route("/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):  
  """ユーザー情報を論理削除"""
  try:
    with db_session() as (current_todo_model, current_user_model):
      deleted_user = current_user_model.delete_user_by_id(user_id)
      if deleted_user:
        return redirect(url_for("auth.login"))
      
      flash(FLASH_MESSAGES["users"]["DELETE_FAILED"])
      return redirect(url_for("user.detail_user", user_id=user_id))
  
  except ValueError as e:
    flash(FLASH_MESSAGES["users"]["INFO_FETCH_ERROR"])
    return redirect(url_for('user.detail_user'))
      
  except (SQLAlchemyError, IntegrityError) as e:
    flash(FLASH_MESSAGES["user_model"]["FETCH_FAILED"])
    return redirect(url_for('user.detail_user'))
