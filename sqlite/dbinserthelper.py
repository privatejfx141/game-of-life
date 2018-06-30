import dbdriver as driver
import dbinserter as inserter
import dbselector as selector


def insert_pattern(name, rle, ptype, rulestring):
    """(str, str, str, str) -> int

    :param name: name of the pattern
    :param rle: pattern RLE
    :param ptype: pattern type
    :param rulestring: rule string
    :return: new row ID in pattern table
    """
    name = name.replace("\'", "\'\'")
    ptype = ptype.upper()
    connection = driver.connect_to_database()
    rule_id = selector.select_rule_id(rulestring, connection, by_rulestring=True)
    pattern_id = inserter.insert_pattern(name, rle, ptype, rule_id, connection)
    connection.close()
    return pattern_id


def insert_rule(name, rulestring):
    """(str, str) -> int

    :param name: name of the pattern
    :param rulestring: rule string
    :return: new row ID in rule table
    """
    name = name.replace("\'", "\'\'")
    connection = driver.connect_to_database()
    rule_id = inserter.insert_rule(name, rulestring, connection)
    connection.close()
    return rule_id


if __name__ == "__main__":
    pid = insert_pattern("Glider", "bob$2bo$3o!", "Spaceship", "B3/S23")
    print(pid)
