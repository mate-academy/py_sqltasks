"""Implement CRUD for database"""
from typing import List
import datetime
import psycopg2

# pylint: disable=C0103
connection = psycopg2.connect(host="localhost", dbname="t", user="u", password="1")
connection.commit()

def add_task(date: datetime.date, task: str):
    """
    Add task to database. If there are tasks on specified date add new task.
    If there are not tasks on specified date add this date and add new task.
    :param date: date
    :param task: name of task
    :return: None
    """
    check_inputs(date, task=task)
    with connection.cursor() as cursor:
        try:
            # date present in dates table. Add task
            id_date = get_date_id(date, cursor)
            cursor.execute(f"insert into tasks (task, date_id) values ('{task}', '{id_date}')")
        except TypeError:
            # date absent in dates. Add date, task
            cursor.execute(f"insert into dates (date) values ('{date}') returning id_date")
            id_date = cursor.fetchone()[0]
            cursor.execute(f"insert into tasks (task, date_id) values ('{task}', '{id_date}')")
        connection.commit()


def get_task(date: datetime.date, index: int) -> str:
    """
    Get task from database.
    :param date: date
    :param index: index of task on specified date
    :return: name of task of report to user
    :raise KeyError if task by specified index doesnt exist
    """
    check_inputs(date, index)
    with connection.cursor() as cursor:
        try:
            id_date = get_date_id(date, cursor)
            cursor.execute(f"""select task from tasks where date_id='{id_date}'
                                        order by id_task asc limit 1 offset '{index}'""")
            task = cursor.fetchone()
            if task is None:
                print(f"No task with index '{index}'")
                raise KeyError
            return task[0]
        except TypeError:
            # raise here or return?
            return f"No date '{date}' in dates'"


def edit_task(date: datetime.date, index: int, new_task: str):
    """
    Edit task in database.
    :param date:
    :param index:
    :param new_task:
    :return: message to user
    """
    check_inputs(date, index, new_task)
    with connection.cursor() as cursor:
        try:
            task_index = get_task_index(date, cursor, index)
            cursor.execute(f"update tasks set task='{new_task}' where id_task='{task_index}'")
            return "updated"
        except TypeError:
            return f"No date '{date}' in dates'"
        connection.commit()


def delete_task(date: datetime.date, index: int):
    """
    Delete task from database.
    :param date: date
    :param index: index of task on specified date
    :return: message to user
    """
    check_inputs(date, index)

    with connection.cursor() as cursor:
        try:
            task_index = get_task_index(date, cursor, index)
            cursor.execute(f"delete from tasks where id_task='{task_index}'")
            return "Deleted"
        except TypeError:
            return f"No date '{date}' in dates'"
        connection.commit()


def list_tasks(date: datetime.date) -> List[str]:
    """
    :param date: date
    :return: list of tasks on specified date. [] if no tasks on specified date
    """
    check_inputs(date)
    with connection.cursor() as cursor:
        try:
            id_date = get_date_id(date, cursor)
            cursor.execute(f"select task from tasks where date_id='{id_date}' order by id_task asc")
            return [row[0] for row in cursor.fetchall()]
        except TypeError:
            return []


def get_date_id(date: datetime.date, cursor):
    """
    Find id of specified date from dates table
    :param date: date
    :param cursor: cursor
    :return: id if date in dates table
    :raise TypeError if date not in dates table
    """
    cursor.execute(f"select id_date from dates where date='{date}'")
    id_ = cursor.fetchone()
    if id_ is not None:
        return id_[0]
    raise TypeError


def get_task_index(date: datetime.date, cursor, index):
    """
    Find index in tasks table.
    :param date: date
    :param cursor:
    :param index: index of task on specified date
    :return: index of task in tasks table
    """
    id_date = get_date_id(date, cursor)
    cursor.execute(f"""select id_task from dates,tasks where dates.id_date = tasks.date_id
                                        and id_date = '{id_date}' order by id_task asc limit 1""")
    return cursor.fetchone()[0] + index


def check_inputs(date=datetime.date(1111, 1, 1), index=1, task="str"):
    """
    Check all inputs from user
    :param date: date of task
    :param index: index of task
    :param task: name of task
    :return: None
    :raise ValueError if inputs are invalid
    """
    if not date or not isinstance(date, datetime.date):
        print("invalid input: date")
        raise ValueError
    if not isinstance(index, int) or index < 0:
        print("invalid input: index")
        raise ValueError
    if not task or not isinstance(task, str):
        print("invalid input: task")
        raise ValueError


connection.close()
