"""Module contain func to retrieve data from config file"""
from configparser import ConfigParser


def config(filename='database.ini', section='postgresql'):
    """Retrieve necessary data to connect to database

    :param filename: filename with necessary data
    :param section: section in filename
    :return: dict with data for database connection
    """
    parser = ConfigParser()
    parser.read(filename)
    db = {}

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]

    return db
