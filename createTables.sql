
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(300) NOT NULL,
    subreddit VARCHAR(21) NOT NULL,
    submission_id VARCHAR(100) NOT NULL,
    body_text VARCHAR(40000),
    num_comments INTEGER);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    comment_id VARCHAR(100) NOT NULL,
    date_created BIGINT NOT NULL,
    parent VARCHAR(100) NOT NULL,
    subreddit VARCHAR(21) NOT NULL,
    body_text VARCHAR(30000) NOT NULL);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(25) UNIQUE NOT NULL,
    post_id INTEGER REFERENCES posts (id),
    comment_id INTEGER REFERENCES comments (id));
