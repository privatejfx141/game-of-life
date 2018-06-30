def select_pattern_id(search_str, connection, by_rle=False):
    """(str, sqlite3.Connection[, bool]) -> int

    :param search_str: string to search, default is pattern name
    :param connection: connection to database
    :param by_rle: if True, search_str is a pattern RLE
    :return: row ID of pattern in pattern table
    """
    cursor = connection.cursor()
    sql_command = "SELECT id FROM pattern p WHERE "
    if by_rle:
        sql_command += "p.rle = \'{}\'".format(search_str)
    else:
        sql_command += "p.name = \'{}\'".format(search_str)
    cursor.execute(sql_command)
    row_id = cursor.fetchone()[0]
    return row_id


def select_pattern_info(row_id, connection):
    """(int, sqlite3.Connection) -> [str, str, int]

    :param row_id: row ID in the pattern table
    :param connection: connection to database
    :return: list of the row values from pattern table
    """
    cursor = connection.cursor()
    sql_command = """
    SELECT * FROM pattern p
    WHERE p.id = {}
    """.format(row_id)
    cursor.execute(sql_command)
    return cursor.fetchone()


def select_rule_id(search_str, connection, by_rulestring=False):
    """(str, sqlite3.Connection[, bool]) -> int

    :param search_str: string to search, default is rule name
    :param connection: connection to database
    :param by_rulestring: if True, search_str is a rulestring
    :return: row ID of rule in rule table
    """
    cursor = connection.cursor()
    sql_command = "SELECT id FROM rule r WHERE "
    if by_rulestring:
        sql_command += "r.rule = \'{}\'".format(search_str)
    else:
        sql_command += "r.name = \'{}\'".format(search_str)
    cursor.execute(sql_command)
    row_id = cursor.fetchone()[0]
    return row_id


def select_rule_info(row_id, connection):
    """(int, sqlite3.Connection) -> [str, str]

    :param row_id: row ID in the rule table
    :param connection: connection to database
    :return: list of the row values from rule table
    """
    cursor = connection.cursor()
    sql_command = """
    SELECT * FROM rule r
    WHERE r.id = {}
    """.format(row_id)
    cursor.execute(sql_command)
    return cursor.fetchone()
