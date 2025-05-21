"""一般的なCRUD操作に関するview."""

from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from wtforms import StringField, TextAreaField, SubmitField, ValidationError, validators
from wtforms.validators import DataRequired, Email, InputRequired, NumberRange
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.todos import TodoProcess
from app.models.users import UserProcess

"""ブループリントの作成"""
crud_bp = Blueprint("app", __name__, template_folder="templates")



"""フォームの作成"""
class CreateNewTodos(FlaskForm):
  title = StringField("タイトル", validators=[DataRequired(),validators.Length(min=4, max=25)])
  body = TextAreaField("内容",validators=[InputRequired(), validators.Length(min=4, max=500)])
  submit = SubmitField(label=("登録"))
  

"""ルーティングの作成"""
@crud_bp.route("/todos", methods=["GET", "POST"])
def get_todos():
  form=CreateNewTodos()
  todo_process = TodoProcess()
  user_id = session.get("user_id")
  
  if request.method == "POST" and form.validate_on_submit():
    title = form.title.data
    body = form.body.data
    
    todo_process.insert_todo_record(title, body, user_id)
    todos = todo_process.select_todo_of_login_user(user_id)
    print("todos:", todos)
    flash("TODOの作成が完了しました。")
    return render_template("todos.html", todos=todos)
  elif request.method == "POST" and form.validate_on_submit() is False:
    flash("TODOの作成に失敗しました。再度入力してください。")
    return render_template("todos_new.html", form=form)
  # GETリクエストの場合
  # ログインしているユーザーのIDを取得
  
  try:
    todos = todo_process.select_todo_of_login_user(user_id)
    return render_template("todos.html", todos=todos)
  except ValueError as e:
    flash("Todo情報の取得に失敗しました。")
    return render_template("todos.html")


@crud_bp.route("/todos/new", methods=["GET"])
def create_todo():
  form=CreateNewTodos()
  return render_template("todos_new.html", form=form)
  
