# Flask
### 1.[インストール](https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/installation.html#install-flask)
```bash
pipenv install Flask
```

## docker composeによるMySQL,mailhogの利用
```zsh
# compose.yamlのカレントへ移動
cd docker/db

# 起動
docker compose up -d

# MySQLの中へログイン
# PWは、./docker/.envへ記載
docker compose exec mysql mysql -u root -p

# 停止
docker compose stop


# 削除
docker compose down
```

## mailhogのブラウザアクセス
```md
- mailhog
  - http://localhost:8025/#

- ログイン画面
  - http://localhost:3000/auth/login

```

## SQL Alchemyの操作
### テーブル作成/削除
```zsh
# todo-projectのルートで実行する。
cd {path_to_dir}/menta-flask-todo/todo-project

## テーブルの一括作成
flask create-tables

## テーブルの一括削除
flask drop-tables
```


## アプリケーションの実行
```zsh
cd {path_to_your_dir}/menta-flask-todo/todo-project
flask run --debug
```

## CSVを非同期でimportするためにceleryのワーカーを起動する。
### flask runとは別プロセスで同時に起動しておく。
```zsh
pipenv shell

cd {path_to_your_dir}/menta-flask-todo/todo-project
celery -A app.tasks.import_todos worker --loglevel=info
```

## 機能
### TODO
#### API仕様
```md
## CRUD
### Auth
- ユーザー登録
  - GET /auth/register
  - POST /auth/register

- ログイン機能
  - GET /auth/login
  - POST /auth/login

- ログアウト機能
  - GET /auth/logout

### Todo
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

### User
- ユーザー詳細
  - GET /user/:id
- ユーザー編集
  - GET /user/:id/edit
  - POST /user/:id
- ユーザー削除
  - POST /user/:id/delete
```

#### その他機能(付け足し)
```md
- DBの活用
  - ORMとして`SQL Alchemy`を用いてMySQLを用いる。
    - MySQLはdocker-composeを想定

- 認証
  - DBに保存されているemail, password_hashの値と一致するか

- 認可
  - JWTを想定

- 画面表示
  - SSRでtemplates配下のhtmlを表示
```

## テーブル定義
```zsh
mysql> SHOW COLUMNS FROM todos;
+--------------+--------------+------+-----+-------------------+-----------------------------------------------+
| Field        | Type         | Null | Key | Default           | Extra                                         |
+--------------+--------------+------+-----+-------------------+-----------------------------------------------+
| id           | int          | NO   | PRI | NULL              | auto_increment                                |
| title        | varchar(100) | NO   |     | NULL              |                                               |
| body         | text         | YES  |     | NULL              |                                               |
| is_completed | tinyint(1)   | NO   | MUL | 1                 |                                               |
| user_id      | int          | NO   | MUL | NULL              |                                               |
| created_at   | timestamp    | NO   | MUL | CURRENT_TIMESTAMP | DEFAULT_GENERATED                             |
| updated_at   | timestamp    | NO   | MUL | CURRENT_TIMESTAMP | DEFAULT_GENERATED on update CURRENT_TIMESTAMP |
| deleted_at   | timestamp    | YES  | MUL | NULL              |                                               |
+--------------+--------------+------+-----+-------------------+-----------------------------------------------+
8 rows in set (0.01 sec)

mysql> SHOW COLUMNS FROM users;
+---------------+--------------+------+-----+-------------------+-----------------------------------------------+
| Field         | Type         | Null | Key | Default           | Extra                                         |
+---------------+--------------+------+-----+-------------------+-----------------------------------------------+
| id            | int          | NO   | PRI | NULL              | auto_increment                                |
| name          | varchar(100) | NO   |     | NULL              |                                               |
| email         | varchar(255) | NO   | UNI | NULL              |                                               |
| password_hash | varchar(500) | NO   |     | NULL              |                                               |
| created_at    | timestamp    | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED                             |
| updated_at    | timestamp    | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED on update CURRENT_TIMESTAMP |
| deleted_at    | timestamp    | YES  |     | NULL              |                                               |
+---------------+--------------+------+-----+-------------------+-----------------------------------------------+
7 rows in set (0.01 sec)
```

## テストデータを挿入しDBの初期時の動作確認の結果
```sql
mysql> select * from users;
+----+--------------------+-----------------------+-------------------------+---------------------+---------------------+
| id | name               | email                 | password_hash           | created_at          | updated_at          |
+----+--------------------+-----------------------+-------------------------+---------------------+---------------------+
|  1 | 山田太郎           | yamada@example.com    | hashed_password_dummy_1 | 2025-05-12 22:59:36 | 2025-05-12 22:59:36 |
|  2 | 佐藤花子           | sato@example.com      | hashed_password_dummy_2 | 2025-05-12 22:59:36 | 2025-05-12 22:59:36 |
|  3 | 高橋ジョージ       | takahashi@example.com | hashed_password_dummy_3 | 2025-05-12 22:59:36 | 2025-05-12 22:59:36 |
+----+--------------------+-----------------------+-------------------------+---------------------+---------------------+
3 rows in set (0.001 sec)

mysql> select * from todos;
+----+-----------+-----------------------------------+---------+--------------+---------------------+---------------------+------------+
| id | title     | body                              | user_id | is_completed | created_at          | updated_at          | deleted_at |
+----+-----------+-----------------------------------+---------+--------------+---------------------+---------------------+------------+
|  1 | 買い物    | イオンに行く                      |       1 |            0 | 2025-05-12 23:01:14 | 2025-05-12 23:01:14 | NULL       |
|  2 | 仕事      | 出社する必要あり。                |       2 |            1 | 2025-05-12 23:01:14 | 2025-05-12 23:01:14 | NULL       |
|  3 | 食事      | 晩御飯はカレーライス。            |       2 |            0 | 2025-05-12 23:01:14 | 2025-05-12 23:01:14 | NULL       |
+----+-----------+-----------------------------------+---------+--------------+---------------------+---------------------+------------+
3 rows in set (0.001 sec)
```

## ログイン用ユーザー(マイケルさん)
```md
- email: michael@gmail.com
- password: michael
```
