import click
from flask.cli import with_appcontext
from app.models.create_tables import Base, engine

@click.command("create-tables")
@with_appcontext
def create_tables_command():
  """テーブル作成のコマンド"""
  Base.metadata.create_all(engine)
  click.echo("テーブルを作成しました。")
  

@click.command("drop-tables")
@with_appcontext
def drop_tables_command():
  """テーブル削除のコマンド"""
  if click.confirm("本当に削除しますか？", default=False):
    Base.metadata.drop_all(engine)
    click.echo('テーブルを削除しました')
    return
  else:
    click.echo("削除をキャンセルしました。")
