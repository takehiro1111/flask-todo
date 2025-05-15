CREATE DATABASE fk_todos;

CREATE TABLE IF NOT EXISTS users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(30) NOT NULL,
  email VARCHAR(100) NOT NULL,
  password_hash VARCHAR(500) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uk_users_email (email)
);

-- 論理削除に対応するため。
ALTER TABLE users
    ADD deleted_at TIMESTAMP NULL DEFAULT NULL;

-- sha512のハッシュ化に対応するため。
ALTER TABLE users 
    MODIFY password_hash VARCHAR(500);



CREATE TABLE IF NOT EXISTS todos (
  id INT PRIMARY KEY AUTO_INCREMENT,
  title VARCHAR(100) NOT NULL,
  body TEXT,
  user_id INT NOT NULL,
  is_completed TINYINT(1) DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP NULL DEFAULT NULL,
  FOREIGN KEY fk_todos_user_id (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- インデックスを削除するために外部キー制約を外す
ALTER TABLE todos DROP FOREIGN KEY todos_ibfk_1;

-- INDEXのカラムを追加するために先に削除する。
DROP INDEX idx_todos_user_id ON todos;

-- カラムを追加した状態でINDEXを再作成。
CREATE INDEX idx_todos_user_id ON todos (user_id, title, is_completed, deleted_at,  created_at);

-- 外部キー制約を再度作成する。
ALTER TABLE todos ADD CONSTRAINT todos_ibfk_1 FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE;

-- スキーマの確認
SHOW COLUMNS FROM todos;
SHOW CREATE TABLE todos;
