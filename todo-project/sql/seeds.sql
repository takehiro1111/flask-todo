BEGIN;

-- 外部キー制約があるままだとusersテーブルを削除できないため。
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE todos; 
TRUNCATE TABLE users;
SET FOREIGN_KEY_CHECKS = 1;

-- users
-- hashed_password_dummy_1(sha256)
-- hashed_password_dummy_2(sha512)
-- hashed_password_dummy_3(MD5)
INSERT INTO users (name, email, password_hash) VALUES
('山田太郎', 'yamada@example.com', '20262b45538ad0741cba091296236bd2c804e698870ee8472aac846f0113f111'),
('佐藤花子', 'sato@example.com', '6881f0556de3db6050ec93387ba6337c13cbb9eb8b9bab122d37e1153cec57dd29a2bfc1413daab8e13489b3e7a2f73ec740bb3da8605514e89db28808501d9f'),
('高橋ジョージ', 'takahashi@example.com', '265529a61935301d219ea7ce1edda400');


-- todos
INSERT INTO todos (title, body, user_id, is_completed) VALUES 
('買い物','イオンに行く', 1,0),
('仕事','出社する必要あり。',2, 1),
('食事','晩御飯はカレーライス。',2,0);


COMMIT;
-- ROLLBACK;
