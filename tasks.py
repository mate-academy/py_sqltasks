"""
Implement CRUD postgresql
operations in python
"""

import datetime
from typing import List
import psycopg2


CONNECT = psycopg2.connect(user="user1",
                           password="user1",
                           host="/tmp",
                           port="5432",
                           database="py_tasks")


def add_task(date: datetime.date, task: str) -> None:
    """
    add task to column name
    """
    cursor = CONNECT.cursor()
    cursor.execute("rollback")
    cursor.execute("""insert into dates
                    (date) values ('{}')
                    on conflict on constraint
                    unique_constraint 
                    do nothing""".format(date))
    CONNECT.commit()
    date_id = get_id(date)
    cursor.execute("""insert into tasks (name, date_id)
                    values ('{}', '{}')""".format(task, date_id))
    CONNECT.commit()
    cursor.close()


def get_id(date):
    """
    get id of given date
    in table dates
    """
    cursor = CONNECT.cursor()
    cursor.execute("""select id from dates where date='{}'""".format(date))
    date_id = cursor.fetchone()
    cursor.close()
    return date_id[0]


def list_task(date: datetime.date) -> List[str]:
    """
    list all tasks
    gor given date
    """
    cursor = CONNECT.cursor()
    cursor.execute("rollback")
    cursor.execute("""select name from tasks
                        where date_id='{}'""".format(get_id(date)))
    record = cursor.fetchall()
    cursor.close()
    return [''.join(i) for i in record]


def get_task(date: datetime.date, index: int) -> str:
    """
    get task on given
    date and index from
    table tasks
    """
    cursor = CONNECT.cursor()
    cursor.execute("rollback")
    cursor.execute("""select name from tasks
    where date_id='{}'""".format(get_id(date)))
    record = cursor.fetchone()
    cursor.close()
    return record[index]


def edit_task(date: datetime.date, index: int, new_task: str) -> None:
    """
    edit task on given
    date and index in
    table tasks
    """
    cursor = CONNECT.cursor()
    cursor.execute("rollback")
    cursor.execute("""
    update tasks set name = '{}'
                      where id = '{}'
                      and date_id = '{}'
                      """.format(new_task, index, get_id(date)))
    CONNECT.commit()
    cursor.close()


def delete_task(date: datetime.date, index: int) -> None:
    """
    delete record on given
    date and index from
    table tasks
    """
    cursor = CONNECT.cursor()
    cursor.execute("rollback")
    # cursor.execute("""select id from tasks where """)
    cursor.execute("""select * from tasks, dates
                 where date_id = dates.id and tasks.id = {0}
                 and date = '{1}'""".format(index, date))
    if not cursor.fetchone():
        raise KeyError
    cursor.execute("""delete from tasks where
                        date_id = '{}'
                        and id = '{}'""".format(get_id(date), index))
    CONNECT.commit()
    cursor.close()
