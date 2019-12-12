import psycopg2

from datetime import date
from config import DATABASE
from tasks import add_task, list_tasks, get_task, edit_task, delete_task

if __name__ == "__main__":
    con = psycopg2.connect(**DATABASE)
    with con.cursor() as cursor:
        try:
            add_task(con, date(2020, 4, 1), "Wake up")
            add_task(con, date(2020, 4, 1), "Make coffee")
            add_task(con, date(2020, 4, 1), "Go to the work")
            add_task(con, date(2020, 4, 1), "Save the world")
            add_task(con, date(2020, 4, 1), "Go back home")
            add_task(con, date(2020, 4, 1), "Go to sleep")
            print(list_tasks(con, date(2020, 4, 1)))

            print(get_task(con, date(2020, 4, 1), 47))
            edit_task(con, date(2020, 4, 1), 47, 'Wake up slowly')
            print(get_task(con, date(2020, 4, 1), 47))

            delete_task(con, date(2020, 4, 1), 47)
            print(list_tasks(con, date(2020, 4, 1)))

            con.commit()
        finally:
            if con:
                con.close()
