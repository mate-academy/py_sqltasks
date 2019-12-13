"""
Module with implemented CRUD operations for tasks_db database.

Functions:
---------
add_task(date, task)
list_task(date)
get_task(date, index)
edit_task(date, index, new_task)
delete_task(date, index)
"""
import datetime
from typing import List
import psycopg2
from config import config


CONNECTION_PARAMETERS = config()


def add_task(date: datetime.date, task: str) -> None:
    """
    Add new task to tasks_db database.
    :date: datetime.date
    :task: str
    :return: None
    """
    with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT day, task
                FROM time INNER JOIN tasks ON time.time_id = tasks.task_id
                WHERE day = '{date}' AND task = '{task}'
                """)
            date_task = cur.fetchone()
            if date_task != (date, task):
                cur.execute("insert into time (day) values (%s)", (date,))
                cur.execute("INSERT INTO tasks (task) VALUES (%s)", (task,))
                print(f"Task {task} added to the database.")
            else:
                print(f"{task} task already exists for {date}")
    conn.close()


def list_task(date: datetime.date) -> List[str]:
    """
    Return list of all tasks in tasks_db for specified date
    :date: datetime.date
    :return: List[str]
    """
    conn = psycopg2.connect(**CONNECTION_PARAMETERS)
    with conn.cursor() as cur:
        cur.execute(f"""
            SELECT task 
            FROM tasks 
            INNER JOIN time ON tasks.task_id = time.time_id 
            WHERE day = '{date}'
            """)
        tasks = cur.fetchall()
    conn.close()
    return [task[0] for task in tasks]


def get_task(date: datetime.date, index: int) -> str:
    """
    Return task for specified date by index from tasks_db.
    If such task doesn't exists - raise KeyError.
    :date: datetime.date
    :index: int
    :return: str
    """
    conn = psycopg2.connect(**CONNECTION_PARAMETERS)
    with conn.cursor() as cur:
        cur.execute(f"""
            SELECT task 
            FROM tasks INNER JOIN time ON tasks.task_id = time.time_id 
            WHERE day = '{date}' AND task_id = '{index}'
            """)
        task = cur.fetchone()
    conn.close()
    if task is None:
        raise KeyError
    return task[0]


def edit_task(date: datetime.date, index: int, new_task: str) -> None:
    """
    Replace existing task with a new one.
    :date: datetime.date
    :index: int
    :new_task: str
    :return: None
    """
    with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT day, time_id
                FROM time
                WHERE day = '{date}' AND time_id = '{index}'
                """)
            date_index = cur.fetchone()
            if date_index == (date, index):
                cur.execute(f"""
                    UPDATE tasks
                    SET task = '{new_task}'
                    FROM time
                    WHERE day = '{date}' AND task_id = '{index}'
                    """)
                print("Task updated.")
            else:
                print(f'There are no date {date} with id {index} in the database!')
    conn.close()


def delete_task(date: datetime.date, index: int) -> None:
    """
    Delete task from the database.
    :date: datetime.date
    :index: int
    :return: None
    """
    with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT day, time_id
                FROM time
                WHERE day = '{date}' AND time_id = '{index}'
                """)
            date_index = cur.fetchone()
            if date_index == (date, index):
                cur.execute(f"""
                    DELETE 
                    FROM tasks
                    USING time
                    WHERE tasks.task_id = time.time_id 
                    AND day = '{date}' AND task_id = '{index}'
                    """)
                print(f"Task with id {index} deleted.")
            else:
                print(f'There are no date {date} with id {index} in the database!')
    conn.close()
