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

import csv
import io

from flask import Blueprint, request, render_template, redirect, url_for, flash, Response, jsonify
from flask_login import login_required, current_user
from wtforms import StringField, TextAreaField, SubmitField, validators
from wtforms.validators import DataRequired, InputRequired
from flask_wtf import FlaskForm
from sqlalchemy.exc import SQLAlchemyError,IntegrityError

from app.models.session import db_session
from utils.messages import FLASH_MESSAGES, ERROR_MESSAGES
from app.tasks.import_todos import process_csv_import

"""ブループリントの作成"""
todo_bp = Blueprint("todos", __name__, url_prefix="/todos", template_folder="templates")

"""フォームの作成"""
class CreateNewTodos(FlaskForm):
  title = StringField("タイトル", validators=[InputRequired(),validators.Length(min=4, max=25)])
  body = TextAreaField("内容",validators=[DataRequired(), validators.Length(min=4, max=500)])
  submit = SubmitField(label=("登録"))
  
class UpdateTodos(FlaskForm):
  title = StringField("タイトル", validators=[InputRequired(),validators.Length(min=4, max=25)])
  body = TextAreaField("内容",validators=[DataRequired(), validators.Length(min=4, max=500)])
  submit = SubmitField(label=("修正"))
  
class DeleteTodos(FlaskForm):
  submit = SubmitField(label=("削除"))


"""ルーティングの作成"""
@todo_bp.route("/", methods=["GET", "POST"])
@login_required
def get_todos():
  """Todoリストの一覧表示"""
  try:
    with db_session() as (current_todo_model, current_user_model):
      form=CreateNewTodos()
      user_id = current_user.id
      user =  current_user_model.select_user_by_id(user_id)
      
      if request.method == "POST" and form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        
        current_todo_model.insert_todo(title, body, user_id)
        todos = current_todo_model.find_by_user(user_id)
        flash(FLASH_MESSAGES["todos"]["CREATED_SUCCESS"])
        return render_template("todo/todos.html", todos=todos, user=user, current_user_id=user_id)
      elif request.method == "POST" and form.validate_on_submit() is False:
        flash(FLASH_MESSAGES["todos"]["CREATED_ERROR"])
        return render_template("todo/todos_new.html", form=form)

      
      todos = current_todo_model.find_by_user(user_id)
      return render_template("todo/todos.html", todos=todos, current_user_id=user_id, user=user)

  # エラー時にログイン画面へリダイレクトさせて戻す。
  except ValueError as e:
    flash(FLASH_MESSAGES["todos"]["FETCH_ERROR"])
    return render_template("auth/login.html", form=form)
      
  except (SQLAlchemyError, IntegrityError) as e:
    flash(FLASH_MESSAGES["todos"]["FETCH_FAILED"])
    return render_template("auth/login.html", form=form)

@todo_bp.route("/new", methods=["GET"])
@login_required
def create_todo():
  """Todoの新規作成"""
  form=CreateNewTodos()
  return render_template("todo/todos_new.html", form=form)

def check_todo_owner(todo_id, user_id):
    """ユーザーがTODOの所有者かどうかを確認"""
    with db_session() as (current_todo_model, _):
        todo = current_todo_model.select_todo_by_id(todo_id)
        if todo is None:
            return False
        return todo.user_id == user_id
  

@todo_bp.route("/<int:todo_id>", methods=["GET", "POST"])
@login_required
def detail_todo(todo_id):
  """Todoの詳細"""
  try: 
    if not check_todo_owner(todo_id, current_user.id):
      flash("このTODOにアクセスする権限がありません", "danger")
      return redirect(url_for("todos.get_todos"))
          
    with db_session() as (current_todo_model, _):
      update_form=UpdateTodos()
      
      if request.method == "POST" and update_form.validate_on_submit():
        title = update_form.title.data
        body = update_form.body.data
        
        # レコードの更新
        current_todo_model.update_todo_by_id(title, body, todo_id)
        
        updated_todo = current_todo_model.select_todo_by_id(todo_id)
        
        flash(FLASH_MESSAGES["todos"]["UPDATED_SUCCESS"])
        return render_template("todo/todos_detail.html", todo=updated_todo)
      
      
      todo = current_todo_model.select_todo_by_id(todo_id)
      return render_template("todo/todos_detail.html", todo=todo)
    
  except ValueError as e:
    flash(FLASH_MESSAGES["todos"]["FETCH_ERROR"])
    return redirect(url_for("todos.get_todos"))
      
  except (SQLAlchemyError, IntegrityError) as e:
    flash(FLASH_MESSAGES["todos"]["FETCH_FAILED"])
    return redirect(url_for("todos.get_todos"))

@todo_bp.route("/<int:todo_id>/edit", methods=["GET"])
@login_required
def edit_todo(todo_id):
  """Todoの編集"""
  try:
    with db_session() as (current_todo_model, current_user_model):
      form=UpdateTodos()
      todo = current_todo_model.select_todo_by_id(todo_id)
      
      return render_template("todo/todos_edit.html", form=form, todo=todo)

  except ValueError as e:
    flash(FLASH_MESSAGES["todos"]["FETCH_ERROR"])
    return redirect(url_for("todos.detail_todo", todo_id=todo_id))
      
  except (SQLAlchemyError, IntegrityError) as e:
    flash(FLASH_MESSAGES["todos"]["FETCH_FAILED"])
    return redirect(url_for("todos.detail_todo", todo_id=todo_id))


@todo_bp.route("/<int:todo_id>/delete", methods=["POST"])
@login_required
def delete_todo(todo_id: int):
  """削除処理"""
  try:
    with db_session() as (current_todo_model, _):
      current_todo_model.soft_delete_todo_by_id(todo_id)
      
      return redirect(url_for("todos.delete_result_todo", todo_id=todo_id))
    
  except ValueError as e:
    flash(FLASH_MESSAGES["todos"]["FETCH_ERROR"])
    return redirect(url_for("todos.detail_todo", todo_id=todo_id))
      
  except (SQLAlchemyError, IntegrityError) as e:
    flash(FLASH_MESSAGES["todos"]["FETCH_FAILED"])
    return redirect(url_for("todos.detail_todo", todo_id=todo_id))
  
  
@todo_bp.route("/<int:todo_id>/delete/result", methods=["GET"])
@login_required
def delete_result_todo(todo_id: int):
  """削除処理の結果表示"""
  try:
    with db_session() as (current_todo_model, _):
      todo = current_todo_model.select_todo_by_id(todo_id)
    
      return render_template("todo/todos_delete_result.html", todo=todo)
  
  except ValueError as e:
    flash(FLASH_MESSAGES["todos"]["FETCH_ERROR"])
    return redirect(url_for("todos.detail_todo", todo_id=todo_id))
      
  except (SQLAlchemyError, IntegrityError) as e:
    flash(FLASH_MESSAGES["todos"]["FETCH_FAILED"])
    return redirect(url_for("todos.detail_todo", todo_id=todo_id))


@todo_bp.route("/export_csv", methods=["GET"])
@login_required
def export_csv():
  """DBからtodoデータを取得し、CSVででエクスポートを行う"""
  try: 
    with db_session() as (current_todo_model, _):
      user_id = current_user.id
      todos = current_todo_model.find_by_user(user_id)
      
      string_io = io.StringIO()
      
      fieldnames = ["id", "title", "description", "status"]
      
      with string_io as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()      
        for todo in todos:
          writer.writerow({
              fieldnames[0]: todo.id,
              fieldnames[1]: todo.title,
              fieldnames[2]: todo.body,
              fieldnames[3]: "完了" if todo.is_completed == 1 else "未完了"
          })

        csv_data = string_io.getvalue()
        return Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=todos.csv"}
        )
    
  except ValueError as e:
    flash(FLASH_MESSAGES["todos"]["FETCH_ERROR"])
    return redirect(url_for("todos.get_todos"))
    
  
@todo_bp.route("/import_csv", methods=["POST"])
@login_required
def import_csv():
    """csvライブラリでCSVをパースしてDBに登録してTodoとして表示する"""
    try:
      if "file" not in request.files:
          return jsonify(success=False, message=ERROR_MESSAGES["csv"]["NOT_UPLOAD_CSV"]), 400
          
      file = request.files["file"]
      
      if file.filename == "":
          return jsonify(success=False, message=ERROR_MESSAGES["csv"]["FILE_NOT_SELECTED"]), 400
          
      if not file.filename.endswith(".csv"):
          return jsonify(success=False, message=ERROR_MESSAGES["csv"]["NOT_A_CSV_FILE"]), 400
        
      
      file_content = file.stream.read().decode("utf-8")
        
      task = process_csv_import.delay(file_content, current_user.id)
      
      response_data = {
        "success": True,
        "message": "CSVファイルのインポート処理を開始しました。完了までしばらくお待ちください。",
        "task_id": task.id
      }
      
      return jsonify(response_data), 202
        

    except Exception as e:
        return jsonify(success=False, message=f"{ERROR_MESSAGES["csv"]["PROCESSING_ERROR"]} {e}"), 500


@todo_bp.route("/import_status/<task_id>")
@login_required
def import_status(task_id):
    from app.tasks.import_todos import process_csv_import
    result = process_csv_import.AsyncResult(task_id)
    if result.state == "PENDING":
        return jsonify(status="processing")
    elif result.state == "SUCCESS":
        return jsonify(status="done", result=result.result)
    elif result.state == "FAILURE":
        return jsonify(status="error", message=str(result.info))
    else:
        return jsonify(status=result.state)
