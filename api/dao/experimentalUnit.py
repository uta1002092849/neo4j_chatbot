class ExperimentalUnitDAO:

    def __init__(self, driver):
        self.driver = driver
    
    # get the unique ID of all experimental units
    def all(self):

        def get_exp_units(tx):
            cypher = "MATCH (u:ExperimentalUnit) RETURN u as exp_units"
            result = tx.run(cypher)
            return [record["exp_units"] for record in result]
        
        with self.driver.session() as session:
            return session.execute_read(get_exp_units)
