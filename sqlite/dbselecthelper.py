import dbdriver as driver
import dbselector as selector


def select_pattern_id(search_str, by_rle=False):
    if not by_rle:
        search_str = search_str.replace("\'", "\'\'")
    connection = driver.connect_to_database()
    pattern_id = selector.select_pattern_id(search_str, connection, by_rle)
    connection.close()
    return pattern_id


def select_pattern_info(row_id):
    connection = driver.connect_to_database()
    pattern_info = selector.select_pattern_info(row_id, connection)
    connection.close()
    return pattern_info


def select_rule_id(search_str, by_rulestring=False):
    if not by_rulestring:
        search_str = search_str.replace("\'", "\'\'")
    connection = driver.connect_to_database()
    rule_id = selector.select_rule_id(search_str, connection, by_rulestring)
    connection.close()
    return rule_id


def select_rule_info(row_id):
    connection = driver.connect_to_database()
    rule_info = selector.select_rule_info(row_id, connection)
    connection.close()
    return rule_info


if __name__ == "__main__":
    rule = select_rule_info(select_rule_id("Conway's Life"))
    print(rule)
