from langchain_community.embeddings import OllamaEmbeddings

llama3_embeddings = OllamaEmbeddings(
    base_url='http://host.docker.internal:11434',
    model="llama3"
)