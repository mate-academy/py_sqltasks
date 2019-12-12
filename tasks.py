"""
CRUD properties implementation
"""
from datetime import date
from typing import List


def add_task(con, task_date: date, task: str) -> None:
    """
    Add new task to db.
    :param con: str
    :param task_date: date
    :param task: str
    :return: None
    """
    with con.cursor() as cursor:
        cursor.execute("""SELECT Id FROM valentyna.public.dates
                        WHERE dates.taskdate='{0}'""".format(task_date))
        current_id = cursor.fetchone()
        if not current_id:
            cursor.execute("""INSERT INTO valentyna.public.dates(taskdate)
                            VALUES ('{0}') 
                            RETURNING id""".format(task_date))
            current_date_id = cursor.fetchone()[0]
        else:
            current_date_id = current_id[0]
        cursor.execute("""INSERT INTO valentyna.public.tasks(taskname, dateid)
                        VALUES ('{0}', {1})""".format(task, current_date_id))
    con.commit()


def list_tasks(con, task_date: date) -> List[str]:
    """
    Get list of tasks from db using date parameter.
    :param con: str
    :param task_date: date
    :return: List[str]
    """
    cursor = con.cursor()
    cursor.execute("""SELECT taskname FROM valentyna.public.tasks, valentyna.public.dates
                    WHERE tasks.dateid = dates.id 
                    AND dates.taskdate = '{0}'""".format(task_date))
    result = [task_name[0] for task_name in cursor]
    cursor.close()
    return result


def get_task(con, task_date: date, index: int) -> str:
    """
    Get task from db using index parameter.
    :param con: str
    :param task_date: date
    :param index: int
    :return: str
    """
    cursor = con.cursor()
    cursor.execute("""SELECT tasks.taskname FROM valentyna.public.dates, valentyna.public.tasks
                    WHERE dates.id = tasks.dateid 
                    AND dates.taskdate = '{0}'
                    AND tasks.id = {1}""".format(task_date, index))
    result = cursor.fetchone()
    cursor.close()
    return result[0]


# why we need use here task_date: date parameter?
def edit_task(con, task_date: date, index: int, new_task: str) -> None:
    """
    Update task in db.
    :param task_date: date
    :param index: int
    :param new_task: str
    :return: None
    """
    with con.cursor() as cursor:
        cursor.execute("""SELECT tasks.id
                        FROM valentyna.public.tasks, valentyna.public.dates
                        WHERE tasks.dateid = dates.id
                        AND tasks.id = {0}
                        AND dates.taskdate = '{1}'""".format(index, task_date))
        task_id = cursor.fetchone()[0]
        cursor.execute("""UPDATE valentyna.public.tasks
                        SET taskname = '{0}'
                        WHERE id = '{1}'""".format(new_task, task_id))
    con.commit()


def delete_task(con, task_date: date, index: int) -> None:
    """
    Delete task in db.
    :param task_date: date
    :param con: str
    :param index: int
    :return: None
    """
    with con.cursor() as cursor:
        cursor.execute("""SELECT tasks.id
                        FROM valentyna.public.tasks, valentyna.public.dates
                        WHERE tasks.dateid = dates.id
                        AND tasks.id = {0}
                        AND dates.taskdate = '{1}'""".format(index, task_date))
        task_id = cursor.fetchone()[0]
        cursor.execute("""DELETE FROM valentyna.public.tasks WHERE id = {0}""".format(task_id))
    con.commit()
