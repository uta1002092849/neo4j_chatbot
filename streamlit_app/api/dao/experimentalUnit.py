class ExperimentalUnitDAO:

    def __init__(self, driver):
        self.driver = driver
    
    # get the unique ID of all experimental units
    def get_all_ids(self):
        def get_exp_units(tx):
            cypher = "MATCH (u:ExperimentalUnit) RETURN u as exp_units"
            result = tx.run(cypher)
            return [record["exp_units"]["expUnit_UID"] for record in result]
        
        with self.driver.session() as session:
            return session.execute_read(get_exp_units)

    # Get experimental unit information
    def get_exp_unit_info(self, expUnit_id):
            def get_exp_unit_info(tx):
                cypher = """MATCH (u:ExperimentalUnit {expUnit_UID: $expUnit_id})
                            RETURN
                                u.expUnit_UID AS ID,
                                u.expUnitChangeInManagement AS Description,
                                u.expUnitStartDate AS Start_Date,
                                u.expUnitEndDate AS End_Date,
                                u.expUnitSize AS Size,
                                u.fieldSlopePercent AS SlopePercent,
                                u.landscapePosition AS LandscapePosition"""
                result = tx.run(cypher, expUnit_id=expUnit_id)
                return result.to_df()
            
            with self.driver.session() as session:
                return session.execute_read(get_exp_unit_info)
    
    # get all treatments applied to an experimental unit
    def get_all_treatments(self, expUnit_id):
        
        def get_treatments(tx):
            cypher = """MATCH (u:ExperimentalUnit {expUnit_UID: $expUnit_id})<-[:appliedInExpUnit]-(t:Treatment)
                        RETURN
                            t.treatmentId AS ID,
                            t.treatmentDescriptor AS Name,
                            t.treatmentStartDate AS Start_Date,
                            t.treatmentEndDate AS End_Date
                        ORDER BY t.treatmentStartDate ASC"""
            result = tx.run(cypher, expUnit_id=expUnit_id)
            return result.to_df()
        
        with self.driver.session() as session:
            return session.execute_read(get_treatments)
    
    # get grain yield of an experimental unit over time
    def get_grain_yield(self, expUnit_id):
        def get_grain_yield(tx):
            cypher = """MATCH (u:ExperimentalUnit {expUnit_UID: $expUnit_id})-[:isHarvested]->(h:Harvest)
                        WHERE
                            h.harvestedGrainYield IS NOT NULL
                        RETURN
                            h.harvestDate AS Date,
                            h.harvestedGrainYield AS grainYield,
                            h.harvestedCrop AS crop
                        ORDER BY h.harvestDate ASC"""
            result = tx.run(cypher, expUnit_id=expUnit_id)
            return result.to_df()
        
        with self.driver.session() as session:
            return session.execute_read(get_grain_yield)
    
    # get soil carbon storage of an experimental unit over time
    def get_soil_carbon(self, expUnit_id):
        
        def get_soil_carbon(tx):
            cypher = """MATCH (u:ExperimentalUnit {expUnit_UID: $expUnit_id})-[:hasChemSample]->(s:SoilChemicalSample)
                        WHERE 
                            s.totalSoilCarbon IS NOT NULL
                        RETURN
                            s.soilChemLowerDepth as LowerDepth,
                            s.soilChemUpperDepth as UpperDepth,
                            s.soilChemDate as Date,
                            s.totalSoilCarbon as SoilCarbon
                        ORDER BY s.soilChemDate ASC"""
            result = tx.run(cypher, expUnit_id=expUnit_id)
            return result.to_df()
        
        with self.driver.session() as session:
            return session.execute_read(get_soil_carbon)
    
    # get soil physical properties of an experimental unit over time
    # ToDO: Need rework, right now it returns all the soil physical properties of an experimental unit, most of the value are NaN
    def get_soil_physical_properties(self, expUnit_id):
        
        def get_physical_properties(tx):
            cypher = """MATCH (u:ExperimentalUnit {expUnit_UID: $expUnit_id})-[:hasPhySample]->(s:SoilPhysicalSample)
                        RETURN
                            s
                        ORDER BY s.soilPhysDate ASC"""
            result = tx.run(cypher, expUnit_id=expUnit_id)
            return result.to_df()
        
        with self.driver.session() as session:
            return session.execute_read(get_physical_properties)
        
    
    # get soil Chemical properties of an experimental unit over time
    def get_soil_chemical_properties(self, expUnit_id):
        
        def get_chemical_properties(tx):
            cypher = """MATCH (u:ExperimentalUnit {expUnit_UID: $expUnit_id})-[:hasChemSample]->(s:SoilChemicalSample)
                        RETURN
                            s.soilChemDate as Date,
                            s.totalSoilCarbon as Carbon,
                            s.soilAmmonium as Ammonium,
                            s.soilNitrate as Nitrate,
                            s.soilPh as PH,
                            s.totalSoilNitrogen as Nitrogen,
                            s.soilChemLowerDepth as LowerDepth,
                            s.soilChemUpperDepth as UpperDepth
                        ORDER BY s.soilChemDate ASC"""
            result = tx.run(cypher, expUnit_id=expUnit_id)
            return result.to_df()
        
        with self.driver.session() as session:
            return session.execute_read(get_chemical_properties)
        