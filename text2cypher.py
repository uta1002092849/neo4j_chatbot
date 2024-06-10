from langchain.chains import GraphCypherQAChain
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate

from langchain_community.vectorstores import Neo4jVector
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma

embeddings = OllamaEmbeddings(model="llama3")

from llm import llama3
from graph import graph

# references: https://python.langchain.com/v0.2/docs/how_to/graph_prompting/
# fewshot examples
examples = [
    {
        "question": "How to find average soil carbon?",
        "query": "MATCH (u:ExperimentalUnit)-[:hasChemSample]->(c:SoilChemicalSample) WHERE (c.totalSoilCarbon) IS NOT NULL AND NOT isNaN(c.totalSoilCarbon) RETURN u.expUnit_UID, (c.totalSoilCarbon) as averageSoilCarbonForTargetedUnit",
    },
    {
        "question": "How to compute the total number of experimental unit per treatment?",
        "query": "MATCH (u:Treatment)-[:appliedInExpUnit]->(e:ExperimentalUnit) RETURN u.treatmentDescriptor as treatment, count(e) AS numberOfExpUnit",
    },
    {
        "question": "How to compute the precipitation for a specific field over Q1, Q2, Q3, Q4?",
        "query": """MATCH (f:Field)<-[:weatherAtField]-(w:WeatherObservation)
WHERE f.fieldId = $neodash_field_fieldid_5
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
ORDER BY period"""
    },
    {
        "question": "How to get a list of experimental units located in a specific field?",
        "query": "MATCH (u:ExperimentalUnit)-[:locatedInField]->(f:Field) WHERE f.fieldId = $field_id RETURN u.expUnit_UID AS Experimental_unit"
    },
    {
        "question": "How to get soil property of a specific field?",
        "query": "MATCH (f:Field)<-[:appliedInField]-(s:Soil) WHERE f.fieldId = $field_id RETURN s.soilSeries"
    },
    {
        "question": "How get a list of research conducted on a specific filed?",
        "query": "MATCH path =(f:Field)<-[:hasField]-(s:Site)<-[:studiesSite]-(p:Publication) WHERE f.fieldId = $neodash_field_fieldid_5 RETURN p.publicationTitle as Title, p.publicationAuthor as Author, p.publicationDate as publicationDate, p.publicationIdentifier as Reference ORDER BY p.publicationDate"
    }
    # ToDo: add more examples that the model seems to struggle with
]

example_prompt = PromptTemplate.from_template(
    "User input: {question}\nCypher query: {query}"
)

example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    embeddings,
    Chroma(),
    k=5,
    input_keys=["question"],
)


prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix = "You are a Neo4j expert. Given an input question, create a syntactically correct Cypher query to run. Use only the provided relationship types and properties in the schema. For example, .\n Here is the schema information:\n{schema}\nBelow are a number of examples of questions and their corresponding Cypher queries.",
    suffix="User input: {question}\nCypher query: ",
    input_variables=["question", "schema"],
)


chain = GraphCypherQAChain.from_llm(
    llm=llama3,
    graph=graph,
    verbose=True,
    validate_cypher=True,
    cypher_prompt=prompt,
    return_intermediate_steps=True
)

def generate_cypher(prompt_text):
    try:
        response = chain.invoke({"query":prompt_text})
    except Exception as e:
        response = {"result": "Sorry, I can only answer questions related to the sockg dataset"}
    constructed_cypher = response['intermediate_steps'][0]['query']
    constructed_context = response['intermediate_steps'][1]['context']
    final_response = response['result']
    
    return {"constructed_cypher": constructed_cypher, "constructed_context": constructed_context, "final_response": final_response}
