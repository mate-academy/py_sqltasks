import psycopg2

from config import DATABASE
from db_utils import fill_tables

if __name__ == "__main__":
    con = psycopg2.connect(**DATABASE)
    with con.cursor() as cursor:
        try:
            fill_tables(cursor)
            con.commit()
        finally:
            if con:
                con.close()
