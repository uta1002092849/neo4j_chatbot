class GeneralDAO:

    def __init__(self, driver):
        self.driver = driver
    
    # get the unique ID of all experimental units
    def run_query(self, cypher_query):

        records, _, _ = self.driver.execute_query(cypher_query)
        results = [record.data() for record in records]
        return results
