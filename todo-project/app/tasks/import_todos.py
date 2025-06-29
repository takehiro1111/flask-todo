import io
import os
import csv
from celery import Celery

from app import create_app

celery_app = Celery(
    'csv_importer',
    broker=os.environ.get("REDIS_URL"),
    backend=os.environ.get("REDIS_URL")
)

@celery_app.task
def process_csv_import(file_content, user_id):
    """
    非同期でCSVをパースし、DBに登録するタスク
    """
    from flask import Flask
    flask_app = create_app(Flask(__name__))
    try:
        with flask_app.app_context():
            with flask_app.test_request_context('/'):
                from app.models.session import db_session

                stream = io.StringIO(file_content)
                reader = csv.DictReader(stream)

                errors = []
                todos_to_insert = []

                for index, row in enumerate(reader, start=2):
                    if not row.get("title"):
                        errors.append(index)
                        continue

                    todos_to_insert.append({
                        "title": row.get("title"),
                        "description": row.get("description", ""),
                        "user_id": user_id
                    })

                if errors:
                    print(f"CSV処理エラー: タイトルが空の行があります。行番号: {errors}")
                    return {"success": False, "message": f"CSVでタイトルが空のデータがあります。", "errors": errors}

                with db_session() as (current_todo_model, _):
                    imported_todos = current_todo_model.bulk_insert_todos(todos_to_insert)
                    new_tasks_data = [
                        {"id": todo.id, "title": todo.title} for todo in imported_todos
                    ]
                    return {
                        "success": True,
                        "message": f"タスクをインポートしました。",
                        "new_tasks": new_tasks_data,
                    }

    except Exception as e:
        print(f"CSV処理中にエラーが発生しました: {e}")
        raise
