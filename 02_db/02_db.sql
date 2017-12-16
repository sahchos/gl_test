-- 1) create a SQL dump of the next structs of entities:
--    * users with some data for authorization
--    * user comments
--    A count of users > 1000, a count of comments > 10**8.
--    This DB has to use for saving of comments and for searching they by user name
CREATE TABLE users(
   id bigserial PRIMARY KEY NOT NULL,
   username char(50) unique NOT NULL,
   email char(255),
   first_name char(30),
   last_name char(150),
   last_login_at timestamp,
   blocked_at timestamp
);

CREATE TABLE comments(
	id bigserial PRIMARY KEY NOT NULL,
	text text not null,
	created_at timestamp default current_timestamp,
	user_id bigint references users (id)
);

-- 2) write example requests:
-- 2.1) search the first name of user with the biggest amount of daily comments
WITH comment_count AS (SELECT user_id, COUNT(DATE(created_at)) as total_comments
	FROM comments
  GROUP BY user_id
)
SELECT first_name, total_comments
	FROM comment_count
    JOIN users ON user_id = users.id
  WHERE total_comments = (SELECT MAX(total_comments) from comment_count);

-- 2.2) block the first 10 users without comments
UPDATE users
  SET blocked_at=NOW()
WHERE users.id IN (
  SELECT users.id FROM users
    LEFT JOIN comments ON users.id = comments.user_id
  WHERE blocked_at ISNULL
  GROUP BY users.id
  HAVING COUNT(comments.id) = 0
  ORDER BY users.id LIMIT 10
);


-- 2.3) select a list of users blocked 1 years ago but with attempts of authorization for a last month
SELECT * FROM users
WHERE blocked_at <= NOW() - INTERVAL '1 year' AND
      users.last_login_at >= NOW() - INTERVAL '1 month';
