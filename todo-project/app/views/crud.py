"""一般的なCRUD操作に関するview."""

from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.users import UserProcess

"""ブループリントの作成"""
crud_bp = Blueprint("app", __name__, template_folder="templates")



"""フォームの作成"""


"""ルーティングの作成"""
@crud_bp.route("/todos", methods=["GET", "POST"])
def todos():

  return render_template("todos.html")
    
