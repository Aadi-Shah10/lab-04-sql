SELECT users.username, posts.title, posts.content FROM posts
JOIN users ON posts.user_id = users.user_id
WHERE posts.posted_at > '2021-01-04 12:00:00';
