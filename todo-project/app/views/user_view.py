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
from wtforms import StringField, TextAreaField, SubmitField, ValidationError, validators, PasswordField
from wtforms.validators import DataRequired, Email, InputRequired, NumberRange
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.users import UserProcess
from utils.messages import FLASH_MESSAGES

"""ブループリントの作成"""
user_bp = Blueprint("user", __name__, url_prefix="/user", template_folder="templates")

"""フォームの作成"""
class UpdateUserInfo(FlaskForm):
  name = StringField("名前", validators=[DataRequired(),validators.Length(min=4, max=25)])
  email = TextAreaField("Eメールアドレス",validators=[InputRequired(), validators.Length(min=4, max=500)])
  password = PasswordField("パスワード", validators=[DataRequired(),validators.Length(min=4, max=30)])
  submit = SubmitField(label=("登録"))

"""初期化"""
user_process = UserProcess()


@user_bp.route("/<int:user_id>", methods=["GET", "POST"])
def detail_user(user_id):
  """ユーザー情報の詳細"""
  
  form = UpdateUserInfo()
  
  if request.method == "POST" and form.validate_on_submit():
    name = form.name.data
    email = form.email.data
    password_hash = generate_password_hash(form.password.data)
    
    user_process.update_user_by_id(user_id, name, email, password_hash)
    
    flash(FLASH_MESSAGES["user_profile"]["UPDATED_SUCCESS"])
    return redirect(url_for('user.detail_user', user_id=user_id))
  
  user = user_process.select_user_by_id(user_id)
  
  return render_template("user/user_detail.html", user=user)


@user_bp.route("/<int:user_id>/edit", methods=["GET"])
def edit_user(user_id):
  """ユーザー情報の編集"""
  
  form=UpdateUserInfo()
  
  user = user_process.select_user_by_id(user_id)
  
  return render_template("user/user_edit.html", form=form, user=user)

@user_bp.route("/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):  
  """ユーザー情報を論理削除"""
  
  deleted_user = user_process.delete_user_by_id(user_id)
  if deleted_user:
    return redirect(url_for("auth.login"))
  
  flash(FLASH_MESSAGES["user_profile"]["DELETE_FAILED"])
  return redirect(url_for("user.detail_user", user_id=user_id))
