CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(30) NOT NULL,
    email VARCHAR (50) NOT NULL,
    created_at DATETIME
    );

CREATE TABLE posts (
    post_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    title TEXT NOT NULL,
    content TEXT,
    posted_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

INSERT INTO users (user_id, username, email, created_at) VALUES (1, 'John Doe', 'john.doe@example.com', '2021-01-01 12:00:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (2, 'Jane Smith', 'jane.smith@example.com', '2021-01-02 12:00:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (3, 'Jim Beam', 'jim.beam@example.com', '2021-01-03 12:00:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (4, 'Jill Johnson', 'jill.johnson@example.com', '2021-01-04 12:00:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (5, 'Jack White', 'jack.white@example.com', '2021-01-05 12:00:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (6, 'Jill Johnson', 'jill.johnson@example.com', '2021-01-04 12:00:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (7, 'Jack White', 'jack.white@example.com', '2021-01-05 12:00:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (8, 'Jill Johnson', 'jill.johnson@example.com', '2021-01-04 12:00:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (9, 'Jack White', 'jack.white@example.com', '2021-01-05 12:00:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (10, 'Jill Johnson', 'jill.johnson@example.com', '2021-01-04 12:00:00');




INSERT INTO posts (post_id, user_id, title, content, posted_at) VALUES (1, 1, 'Hello, World!', 'This is my first post.', '2021-01-01 12:00:00');
INSERT INTO posts (post_id, user_id, title, content, posted_at) VALUES (2, 2, 'This is my second post.', 'This is my second post.', '2021-01-02 12:00:00');
INSERT INTO posts (post_id, user_id, title, content, posted_at) VALUES (3, 3, 'This is my third post.', 'This is my third post.', '2021-01-03 12:00:00');
INSERT INTO posts (post_id, user_id, title, content, posted_at) VALUES (4, 4, 'This is my fourth post.', 'This is my fourth post.', '2021-01-04 12:00:00');
INSERT INTO posts (post_id, user_id, title, content, posted_at) VALUES (5, 5, 'This is my fifth post.', 'This is my fifth post.', '2021-01-05 12:00:00');
INSERT INTO posts (post_id, user_id, title, content, posted_at) VALUES (6, 6, 'This is my sixth post.', 'This is my sixth post.', '2021-01-06 12:00:00');
INSERT INTO posts (post_id, user_id, title, content, posted_at) VALUES (7, 7, 'This is my seventh post.', 'This is my seventh post.', '2021-01-07 12:00:00');
INSERT INTO posts (post_id, user_id, title, content, posted_at) VALUES (8, 8, 'This is my eighth post.', 'This is my eighth post.', '2021-01-08 12:00:00');
INSERT INTO posts (post_id, user_id, title, content, posted_at) VALUES (9, 9, 'This is my ninth post.', 'This is my ninth post.', '2021-01-09 12:00:00');
INSERT INTO posts (post_id, user_id, title, content, posted_at) VALUES (10, 10, 'This is my tenth post.', 'This is my tenth post.', '2021-01-10 12:00:00');

