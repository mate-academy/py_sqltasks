"""Module defines function to
- add items to db tables
- get items from db tables
- update data about items
- delete items from tables
"""
import datetime
from typing import List
import psycopg2
from config import config

CONNECT_PARAMS = config()


def add_task(date: datetime.date, task: str) -> None:
    """
    Add data about task to data_of_task and task tables
    :param date: date of task
    :param task: task name
    :return: None
    """
    conn = psycopg2.connect(**CONNECT_PARAMS)
    cur = conn.cursor()
    try:
        cur.execute("""INSERT INTO date_of_task (date_repr)
                    VALUES (%s) RETURNING date_id;""", (date,))
        date_id = cur.fetchone()[0]
        conn.commit()
    except psycopg2.IntegrityError:
        conn.rollback()
        cur.execute("""SELECT date_id FROM date_of_task
                    WHERE date_repr = %s;""", (date,))
        date_id = cur.fetchone()[0]

    try:
        cur.execute("""INSERT INTO task (task_name, task_date)
                    VALUES (%s, %s);""", (task, date_id))
        conn.commit()
    except psycopg2.IntegrityError:
        conn.rollback()
        print('There is already exist same task')
    finally:
        conn.close()


def list_tasks(date: datetime.date) -> List[str]:
    """
    Retrieve tasks by date
    :param date: date for task(s)
    :return: list with task_names (strings)
    """
    result = []
    conn = psycopg2.connect(**CONNECT_PARAMS)
    cur = conn.cursor()
    date_id = get_date_id(date, cur, conn)

    cur.execute("""SELECT task_name FROM task
                WHERE task_date = %s;""", (date_id,))
    for task in cur.fetchall():
        result.append(task[0])
    conn.close()
    return result


def get_task(date: datetime.date, index: int) -> str:
    """
    Get task's name by date and index
    :param date: date of task
    :param index: task_id
    :return: name of task
    """
    conn = psycopg2.connect(**CONNECT_PARAMS)
    cur = conn.cursor()
    date_id = get_date_id(date, cur, conn)

    cur.execute("""SELECT task_name
                FROM task
                WHERE task_date = %s AND task_id = %s""", (date_id, index))

    task_name = cur.fetchone()

    if task_name is None:
        conn.close()
        raise KeyError
    return task_name[0]


def edit_task(date: datetime.date, index: int, new_task: str) -> None:
    """
    Update name of task
    :param date: date of task
    :param index: index of old task
    :param new_task: name of new task
    :return:
    """
    conn = psycopg2.connect(**CONNECT_PARAMS)
    cur = conn.cursor()
    date_id = get_date_id(date, cur, conn)

    cur.execute("""UPDATE task
                SET task_name = %s
                WHERE task_date = %s AND task_id = %s""",
                (new_task, date_id, index))
    conn.commit()
    conn.close()


def delete_task(date: datetime.date, index: int) -> None:
    """
    Remove task from task table
    :param date: date of task
    :param index: task_id
    :return:
    """
    conn = psycopg2.connect(**CONNECT_PARAMS)
    cur = conn.cursor()
    date_id = get_date_id(date, cur, conn)
    cur.execute("""DELETE FROM task
                WHERE task_date = %s AND task_id = %s""", (date_id, index))
    conn.commit()
    conn.close()


def get_date_id(date, cursor, connection):
    """
    Function to get date_id
    :param date: date object
    :param cursor: cursor object
    :param connection: connection object
    :return: date_id (if exist)
    """
    cursor.execute("""SELECT date_id FROM date_of_task
                     WHERE date_repr = %s;""", (date,))
    date_id = cursor.fetchone()

    if not date_id:
        connection.close()
        raise KeyError

    return date_id[0]
