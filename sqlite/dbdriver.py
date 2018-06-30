import sqlite3

DB_FILE_NAME = "gol.db"


def initialize_database():
    """() -> sqlite3.Connection

    :return: Connection to database
    """
    connection = sqlite3.connect(DB_FILE_NAME)
    cursor = connection.cursor()
    # create rule table
    sql_command = """
    CREATE TABLE rule (
        id INTEGER PRIMARY KEY,
        name character(127),
        rule CHARACTER(63)
    );
    """
    cursor.execute(sql_command)
    # create pattern rle table
    sql_command = """
    CREATE TABLE pattern (
        id INTEGER PRIMARY KEY,
        name CHARACTER(127),
        rle CLOB,
        type CHARACTER(127),
        rule_id INTEGER,
        FOREIGN KEY(rule_id) REFERENCES rule(id)
    );
    """
    cursor.execute(sql_command)
    # return the connection
    return connection


def connect_to_database():
    """() -> sqlite3.Connection

    :return: Connection to database
    """
    connection = sqlite3.connect(DB_FILE_NAME)
    return connection


if __name__ == "__main__":
    db_connect = connect_to_database()
    db_connect.close()
