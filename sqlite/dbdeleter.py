def delete_pattern(row_id, connection):
    """(int, sqlite3.Connection) -> bool

    :param row_id: row ID in the pattern table
    :param connection: connection to database
    :return: True if row deletion was successful
    """
    cursor = connection.cursor()
    sql_command = """
    DELETE FROM
        pattern p
    WHERE
        p.id = {}
    """.format(row_id)
    cursor.execute(sql_command)
    connection.commit()
    return True


def delete_rule(row_id, connection):
    """(int, sqlite3.Connection) -> bool

    :param row_id: row ID in the rule table
    :param connection: connection to database
    :return: True if row deletion was successful
    """
    cursor = connection.cursor()
    sql_command = """
    DELETE FROM
        rule r
    WHERE
        r.id = {}
    """.format(row_id)
    cursor.execute(sql_command)
    connection.commit()
    return True
