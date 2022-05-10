from sqlalchemy import create_engine

db_string="postgresql://root:root@localhost:5432/store"

engine = create_engine(db_string)
connection = engine.connect()
bd = open('create.sql')
connection.execute(bd.read())
bd.close()
#Creation des tables Users et Application
#connection.execute("CREATE TABLE IF NOT EXISTS Users (id serial primary key, firstname text, lastname text, age int, email text, job text)")
#connection.execute("CREATE TABLE IF NOT EXISTS Application (id serial primary key, appname text, username text, lastconnection date, user_id text)")
