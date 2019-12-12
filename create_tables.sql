DROP TABLE dates CASCADE;
DROP TABLE tasks CASCADE;
create table dates (
id serial primary key,
date_field date
);
create table tasks (
id serial primary key,
task_name varchar(100),
date_id integer references dates(id)
);
grant all privileges on table dates to task_admin;
grant all privileges on table tasks to task_admin;
grant all on sequence dates_id_seq to task_admin;
grant all on sequence tasks_id_seq to task_admin;

