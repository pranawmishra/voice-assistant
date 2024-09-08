from langchain_community.document_loaders import PyPDFLoader
from langchain_qdrant import QdrantVectorStore
from langchain_core.documents import Document
import os
import pandas as pd

class QdrantDatabase:
    def __init__(self, url, qdrant_api_key, embeddings,qdrant_client):
        self.url = url
        self.qdrant_api_key = qdrant_api_key
        self.embeddings = embeddings
        self.qdrant_client = qdrant_client

    @staticmethod
    def csv_to_document(filepath):
        df = pd.read_csv(filepath)
        documents = []
        for index, row in df.iterrows():
            text = f"Dish Category: {row['Dish Category']} \n Dish Name: {row['Dish Name']} \n Price: {row['Price']} \n Dish Details: {row['Dish Detail']} \n"
            documents.append(Document(page_content=text, metadata={'filepath': filepath,
                                                                'Row': index+1}))
        
        return documents

    def create_collection(self,collection_name):
        file_folder = 'sample_file'
        file = os.listdir(file_folder)[0]
        file_path  = file_folder+'/'+file
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.csv':
            documents = self.csv_to_document(file_path)
        elif ext == '.pdf':
            loader = PyPDFLoader(file_path)

        
            documents = []
            for load in ([loader]):
                try:
                    documents.extend(load.load())
                except Exception as e:
                    print(f'Error in document loading (Currently in src/helper_functions/pinecone_database) with error {e}')

        qdrant = QdrantVectorStore.from_documents(documents,
                                                self.embeddings,
                                                url=self.url,
                                                api_key=self.qdrant_api_key,
                                                collection_name=collection_name)
        
        print(f"Collection {collection_name} created successfully.")
        vector_store = QdrantVectorStore(
                    client=self.qdrant_client,
                    collection_name=collection_name,
                    embedding=self.embeddings
                )
        retriever = vector_store.as_retriever()
        print('Retriever retrieved successfully')
        return retriever

    def query_collection(self,collection_name):
        try:
            if self.qdrant_client.get_collection(collection_name):
                print('Collection name exists!!')
                vector_store = QdrantVectorStore(
                    client=self.qdrant_client,
                    collection_name=collection_name,
                    embedding=self.embeddings
                )
                retriever = vector_store.as_retriever()
                return retriever
        except Exception as e:
            print(f'Wrong collection name {e}')
            return None


