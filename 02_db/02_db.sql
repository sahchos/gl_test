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
-- 2.2) block the first 10 users without comments
-- 2.3) select a list of users blocked 1 years ago but with attempts of authorization for a last month
