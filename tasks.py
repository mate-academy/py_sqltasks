"""
Create database to store a list of tasks for some date. Implement CRUD for this database.
Make all tests independent from database content.
"""


import datetime
from typing import List
import psycopg2

CON = psycopg2.connect(
    database="db_sql_task",
    user="myuser",
    password="1111",
    host="localhost",
    port="5432"
)


def add_task(date: datetime.date, task: str) -> None:
    """Add to db"""
    cur = CON.cursor()

    cur.execute("select id from dates_table where datetask='{}'".format(date))
    cur_id = cur.fetchone()

    if cur_id:
        cur.execute("""
            insert into tasks_table (name, id_date) values ('{}', {})
            """.format(task, cur_id[0]))
    else:
        cur.execute("""
                insert into dates_table (datetask) values('{}')
            """.format(date))

        cur.execute("select id from dates_table where datetask='{}'".format(date))
        cur_id = cur.fetchone()

        cur.execute("""
                insert into tasks_table (name, id_date) values ('{}', {})
            """.format(task, cur_id[0]))

    CON.commit()
    cur.close()


def list_task(date: datetime.date) -> List[str]:
    """Get list task"""
    cur = CON.cursor()

    cur.execute("select id from dates_table where datetask='{}'".format(date))
    cur_id = cur.fetchone()[0]

    if not cur_id:
        raise KeyError

    cur.execute("select name from tasks_table where id_date={}".format(cur_id))
    cur_str = cur.fetchall()

    CON.commit()
    cur.close()
    return [i[0] for i in cur_str]


def get_task(date: datetime.date, index: int) -> str:
    """Get task"""
    cur = CON.cursor()

    cur.execute("select id from dates_table where datetask='{}'".format(date))
    cur_id = cur.fetchone()[0]

    if not cur_id:
        raise KeyError

    cur.execute("select name from tasks_table where id_date={}".format(cur_id))

    try:
        cur_str = cur.fetchone()[index]
    except TypeError:
        raise KeyError

    CON.commit()
    cur.close()
    return cur_str


def edit_task(date: datetime.date, index: int, new_task: str) -> None:
    """Edit task"""
    cur = CON.cursor()

    cur.execute("select id from dates_table where datetask='{}'".format(date))
    cur_id = cur.fetchone()[0]

    if not cur_id:
        raise KeyError

    cur.execute("""
            select id from tasks_table where id_date='{}'
        """.format(cur_id))
    cur_id_task = cur.fetchall()[index][0]
    cur.execute("""
                update tasks_table set name='{}' where id={}
            """.format(new_task, cur_id_task))

    CON.commit()
    cur.close()


def delete_task(date: datetime.date, index: int) -> None:
    """Del task"""
    cur = CON.cursor()

    cur.execute("select id from dates_table where datetask='{}'".format(date))
    cur_id = cur.fetchone()[0]

    if not cur_id:
        raise KeyError

    cur.execute("""
            select id from tasks_table where id_date='{}'
        """.format(cur_id))
    cur_id_task = cur.fetchall()[index][0]
    cur.execute("""
                delete from tasks_table where id={}
            """.format(cur_id_task))

    CON.commit()
    cur.close()
