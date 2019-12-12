import datetime

import psycopg2
import pytest

import tasks
from config import DATABASE


def test_create():
    con = psycopg2.connect(**DATABASE)
    tasks.add_task(con, datetime.date(2020, 4, 1), "Wake up")
    assert tasks.get_task(con, datetime.date(2020, 4, 1), 1) == "Wake up"


def test_list():
    con = psycopg2.connect(**DATABASE)
    tasks.add_task(con, datetime.date(2020, 4, 1), "Wake up again")
    tasks.add_task(con, datetime.date(2020, 4, 1), "Make coffee")
    assert tasks.list_tasks(con, datetime.date(2020, 4, 1)) == ["Wake up", "Wake up again", "Make coffee"]


def test_update():
    con = psycopg2.connect(**DATABASE)
    tasks.add_task(con, datetime.date(2020, 4, 1), "Wake up")
    tasks.edit_task(con, datetime.date(2020, 4, 1), 1, "Make coffee")
    assert tasks.get_task(con, datetime.date(2020, 4, 1), 1) == "Make coffee"


def test_delete():
    con = psycopg2.connect(**DATABASE)
    tasks.add_task(con, datetime.date(2020, 4, 1), "Wake up")
    tasks.delete_task(con, datetime.date(2020, 4, 1), 1)
    with pytest.raises(TypeError):
        tasks.get_task(con, datetime.date(2020, 4, 1), 1)
