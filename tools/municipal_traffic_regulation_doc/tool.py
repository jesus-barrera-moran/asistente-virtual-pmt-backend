import os
from uuid import UUID
from langchain.tools.retriever import create_retriever_tool
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

from services.files_storage import read_file

async def tool(id_pasteleria: UUID):
    id_pasteleria_str = str(id_pasteleria)
    folder_name = f"documents/{id_pasteleria_str}"
    os.makedirs(folder_name, exist_ok=True)

    file_data = read_file(
        id_pasteleria_str,
        "municipal_traffic_regulation"
    )

    file_content = "No existen procesos disponibles en la regulación de tráfico municipal."

    if file_data["content"]:
        try:
            file_content = file_data["content"].decode('utf-8')
        except UnicodeDecodeError:
            file_content = file_data["content"].decode('cp1252', errors='ignore')

    file_path = os.path.join(folder_name, f"{file_data['name']}.txt")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(file_content)

    loader = TextLoader(file_path, encoding='utf-8')
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(texts, embeddings)

    retriever = db.as_retriever()

    tool = create_retriever_tool(
        retriever,
        "municipal_traffic_regulation_doc",
        "Useful when you need to answer questions about traffic laws, penalties, and enforcement procedures.",
    )

    return tool
