DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS groups;

CREATE TABLE user (
    id integer primary key autoincrement,
    username text unique not null,
    password text not null
);

CREATE TABLE groups (
    id integer primary key autoincrement,
    user_id integer not null,
    group_json blob not null,
    foreign key (user_id) references users (id) 
);