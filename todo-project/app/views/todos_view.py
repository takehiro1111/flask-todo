"""Todoの処理に関するview.

- メモ一覧画面
  - GET /todos
- メモ詳細画面
  - GET /todos/:id
- 新規作成
  - GET /todos/new
    - フォーム画面の表示
  - POST /todos
- 編集
  - GET /todos/:id/edit
    - 編集画面の表示
  - POST /todos/:id
- 削除
  - POST /todos/:id/delete
  - GET /todos/:id/delete/result
    - 削除結果の画面表示
"""

from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from wtforms import StringField, TextAreaField, SubmitField, validators
from wtforms.validators import DataRequired, InputRequired
from flask_wtf import FlaskForm

from app.models.todos import TodoProcess
from app.models.users import UserProcess
from utils.messages import FLASH_MESSAGES

"""ブループリントの作成"""
todo_bp = Blueprint("todos", __name__, url_prefix="/todos", template_folder="templates")



"""フォームの作成"""
class CreateNewTodos(FlaskForm):
  title = StringField("タイトル", validators=[DataRequired(),validators.Length(min=4, max=25)])
  body = TextAreaField("内容",validators=[InputRequired(), validators.Length(min=4, max=500)])
  submit = SubmitField(label=("登録"))
  
class UpdateTodos(FlaskForm):
  title = StringField("タイトル", validators=[DataRequired(),validators.Length(min=4, max=25)])
  body = TextAreaField("内容",validators=[InputRequired(), validators.Length(min=4, max=500)])
  submit = SubmitField(label=("修正"))
  
class DeleteTodos(FlaskForm):
  submit = SubmitField(label=("削除"))
  
"""初期化"""
todo_process = TodoProcess()
user_process = UserProcess()


"""ルーティングの作成"""
@todo_bp.route("/", methods=["GET", "POST"])
def get_todos():
  """Todoリストの一覧表示"""
  
  form=CreateNewTodos()
  user_id = session.get("user_id")
  user =  user_process.select_user_by_id(user_id)
  
  if request.method == "POST" and form.validate_on_submit():
    title = form.title.data
    body = form.body.data
    
    todo_process.insert_todo_record(title, body, user_id)
    todos = todo_process.select_todo_of_login_user(user_id)
    flash(FLASH_MESSAGES["todos"]["CREATED_SUCCESS"])
    return render_template("todo/todos.html", todos=todos, user=user, current_user_id=user_id)
  elif request.method == "POST" and form.validate_on_submit() is False:
    flash(FLASH_MESSAGES["todos"]["CREATED_ERROR"])
    return render_template("todo/todos_new.html", form=form)

  try:
    todos = todo_process.select_todo_of_login_user(user_id)
    return render_template("todo/todos.html", todos=todos, current_user_id=user_id, user=user)
  except ValueError as e:
    flash(FLASH_MESSAGES["todos"]["FETCH_ERROR"])
    return render_template("todo/todos.html")
  finally:
    todo_process.close()
    user_process.close() 


@todo_bp.route("/new", methods=["GET"])
def create_todo():
  """Todoの新規作成"""
  
  form=CreateNewTodos()
  return render_template("todo/todos_new.html", form=form)
  

@todo_bp.route("/<int:todo_id>", methods=["GET", "POST"])
def detail_todo(todo_id):
  """Todoの詳細"""
  
  update_form=UpdateTodos()
  
  if request.method == "POST" and update_form.validate_on_submit():
    title = update_form.title.data
    body = update_form.body.data
    
    # レコードの更新
    updated_todo = todo_process.update_todo_by_id(title, body, todo_id)
    
    flash(FLASH_MESSAGES["todos"]["UPDATED_SUCCESS"])
    return render_template("todo/todos_detail.html", todo=updated_todo)
  
  todo = todo_process.select_todo_by_id(todo_id)
  
  return render_template("todo/todos_detail.html", todo=todo)

@todo_bp.route("/<int:todo_id>/edit", methods=["GET"])
def edit_todo(todo_id):
  """Todoの編集"""
  
  form=UpdateTodos()
  
  todo = todo_process.select_todo_by_id(todo_id)
  
  return render_template("todo/todos_edit.html", form=form, todo=todo)


@todo_bp.route("/<int:todo_id>/delete", methods=["POST"])
def delete_todo(todo_id: int):
  """削除処理"""
  
  todo_process.delete_todo_by_id(todo_id)
  
  return redirect(url_for("todos.delete_result_todo", todo_id=todo_id))
  
  
@todo_bp.route("/<int:todo_id>/delete/result", methods=["GET"])
def delete_result_todo(todo_id: int):
  """削除処理の結果表示"""
  
  todo = todo_process.select_todo_by_id(todo_id)
  
  return render_template("todo/todos_delete_result.html", todo=todo)
