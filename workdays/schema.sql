DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS groups;

CREATE TABLE users (
    id integer primary key autoincrement,
    username text unique not null,
    password text not null
);

CREATE TABLE groups (
    id integer primary key autoincrement,
    user_id integer not null,
    blob blob not null,
    foreign key (user_id) references users (id)
);