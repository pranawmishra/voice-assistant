from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
import pickle
from langchain_openai import OpenAIEmbeddings
vector_db_path = 'data/vector_db.pkl'

def create_vector_db(api_key,path):
    """
    Loads documents from a CSV file and returns them.

    Parameters:
    api_key (str): The API key for accessing necessary services (not used in this function).
    path (str): The path to the CSV file.

    Returns:
    list: A list of loaded documents.
    """
    
    loader = CSVLoader(path)
    documents = []
    for load in ([loader]):
        try:
            documents.extend(load.load())
        except:
            pass

    return documents

def return_vector_store(documents,api_key):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    all_splits = text_splitter.split_documents(documents)
    vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings(api_key=api_key))
    return vectorstore
