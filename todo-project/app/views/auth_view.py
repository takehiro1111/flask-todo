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

from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError,IntegrityError

from utils.messages import FLASH_MESSAGES
from app.models.session import db_session

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
  submit = SubmitField("ログイン")


"""ルーティングの作成"""
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
  """ユーザー登録"""
  try:
    with db_session() as (current_todo_model, current_user_model):
      form=AuthRegister()
      
      if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password_hash = generate_password_hash(form.password.data)
        
        
        current_user_model.insert_user(username, email, password_hash)
        flash(FLASH_MESSAGES["authentication"]["USER_REGISTERED_SUCCESS"])
        return  redirect(url_for("auth.login"))
    
      return render_template("auth/register.html", form=form)
      
  except ValueError as e:
    flash(FLASH_MESSAGES["authentication"]["USER_REGISTERED_ERROR"])
    print(f"エラー:{e}")
    return redirect(url_for("auth.login"))
        
  except (SQLAlchemyError, IntegrityError) as e:
    flash(FLASH_MESSAGES["todos"]["FETCH_FAILED"])
    print(f"エラー:{e}")
    return redirect(url_for("auth.login"))
  
  except Exception as e:
    print(f"Exception:{e}")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
  """ログイン処理"""
  try: 
    with db_session() as (current_todo_model, current_user_model):
      form=AuthLogin()
      
      if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        registered_user = current_user_model.select_user_for_login(email)
        
        if registered_user and check_password_hash(registered_user.password_hash, password):
          session['user_id'] = registered_user.id 
          session['user_name'] = registered_user.name 

          return redirect(url_for("todos.get_todos"))
        else:
          flash(FLASH_MESSAGES["authentication"]["USER_LOGIN_ERROR"])
          return render_template("auth/login.html", form=form)
          
      return render_template("auth/login.html", form=form)
    
  except ValueError as e:
    flash(FLASH_MESSAGES["authentication"]["USER_LOGIN_EXCEPTION"])
    return redirect(url_for("auth.login"))
  
  except (SQLAlchemyError, IntegrityError) as e:
    flash(FLASH_MESSAGES["todos"]["FETCH_FAILED"])
    return redirect(url_for("auth.login"))


@auth_bp.route("/logout", methods=["GET"])
def logout():
  """ログアウト処理"""
  session.clear()
  return render_template("auth/logout.html")
