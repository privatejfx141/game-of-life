def update_pattern(row_id, rle, connection):
    """(int, str, sqlite3.Connection) -> bool

    :param row_id:
    :param rle:
    :param connection:
    :return:
    """
    cursor = connection.cursor()
    connection.commit()


def update_pattern_name(row_id, name, connection):
    """(int, str, sqlite3.Connection) -> bool

    :param row_id:
    :param name:
    :param connection:
    :return:
    """
    cursor = connection.cursor()
    connection.commit()


def update_pattern_type(row_id, ptype, connection):
    """(int, str, sqlite3.Connection) -> bool

    :param row_id:
    :param ptype:
    :param connection:
    :return:
    """
    cursor = connection.cursor()
    connection.commit()


def update_pattern_rule(row_id, rule_id, connection):
    """(int, int, sqlite3.Connection) -> bool

    :param row_id:
    :param rule_id:
    :param connection:
    :return:
    """
    cursor = connection.cursor()
    connection.commit()


def update_rule(row_id, rulestring, connection):
    """(int, str, sqlite3.Connection) -> bool

    :param row_id:
    :param rulestring:
    :param connection:
    :return:
    """
    cursor = connection.cursor()
    connection.commit()


def update_rule_name(row_id, name, connection):
    """(int, str, sqlite3.Connection) -> bool

    :param row_id:
    :param name:
    :param connection:
    :return:
    """
    cursor = connection.cursor()
    connection.commit()

