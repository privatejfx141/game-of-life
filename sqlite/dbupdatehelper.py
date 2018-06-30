import dbdriver as driver
import dbupdater as updater


def update_pattern(row_id, new_rle):
    connection = driver.connect_to_database()
    result = updater.update_pattern(row_id, new_rle, connection)
    connection.close()
    return result


def update_pattern_name(row_id, new_name):
    connection = driver.connect_to_database()
    result = updater.update_pattern_name(row_id, new_name, connection)
    connection.close()
    return result


def update_pattern_type(row_id, new_type):
    connection = driver.connect_to_database()
    result = updater.update_pattern_type(row_id, new_type, connection)
    connection.close()
    return result


def update_pattern_rule(row_id, new_rule):
    connection = driver.connect_to_database()
    result = updater.update_pattern_rule(row_id, new_rule, connection)
    connection.close()
    return result


def update_rule(row_id, new_rulestring):
    connection = driver.connect_to_database()
    result = updater.update_rule(row_id, new_rulestring, connection)
    connection.close()
    return result


def update_rule_name(row_id, new_name):
    connection = driver.connect_to_database()
    result = updater.update_rule_name(row_id, new_name, connection)
    connection.close()
    return result
