from itsdangerous import TimedSerializer
import secrets

def generate_password_reset_token(email, expiration=3600):
  """パスワードリセットトークンの生成"""
  serializer = TimedSerializer("secret_key")
  return serializer.dumps(email, salt=secrets.token_hex(16))

print(generate_password_reset_token("test@gmail.com"))
