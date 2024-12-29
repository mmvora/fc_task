# from langchain_openai import OpenAI
from langchain_ollama.llms import OllamaLLM
from langchain_community.graphs import Neo4jGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fc_task.config import load_db_url, get_neo4j_creds
from fc_task.article_model import Article

llm = OllamaLLM(model="llama3.2")

llm_transformer = LLMGraphTransformer(
    llm=llm,
)

neo4j_creds = get_neo4j_creds()
url = neo4j_creds["url"]
user = neo4j_creds["user"]
password = neo4j_creds["password"]

def extract_relations() -> None:
    documents: list[Document] = []
    engine = create_engine(load_db_url())

    with Session(engine) as session:
        for article in session.query(Article).all():
            documents.append(Document(page_content=article.ai_summary))

    graph_documents = llm_transformer.convert_to_graph_documents(documents)
    print(f"Nodes:{graph_documents[0].nodes}")
    print(f"Relationships:{graph_documents[0].relationships}")

    
    graph = Neo4jGraph(url=url, username=user, password=password, enhanced_schema=True)
    graph.add_graph_documents(graph_documents)


if __name__ == "__main__":
    extract_relations()
