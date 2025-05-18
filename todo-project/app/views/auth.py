"""認証に関するview."""

from flask import Blueprint, request, render_template, redirect, url_for, session
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.users import UserProcess


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
  form=AuthRegister()
  
  if request.method == "POST" and form.validate_on_submit():
    username = form.username.data
    email = form.email.data
    password_hash = generate_password_hash(form.password.data)
    print(username, email, password_hash)

    user_process = UserProcess()
    
    try:
      # DBにinsertの処理を追加する。
      user_process.insert_user(username, email, password_hash)
      return  redirect(url_for("auth.login"))
    
    except ValueError as e:
      return render_template("auth/register.html", form=form, error=str(e))
      
  return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
  form=AuthLogin()
  
  if request.method == "POST" and form.validate_on_submit():
    email = form.email.data
    password = form.password.data
    
    user_process = UserProcess()
    
    try:
      registered_user = user_process.select_user_for_login(email)
    
      if registered_user and check_password_hash(registered_user.password_hash, password):
        # セッション情報の管理
        
        print("ログイン成功",registered_user.name)
        return redirect(url_for("todos"))
      
    except ValueError as e:
      return render_template("auth/login.html", form=form, error=str(e))
    
    finally:
      user_process.close()
      
    return render_template("auth/login.html", form=form, error="メールアドレスまたはパスワードが間違っています。")
      
  return render_template("auth/login.html", form=form)
