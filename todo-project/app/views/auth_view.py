"""認証に関するview.

- ユーザー登録
  - GET /auth/register
  - POST /auth/register

- ログイン機能
  - GET /auth/login
  - POST /auth/login

- ログアウト機能
  - GET /auth/logout
"""

from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse
from sqlalchemy.exc import SQLAlchemyError,IntegrityError

from utils.messages import FLASH_MESSAGES, ERROR_MESSAGES, FLASH_CATEGORIES
from app.models.session import db_session
from utils.logger import logger
from utils.password_reset import (
  generate_password_reset_token, 
  verify_password_reset_token, 
  send_password_reset_email
) 

"""ブループリントの作成"""
auth_bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="templates")


"""フォームの作成"""
class AuthRegister(FlaskForm):
  username = StringField("ユーザー名", validators=[DataRequired()])
  email = StringField("Eメールアドレス", validators=[DataRequired(), Email()])
  password = PasswordField("パスワード", validators=[DataRequired()])
  submit = SubmitField("登録")
  
class AuthLogin(FlaskForm):
  email = StringField("Eメールアドレス", validators=[DataRequired(), Email()])
  password = PasswordField("パスワード", validators=[DataRequired()])
  remember = BooleanField("ログイン情報を保存する")
  submit = SubmitField("ログイン")
  
class InputEmail(FlaskForm):
  email = StringField("Eメールアドレス", validators=[DataRequired(), Email()])
  submit = SubmitField("送信")
  
class ResetPassword(FlaskForm):
  new_password = PasswordField("新しいパスワード", validators=[DataRequired()])
  new_password_match = PasswordField("確認用", [
        DataRequired(),
        EqualTo("new_password", message="パスワードの入力が一致している必要があります。")
    ])
  submit = SubmitField("リセット")


"""ルーティングの作成"""
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
  """ユーザー登録"""
  
  with db_session() as (_, current_user_model):
    form=AuthRegister()
    
    if request.method == "POST" and form.validate_on_submit():
      username = form.username.data
      email = form.email.data
      password_hash = generate_password_hash(form.password.data)
      
      try:
        current_user_model.insert_user(username, email, password_hash)
      except ValueError as e:
        flash(FLASH_MESSAGES["authentication"]["USER_REGISTERED_ERROR"])
        logger.error(f"{ERROR_MESSAGES["user_model"]["INVALID_VALUE"]}:{e}")
        return redirect(url_for("auth.login"))
      except (SQLAlchemyError, IntegrityError) as e:
        flash(FLASH_MESSAGES["authentication"]["USER_REGISTERED_ERROR"])
        logger.error(f"{ERROR_MESSAGES["user_model"]["REGISTRATION_FAILED"]}:{e}")
        return redirect(url_for("auth.login"))
      
      flash(FLASH_MESSAGES["authentication"]["USER_REGISTERED_SUCCESS"])
      return  redirect(url_for("auth.login"))
  
    return render_template("auth/register.html", form=form)
      
  
  
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
  """ログイン処理"""
  with db_session() as (_, current_user_model):
    form=AuthLogin()
    
    if request.method == "POST" and form.validate_on_submit():
      email = form.email.data
      password = form.password.data
      
      try:
        registered_user = current_user_model.select_user_by_email(email)
      except (SQLAlchemyError, IntegrityError) as e:
        flash(FLASH_MESSAGES["authentication"]["USER_LOGIN_ERROR"])
        logger.error(f"{ERROR_MESSAGES["user_model"]["FETCH_FAILED"]}:{e}")
        return redirect(url_for("auth.login"))
      except ValueError as e:
        flash(FLASH_MESSAGES["authentication"]["USER_LOGIN_EXCEPTION"])
        logger.error(f"{ERROR_MESSAGES["user_model"]["INVALID_VALUE"]}:{e}")
        return redirect(url_for("auth.login"))
      
      if registered_user and check_password_hash(registered_user.password_hash, password):
        # Flask-Loginの機能を使ってユーザーをログイン状態にする
        login_user(registered_user, remember=form.remember.data)
        
        # リクエストパラメータから次のページを取得（ログイン要求元ページなど）
        next_page = request.args.get("next")
        if not next_page or urlparse(next_page).netloc != "":
            next_page = url_for("todos.get_todos")

        return redirect(url_for("todos.get_todos"))
      else:
        flash(FLASH_MESSAGES["authentication"]["USER_LOGIN_ERROR"])
        return render_template("auth/login.html", form=form)
        
    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout", methods=["GET"])
@login_required
def logout():
  """ログアウト処理"""
  logout_user()
  flash(FLASH_MESSAGES["authentication"]["USER_LOGOUT_SUCCESS"])
  return redirect(url_for("auth.login"))

##########################################################################
# パスワードの再設定
##########################################################################
@auth_bp.route("/input_email", methods=["GET", "POST"])
def input_email():
  """パスワード再設定するためのメールアドレス入力画面"""
  with db_session() as (_, current_user_model):
    form=InputEmail()
    
    if request.method == "POST":
      if form.validate_on_submit():
        user_email = form.email.data
        matched_user = current_user_model.select_user_by_email(user_email)
        
      if matched_user:
        token = generate_password_reset_token(user_email)
        email_sent_successfully = send_password_reset_email(user_email, token)
        
        if email_sent_successfully:
          flash(FLASH_MESSAGES["authentication"]["PASSWORD_RESET_EMAIL_SENT_SUCCESS"], FLASH_CATEGORIES["SUCCESS"])
        else:
          flash(FLASH_MESSAGES["authentication"]["PASSWORD_RESET_EMAIL_SENT_FAILURE"], FLASH_CATEGORIES["FAILURE"])
      else:
        flash(FLASH_MESSAGES["authentication"]["PASSWORD_RESET_EMAIL_SENT_SUCCESS"], FLASH_CATEGORIES["SUCCESS"])
        
      return redirect(url_for("auth.login"))
        
        
    return render_template("auth/input_email.html", form=form)

@auth_bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
  """パスワード再設定の画面"""
  email_from_token = verify_password_reset_token(token)
  if email_from_token is None:
    flash(FLASH_MESSAGES["authentication"]["PASSWORD_RESET_INVALID_TOKEN"], FLASH_CATEGORIES["WARNING"])
    return redirect(url_for("auth.input_email"))
  
  form=ResetPassword()
  if request.method == "POST" and form.validate_on_submit():
    with db_session() as (_, current_user_model):
      new_hashed_password = generate_password_hash(form.new_password.data)
      
      result = current_user_model.reset_password_hash_by_email(email_from_token, new_hashed_password)
      
      if result:
        flash(FLASH_MESSAGES["authentication"]["PASSWORD_RESET_SUCCESS"], FLASH_CATEGORIES["SUCCESS"])
        return redirect(url_for("auth.login"))
        
      flash(FLASH_MESSAGES["authentication"]["PASSWORD_RESET_FAILURE"], FLASH_CATEGORIES["FAILURE"])
      return redirect(url_for("auth.input_email"))
      
  
  return render_template("auth/reset_password.html", form=form, token=token)
