from langchain.chains import GraphCypherQAChain
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate

from llm import llm
from graph import graph

# ToDo: add dynamic fewshot once get access to OPenAI embedding model
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
        "question": "How to compute the total number of experimental unit per treatment?",
        "query": "MATCH (u:Treatment)-[:appliedInExpUnit]->(e:ExperimentalUnit) RETURN u.treatmentDescriptor as treatment, count(e) AS numberOfExpUnit",
    },
    # ToDo: add more examples that the model seems to struggle with
]

example_prompt = PromptTemplate.from_template(
    "User input: {question}\nCypher query: {query}"
)

prompt = FewShotPromptTemplate(
    examples=examples[:10],     # to reduce context size
    example_prompt=example_prompt,
    prefix = "You are a Neo4j expert. Given an input question, create a syntactically correct Cypher query to run. Use only the provided relationship types and properties in the schema. For example, .\n Here is the schema information:\n{schema}\nBelow are a number of examples of questions and their corresponding Cypher queries.",
    suffix="User input: {question}\nCypher query: ",
    input_variables=["question", "schema"],
)


chain = GraphCypherQAChain.from_llm(
    llm,
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
