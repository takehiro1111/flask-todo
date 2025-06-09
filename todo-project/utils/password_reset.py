from flask import url_for, current_app
from itsdangerous import TimedSerializer, SignatureExpired, BadSignature
from flask_mail import Message

from app import mail
from utils.logger import logger
from utils.messages import MAIL_TEMPLATE

def generate_password_reset_token(email):
  """パスワードリセットトークンの生成"""
  serializer = TimedSerializer(current_app.config['SECRET_KEY'])
  return serializer.dumps(email, salt=current_app.config['PASSWORD_RESET_SALT'])

def verify_password_reset_token(token, expiration=3600):
  """パスワードリセットトークンの検証"""
  serializer = TimedSerializer(current_app.config['SECRET_KEY'])
  try:
    email = serializer.loads(token, salt=current_app.config['PASSWORD_RESET_SALT'], max_age=expiration)
  except (SignatureExpired, BadSignature) as e:
    return None
  except Exception as e:
    logger.error(f"Failed to send password reset {e}")
    return False
  return email

def send_password_reset_email(email_address, token):
    """パスワードリセット用のメールを送信する"""
    try:
        reset_url = url_for('auth.reset_password', token=token, _external=True)
        msg = Message(
            subject="パスワードリセットのご案内",
            sender=current_app.config['MAIL_DEFAULT_SENDER'], 
            recipients=[email_address]
        )
        # メール本文をテンプレートからレンダリングすることも可能
        msg.body =  MAIL_TEMPLATE["password_reset"].format(reset_url=reset_url)

        mail.send(msg)
        logger.info(f"Password reset email sent to {email_address}")
        return True
    except Exception as e:
        logger.error(f"パスワードリセット用のメール送信に失敗しました:{email_address}: {e}")
        return False
