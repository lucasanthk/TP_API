CREATE TABLE IF NOT EXISTS users (
    id serial primary key,
    firstname varchar,
    lastname varchar,
    age int,
    email varchar,
    job varchar
);

CREATE TABLE IF NOT EXISTS application (
    id serial primary key,
    appname varchar,
    username varchar,
    lastconnection date,
    user_id varchar
);