# Reddit Recovery Dashboard
 
Use this video to set up postgres. https://www.youtube.com/watch?v=7EeAZx78P2U

In Postgres terminal/GUI: The URI and credentials need to be the same!

EITHER:
- set postgres user password to admin
- create database "first"
- create table (CREATE TABLE users(id SERIAL PRIMARY KEY,username VARCHAR(25) UNIQUE NOT NULL);)

OR: 
Change this line in init_py:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/first'
to
'postgressql://[username]:[password]@localhost/[databasename]'

These are the commands to run from a python terminal. 

3/30 Update: to set up new db models:
- delete old table(s) using psql (drop table users;)
- run createTables.sql or copy and paste the code
- run the code below in vscode terminal (or however you did it before)

python

from dashboard import db

db.create_all()


