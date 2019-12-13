CREATE DATABASE tasks_db;

\c tasks_db;
DROP TABLE IF EXISTS time;
DROP TABLE IF EXISTS tasks;

CREATE TABLE time (
    time_id SERIAL PRIMARY KEY,
    day DATE
    );

CREATE TABLE tasks (
    task_id SERIAL PRIMARY KEY,
    task TEXT
    );

grant all privileges on table time to postgres;
grant all privileges on table tasks to postgres