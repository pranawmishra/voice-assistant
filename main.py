from src.helper_functions.retrieve_queries import retreive_queries
from src.config.secrets import deepgram_api_key
from src.helper_functions.speak_deepgram import speak_deepgram
from src.helper_functions.save_call_history import save_call_history
from src.helper_functions.restaurant_index_manager import index_manager
from datetime import datetime
from src.helper_functions.create_chain import create_chain
from src.helper_functions.order_processing_and_storage import prompt_to_store_order, save_in_json
from src.helper_functions.save_customer_details import save_customer_detail
from src.helper_functions.restaurant_order_assistant import chain
from src.helper_functions.store_session_memory import create_msg_history
from src.helper_functions.pinecone_database import create_pinecone_db,load_existing_pinecone_db
from src.config.secrets import deepgram_api_key,groq_api_key,together_api_key,pinecone_api_key
from src.helper_functions.speak_deepgram import speak_deepgram
from src.helper_functions.create_order import Data
from src.helper_functions.save_order_history import save_order_history
from pinecone import Pinecone
from langchain_together import TogetherEmbeddings
import os
os.environ['PINECONE_API_KEY'] = pinecone_api_key
os.environ['TOGETHER_API_KEY'] = together_api_key
pc = Pinecone() 
embeddings = TogetherEmbeddings(
    model="togethercomputer/m2-bert-80M-8k-retrieval",
)
# Generate a random secret key
# You can make this longer for additional security

session_id = f'Pid_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
message_history_chain,store = chain(groq_api_key,create_chain,create_msg_history)


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
    
    ai_content, content= retreive_queries(question,retriever,session_id,message_history_chain)
    
    
    # content = dict(ai_content)['content']
    
    save_call_history(session_id,content,question)

    # SPEAK_OPTIONS = {"text": content}
    # mp3_file = speak_deepgram(deepgram_api_key,SPEAK_OPTIONS,'output.wav') # need to comment out the line if we are using twilio inbuilt text to speech

    return question, ai_content,content #,mp3_file #need to comment mp3_file to use twilio speech to text



existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
print('Hi following is the list of indexes we have: ')
print(existing_indexes)
index_name = input('Which index do you want to connect to? Else if this is a new index please provide the new index name here: ')

if index_name in existing_indexes:
    index_exist = True
    retriever = index_manager(pc,embeddings,create_pinecone_db,load_existing_pinecone_db,index_name,index_exist=True)
else:
    retriever = index_manager(pc,embeddings,create_pinecone_db,load_existing_pinecone_db,index_name,index_exist=False)



while True:

    question = input('Enter your question: ')
    if question=='exit()':
        break
    else:
        question, ai_content, content = main(session_id,retriever, message_history_chain, question)
        print(f'Question: {question}')
        # print(f'AI Content: {ai_content}')
        print(f'Content: {content}')
        # print(f'MP3 File: {mp3_file}')
        print('-----------------------------------')


