BEGIN;

DELETE FROM todos;
DELETE FROM users;

-- users
INSERT INTO users (name, email, password_hash) VALUES
('山田太郎', 'yamada@example.com', 'hashed_password_dummy_1'),
('佐藤花子', 'sato@example.com', 'hashed_password_dummy_2'),
('高橋ジョージ', 'takahashi@example.com', 'hashed_password_dummy_3');


-- todos
INSERT INTO todos (title, body, user_id, is_completed) VALUES 
('買い物','イオンに行く', 1,0),
('仕事','出社する必要あり。',2, 1),
('食事','晩御飯はカレーライス。',2,0);


COMMIT;
-- ROLLBACK;
