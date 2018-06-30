def insert_pattern(name, rle, ptype, rule_id, connection):
    """(str, str, str, int, sqlite3.Connection) -> int

    :param name: name of the pattern
    :param rle: pattern RLE
    :param ptype: pattern type
    :param rule_id: ID integer of rulestring
    :param connection: connection to database
    :return: ID of the inserted row
    """
    cursor = connection.cursor()
    sql_command = """
    INSERT INTO
        pattern (name, rle, type, rule_id)
    VALUES
        (\'{}\', \'{}\', \'{}\', {})
    """.format(name, rle, ptype, rule_id)
    cursor.execute(sql_command)
    connection.commit()
    row_id = cursor.lastrowid
    return row_id


def insert_rule(name, rulestring, connection):
    """(str, sqlite3.Connection) -> int

    :param name: name of the rulestring
    :param rulestring: rulestring
    :param connection: connection to database
    :return: ID of the inserted row
    """
    cursor = connection.cursor()
    sql_command = """
        INSERT INTO
            rule (name, rule)
        VALUES
            (\'{}\', \'{}\')
        """.format(name, rulestring)
    cursor.execute(sql_command)
    connection.commit()
    row_id = cursor.lastrowid
    return row_id
