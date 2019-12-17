import datetime
import pytest

import tasks


def test_create():
    tasks.add_task(datetime.date(2020, 4, 1), "Wake up")
    assert tasks.get_task(datetime.date(2020, 4, 1), 1) == "Wake up"


def test_list():
    tasks.add_task(datetime.date(2020, 5, 2), "Write story")
    tasks.add_task(datetime.date(2020, 5, 2), "Make coffee")
    assert tasks.list_tasks(datetime.date(2020, 5, 2)) == ["Write story",
                                                           "Make coffee"]


def test_update():
    tasks.add_task(datetime.date(2020, 6, 3), "Open book")
    tasks.edit_task(datetime.date(2020, 6, 3), 1, "Close book")
    assert tasks.get_task(datetime.date(2020, 6, 3), 1) == "Close book"


def test_delete():
    tasks.delete_task(datetime.date(2020, 4, 1), 1)
    with pytest.raises(KeyError):
        tasks.get_task(datetime.date(2020, 4, 1), 1)


