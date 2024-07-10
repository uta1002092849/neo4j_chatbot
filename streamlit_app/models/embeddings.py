from langchain_community.embeddings import OllamaEmbeddings

llama3_embeddings = OllamaEmbeddings(
    base_url='http://llama3:11434',
    model="llama3"
)