"""Task tracker interface"""

import datetime
from typing import List
import psycopg2

CONN = psycopg2.connect(dbname='py_sqltasks', user='task_admin',
                        password='test_password', host='localhost')


def add_task(date: datetime.date, task: str) -> None:
    """add task to task tracker"""
    cursor = CONN.cursor()
    cursor.execute("""select id from dates
            where date_field='{0}'""".format(date))
    current_id = cursor.fetchone()
    if not current_id:
        cursor.execute("""insert into dates (date_field)
                values ('{0}') returning id""".format(date))
        current_date_id = cursor.fetchone()[0]
    else:
        current_date_id = current_id[0]
    cursor.execute("""insert into tasks (task_name, date_id)
            values ('{0}', {1})""".format(task, current_date_id))
    CONN.commit()
    cursor.close()


def list_tasks(date: datetime.date) -> List[str]:
    """show list task from task tracker"""
    cursor = CONN.cursor()
    cursor.execute("""select task_name from dates, tasks
            where date_id = dates.id and date_field = '{0}'""".format(date))
    result = [task_name[0] for task_name in cursor]
    cursor.close()
    return result


def get_task(date: datetime.date, index: int) -> str:
    """show task from task tracker"""
    cursor = CONN.cursor()
    cursor.execute("""select task_name from dates, tasks
            where date_id = dates.id and date_field = '{0}'
            and tasks.id = {1}""".format(date, index))
    result = cursor.fetchone()
    cursor.close()
    if not result:
        raise KeyError
    return result[0]


def edit_task(date: datetime.date, index: int, new_task: str) -> None:
    """edit task in task tracker"""
    cursor = CONN.cursor()
    cursor.execute("""select tasks.id from tasks, dates
            where date_id = dates.id and tasks.id = {0}
            and date_field = '{1}'""".format(index, date))
    if not cursor.fetchone():
        raise KeyError
    cursor.execute("""update tasks set task_name = '{0}'
            where id = {1}""".format(new_task, index))
    CONN.commit()
    cursor.close()


def delete_task(date: datetime.date, index: int) -> None:
    """delete task from task tracker"""
    cursor = CONN.cursor()
    cursor.execute("""select tasks.id from tasks, dates
            where date_id = dates.id and tasks.id = {0}
            and date_field = '{1}'""".format(index, date))
    if not cursor.fetchone():
        raise KeyError
    cursor.execute("delete from tasks where id = {0}".format(index))
    CONN.commit()
    cursor.close()
