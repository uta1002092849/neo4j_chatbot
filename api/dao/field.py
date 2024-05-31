import pandas as pd

class FieldDAO:

    def __init__(self, driver):
        self.driver = driver
    
    # get the unique ID of all experimental units
    def get_all_ids(self):
        # transaction function
        def get_exp_units(tx):
            cypher = "MATCH (f:Field) RETURN f as field"
            result = tx.run(cypher)
            return [record["field"]['fieldId'] for record in result]
        
        # execute transaction
        with self.driver.session() as session:
            return session.execute_read(get_exp_units)
    
    
    # get latitude and longitude of a field
    def get_lat_long_dataframe(self, field_id):
        # transaction function
        def get_lat_long(tx):
            cypher = "MATCH (f:Field {fieldId: $field_id}) RETURN f.fieldLatitude as latitude, f.fieldLongitude as longitude"
            result = tx.run(cypher, field_id=field_id)
            return result.single()
        
        # execute transaction
        with self.driver.session() as session:
            result = session.execute_read(get_lat_long)
            longtitue = result['longitude']
            latitude = result['latitude']
            df = pd.DataFrame({
                'latitude': [latitude],
                'longitude': [longtitue]
            })
            return df
    
    # get rainfall data of a field
    def get_rainfall_df(self, field_id):

        # transaction function
        def get_rainfall(tx):
            cypher = """MATCH (f:Field {fieldId: $field_id})<-[:weatherAtField]-(w:WeatherObservation)
                        WITH w.weatherObservationDate AS date, w.precipitation AS precipitation
                        WITH date, precipitation,
                            toInteger(substring(date, 0, 4)) AS year,
                            toInteger(substring(date, 5, 2)) AS month
                        WITH year,
                            CASE
                                WHEN month IN [1, 2, 3] THEN 'Q1'
                                WHEN month IN [4, 5, 6] THEN 'Q2'
                                WHEN month IN [7, 8, 9] THEN 'Q3'
                                ELSE 'Q4'
                            END AS quarter,
                            precipitation
                        WITH year + '-' + quarter AS period, SUM(precipitation) AS totalPrecipitation
                        RETURN period, round(totalPrecipitation, 3) AS totalPrecipitation
                        ORDER BY period ASC"""
            result = tx.run(cypher, field_id=field_id)
            date = []
            precipitation = []
            
            for record in result:
                date.append(record['period'])
                precipitation.append(record['totalPrecipitation'])
            return date, precipitation
        
        # execute transaction
        with self.driver.session() as session:
            date, precipitation = session.execute_read(get_rainfall)
            df = pd.DataFrame({
                'period': date,
                'totalPrecipitation': precipitation
            })
            return df
            
    # get all experimental units in a field
    def get_all_experimental_unit(self, field_id):
        # transaction function
        def get_exp_units(tx):
            cypher = """MATCH (f:Field {fieldId: $field_id})<-[:locatedInField]-(u:ExperimentalUnit)
                        RETURN u.expUnit_UID as id"""
            result = tx.run(cypher, field_id=field_id)
            return [record["id"] for record in result]
        
        # execute transaction
        with self.driver.session() as session:
            fields =  session.execute_read(get_exp_units)

            # create df
            df = pd.DataFrame(fields)
            return df
