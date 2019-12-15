import datetime
import pytest

import tasks


def test_create():
    tasks.add_task(datetime.date(2020, 4, 1), "Wake up")
    assert tasks.get_task(datetime.date(2020, 4, 1), 0) == "Wake up"


def test_list():
    tasks.add_task(datetime.date(2020, 4, 1), "Wake up")
    tasks.add_task(datetime.date(2020, 4, 1), "Make coffee")
    assert tasks.list_tasks(datetime.date(2020, 4, 1)) == ["Wake up", "Make coffee"]


def test_update():
    tasks.add_task(datetime.date(2020, 4, 1), "Wake up")
    tasks.edit_task(datetime.date(2020, 4, 1), 0, "Make coffee")
    assert tasks.get_task(datetime.date(2020, 4, 1), 0) == "Make coffee"


def test_delete():
    tasks.add_task(datetime.date(2020, 4, 1), "Wake up")
    tasks.delete_task(datetime.date(2020, 4, 1), 0)
    with pytest.raises(KeyError):
        tasks.get_task(datetime.date(2020, 4, 1), 0)


