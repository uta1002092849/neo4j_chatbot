from neo4j import GraphDatabase

def init_driver(uri, user, password):

    driver =  GraphDatabase.driver(uri, auth=(user, password))

    driver.verify_connectivity()

    return driver

def close_driver(driver):
    if driver is not None:
        driver.close()
        return True
    else:
        return False
