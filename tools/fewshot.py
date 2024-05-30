from langchain.chains import GraphCypherQAChain
from langchain.prompts.prompt import PromptTemplate

from llm import llm
from graph import graph


CYPHER_GENERATION_TEMPLATE = """
You are an expert Neo4j Developer translating user questions into Cypher to answer questions about sockg dataset and provide informations.
Convert the user's question based on the schema.

Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Do not be picky about the exact wording of the context

Fine Tuning:
ALWAYS USED AS TO RENAME THE COLUMN NAME TO THE EXPECTED OUTPUT NAME SPECIFIED IN THE QUESTION.
For example, never return count(u) as count, always return count(u) as totalNumberOfExperimentalUnits

Example Cypher Statements:

1. How to find average soil carbon?
MATCH (u:ExperimentalUnit)-[:hasChemSample]->(c:SoilChemicalSample)
WHERE (c.totalSoilCarbon) IS NOT NULL AND NOT isNaN(c.totalSoilCarbon)
RETURN u.expUnit_UID, (c.totalSoilCarbon) as averageSoilCarbonForTargetedUnit

2. How to compute total number of experimental units?
MATCH (u:ExperimentalUnit)
RETURN count(u) as totalNumberOfExperimentalUnits

Schema:
{schema}

Question:
{question}
"""

cypher_prompt = PromptTemplate.from_template(CYPHER_GENERATION_TEMPLATE)
cypher_qa = GraphCypherQAChain.from_llm(
    llm,
    graph=graph,
    verbose=True,
    cypher_prompt=cypher_prompt
)