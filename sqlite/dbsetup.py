import dbdriver as driver
import dbinserter as inserter


def setup_database():
    connection = driver.initialize_database()
    # insert common rules
    inserter.insert_rule("Conway\'\'s Life", "B3/S23", connection)
    inserter.insert_rule("Replicator", "B1357/S1357", connection)
    inserter.insert_rule("Fredkin", "B1357/S02468", connection)
    inserter.insert_rule("Seeds", "B2/S", connection)
    inserter.insert_rule("Live Free or Die", "B2/S0", connection)
    inserter.insert_rule("Life without Death", "B3/S012345678", connection)
    inserter.insert_rule("Flock", "B3/S12", connection)
    inserter.insert_rule("Maze", "B3/S12345", connection)
    inserter.insert_rule("Mazectric", "B3/S1234", connection)
    inserter.insert_rule("2x2", "B36/S125", connection)
    inserter.insert_rule("HighLife", "B36/S23", connection)
    inserter.insert_rule("Move", "B368/S245", connection)
    inserter.insert_rule("Day & Night", "B3678/S34678", connection)
    inserter.insert_rule("DryLife", "B37/S23", connection)
    inserter.insert_rule("Pedestrian Life", "B38/S23", connection)
    # close connection
    connection.close()


if __name__ == "__main__":
    setup_database()
