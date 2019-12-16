create database py_tasks;

create user user1 with encrypted password = 'user1';

grant all privileges on table dates to user1;
grant all privileges on table tasks to user1;

create table dates(
id serial primary key,
date date unique);

create table tasks(
id serial primary key,
name varchar(66) not null,
date_id integer references dates(id));

grant all on sequence tasks_id_seq to user1;
grant all on sequence dates_id_seq to user1;

###alter sequence tasks_id_seq restart with 1;

