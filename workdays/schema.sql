DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS groups;
DROP TABLE IF EXISTS members;

CREATE TABLE users (
    id integer primary key autoincrement,
    username text unique not null,
    password text not null
);

CREATE TABLE groups (
    id integer primary key autoincrement,
    group_name text not null,
    user_id integer not null,
    members_id text not null,
    foreign key (user_id) references users (id),
    foreign key (members_id) references members (id)
);

CREATE TABLE members (
    id integer primary key autoincrement,
    name text not null,
    days text not null,
    preference text not null
);