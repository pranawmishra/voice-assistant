import os
from src.helper_functions.retrieve_queries import retreive_queries
from src.helper_functions.save_call_history import save_call_history
from src.helper_functions.restaurant_index_manager import index_manager
from src.helper_functions.order_processing_and_storage import prompt_to_store_order, save_in_json
from src.helper_functions.save_customer_details import save_customer_detail
from src.helper_functions.restaurant_order_assistant import chain
from src.helper_functions.store_session_memory import create_msg_history
from src.helper_functions.pinecone_database import create_pinecone_db,load_existing_pinecone_db
from src.config.secrets import ConfigurationManager
from src.helper_functions.speak_deepgram import speak_deepgram
from src.helper_functions.create_order import Data
from src.helper_functions.save_order_history import save_order_history
from langchain_cohere import CohereEmbeddings
from src.helper_functions.qdrant_database import QdrantDatabase
from qdrant_client import QdrantClient
from langchain_core.documents import Document
import cohere

config_manager = ConfigurationManager()
os.environ['COHERE_API_KEY'] = config_manager.cohere_api_key


embeddings = CohereEmbeddings(model='embed-english-light-v3.0')
qdrant_client = QdrantClient(
    url = config_manager.url,
    api_key=config_manager.qdrant_api_key
)
qdrant_database = QdrantDatabase(config_manager.url,
                                 config_manager.qdrant_api_key,
                                 embeddings,
                                 qdrant_client)
# session_id = f'Pid_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
cohere_client = cohere.Client(config_manager.cohere_api_key)
session_id = '002'
message_history_chain,store = chain(config_manager.groq_api_key,create_msg_history)


def main(session_id,retriever,message_history_chain, question):
    """
    Main function to process a given question, retrieve related content, save call history, and generate speech.

    Parameters:
    session_id (str): The session identifier.
    retriever (object): The retriever object used to fetch related queries.
    message_history_chain (object): The message history chain object.
    question (str): The question to be processed.

    Returns:
    tuple: A tuple containing:
        - question (str): The original question.
        - ai_content (dict): The retrieved AI content.
        - content (str): The content extracted from the AI response.
        - mp3_file (str): The path to the generated MP3 file (if not using Twilio's text-to-speech).

    """
    print(question)
    relevant_content = retriever.invoke(question)
    page_contents = [doc.page_content for doc in relevant_content]
    rerank_response = cohere_client.rerank(query=question,documents = page_contents, model = 'rerank-english-v3.0',return_documents=True)
    # print(rerank_response)
    reranked_result = []
    relevant_documents = []
    for item in rerank_response.results:
        original_doc = item.document.text
        reranked_doc = Document(page_content=original_doc)
        relevant_documents.append(reranked_doc)
        reranked_result.append({
            'index':item.index,
            'relevance_score':item.relevance_score,
            'document':item.document.text
        })
    
    ai_content, content= retreive_queries(question,relevant_documents,session_id,message_history_chain)
    
    
    # content = dict(ai_content)['content']
    
    # save_call_history(session_id,content,question)

    # SPEAK_OPTIONS = {"text": content}
    # mp3_file = speak_deepgram(deepgram_api_key,SPEAK_OPTIONS,'output.wav') # need to comment out the line if we are using twilio inbuilt text to speech

    return relevant_documents,ai_content,content #,mp3_file #need to comment mp3_file to use twilio speech to text



# Retrieve all collections
collections = qdrant_client.get_collections()

# Extract the names of the collections
existing_indexes = [collection.name for collection in collections.collections]
print('Hi following is the list of indexes we have: ')
print(existing_indexes)
index_name = input('Which index do you want to connect to? Else if this is a new index please provide the new index name here: ')

if index_name in existing_indexes:
    index_exist = True
    print('Index exists')
    retriever = qdrant_database.query_collection(index_name)
else:
    print('Index does not exists')
    retriever = qdrant_database.create_collection(index_name)



prev_ques = []
while True:

    question = input('Enter your question: ')
    if question=='exit()':
        break
    else:
        retrieved_docs = (retriever.invoke(question))
        relevant_documents,ai_content, content = main(session_id,retriever, message_history_chain, question)
        print('Answer:',content)
        print('Retrieved documents type',type(retrieved_docs))
        for i, doc in enumerate(relevant_documents):
            # print('Page COntent')
            # print(i,doc.page_content)
            print('------------------------------------')
            print('Docs')
            print(doc)
            print(type(doc))
        print('-----------------------------------')


