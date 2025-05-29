from flask import Blueprint, request, render_template, redirect, url_for, flash

"""ブループリントの作成"""
index_bp = Blueprint("index", __name__, template_folder="templates")


"""ルーティングの作成"""
@index_bp.route("/", methods=["GET"])
def index_redirect_to_login():
  """ルートにアクセス来たらログインページへリダイレクト"""
  return redirect(url_for('auth.login'))
