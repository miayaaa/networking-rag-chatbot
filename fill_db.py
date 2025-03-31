from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb

# Setup the environment

DATA_PATH = r"data"
CHROMA_PATH = r"chroma_db"

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_or_create_collection(name='networkperformance')

# Loading the document

loader = PyPDFDirectoryLoader(DATA_PATH)

raw_documents = loader.load()

# Splitting the document so that it's easier to access

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=250,
    length_function=len,
    is_separator_regex=False,
)

chunks = text_splitter.split_documents(raw_documents)

# Preparing for the chunks to be added to ChromaDB

documents = []
metadata = []
ids = []

i = 0

for chunk in chunks:
    documents.append(chunk.page_content)
    ids.append("ID"+str(i))
    metadata.append({
        # Add source file info
        "source": chunk.metadata.get("source", "unknown"),
        # Add document section or category
        "section": chunk.metadata.get("section", "general"),
    })
    i += 1

collection.upsert(
    documents=documents,
    metadatas=metadata,
    ids=ids
)
