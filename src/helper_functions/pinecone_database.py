from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredPDFLoader
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore

def create_pinecone_db(path,index_name,pc,embeddings):
    """
    Creates a Pinecone database from documents loaded from a specified path.

    Parameters:
    path (str): The path to the document file.
    index_name (str): The name of the Pinecone index to be created.
    pc (object): The Pinecone client instance.
    embeddings (object): The embeddings object used to create the Pinecone vector store.

    Returns:
    PineconeVectorStore: The created Pinecone vector store with the indexed documents.
    """

    # loader = CSVLoader(path)
    # loader = PyPDFLoader(path)
    loader = PyPDFLoader(path)
    documents = []
    for load in ([loader]):
        try:
            documents.extend(load.load())
        except Exception as e:
            print(f'Error in document loading (Currently in src/helper_functions/pinecone_database) with error {e}')

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    pc.create_index(
        name=index_name,
        dimension=1024,
        metric='cosine',
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    docsearch = PineconeVectorStore.from_documents(docs, embeddings, index_name=index_name)
    return docsearch
    
def load_existing_pinecone_db(index_name,pc,embeddings):
    """
    Loads an existing Pinecone database.

    Parameters:
    index_name (str): The name of the Pinecone index to be loaded.
    pc (object): The Pinecone client instance.
    embeddings (object): The embeddings object used to load the Pinecone vector store.

    Returns:
    PineconeVectorStore: The loaded Pinecone vector store.
    """
    
    docs = []
    docsearch = PineconeVectorStore.from_documents(docs, embeddings, index_name=index_name)
    return docsearch
