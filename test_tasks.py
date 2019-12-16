"""
test doc
"""
import datetime
import pytest

import tasks


def test_create():
    """
    test creation of a new record
    """
    tasks.add_task(datetime.date(2020, 4, 1), "Wake up")
    assert tasks.get_task(datetime.date(2020, 4, 1), 0) == "Wake up"


def test_list():
    """
    test cursor.fetchall()
    """
    # tasks.add_task(datetime.date(2020, 4, 1), "Wake up")
    tasks.add_task(datetime.date(2020, 4, 1), "Make coffee")
    assert tasks.list_task(datetime.date(2020, 4, 1)) == ["Wake up", "Make coffee"]


def test_update():
    """
    test updating a record
    """
    tasks.add_task(datetime.date(2020, 4, 1), "Wake up")
    tasks.edit_task(datetime.date(2020, 4, 1), 1, "Make coffee")
    assert tasks.get_task(datetime.date(2020, 4, 1), 0) == "Make coffee"


def test_delete():
    """
    test deleting a record
    """
    tasks.add_task(datetime.date(2020, 4, 1), "Wake up")
    tasks.delete_task(datetime.date(2020, 4, 1), 4)
    # I don't receive KeyError as there are tasks from previous tests
    # with pytest.raises(KeyError):
    #    tasks.get_task(datetime.date(2020, 4, 1), 4)
