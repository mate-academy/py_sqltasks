--CREATING TABLES IN POSTGRES DATABASE

CREATE TABLE date_of_task(
    date_id SERIAL PRIMARY KEY,
    date_repr DATE
    UNIQUE(date_repr)
);

CREATE TABLE task(
    task_id SERIAL PRIMARY KEY,
    task_name VARCHAR(30) NOT NULL,
    task_date integer,
    FOREIGN KEY (task_date) REFERENCES date_of_task(date_id)
    UNIQUE(task_name, task_date)
);


GRANT ALL ON TABLE date_of_task TO postgres;
GRANT ALL ON TABLE task TO postgres;