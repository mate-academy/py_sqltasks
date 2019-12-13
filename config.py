"""
Module to generate tasks_db database connection configurations

Functions
---------
config(filename, section)
create_tables()
"""
from configparser import ConfigParser
import psycopg2


def config(filename='database.ini', section='postgresql'):
    """
    Return connection parameters for tasks_db database.
    :filename: str
    :section: str
    :return: dict
    """
    parser = ConfigParser()
    parser.read(filename)
    db = {}

    if parser.has_section(section):
        parameters = parser.items(section)
        for param in parameters:
            db[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in {filename} file")
    return db


CONNECTION_PARAMETERS = config()


def create_tables():
    """
    Create tables time and tasks in tasks_db database.
    :return: None
    """
    commands = (
        """
        CREATE TABLE time (
        time_id SERIAL PRIMARY KEY,
        day DATE
        )""",

        """
        CREATE TABLE tasks (
        task_id SERIAL PRIMARY KEY,
        task TEXT
        )"""
    )

    conn = None
    try:
        with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
            with conn.cursor() as cursor:
                for command in commands:
                    cursor.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
