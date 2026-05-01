import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

KNOWLEDGE_BASE_DIR = "./knowledge_base"
DB_DIR = "./chroma_db"

def setup_rag():
    print(f"Loading documents from {KNOWLEDGE_BASE_DIR}...")
    
    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        os.makedirs(KNOWLEDGE_BASE_DIR)
        print(f"Created {KNOWLEDGE_BASE_DIR}. Please add markdown/text files and run this script again.")
        return

    # Load markdown and text files
    loaders = [
        DirectoryLoader(KNOWLEDGE_BASE_DIR, glob="**/*.md", loader_cls=UnstructuredMarkdownLoader),
        DirectoryLoader(KNOWLEDGE_BASE_DIR, glob="**/*.txt", loader_cls=TextLoader)
    ]
    
    docs = []
    for loader in loaders:
        try:
            docs.extend(loader.load())
        except Exception as e:
            print(f"Error loading documents: {e}")
            
    if not docs:
        print("No documents found to ingest.")
        return

    print(f"Loaded {len(docs)} documents. Splitting text...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    print(f"Creating embeddings using Ollama (nomic-embed-text)...")
    try:
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory=DB_DIR)
        print(f"Successfully ingested {len(splits)} chunks into {DB_DIR}")
    except Exception as e:
        print(f"Error creating vector store: {e}\nMake sure Ollama is running and 'nomic-embed-text' is pulled.")

if __name__ == "__main__":
    setup_rag()
