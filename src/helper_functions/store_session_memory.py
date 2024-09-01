from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain.memory import ChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
import os
import json

store = {}

def get_by_session_id(session_id):
    """
    Retrieves the chat message history for a given session ID.

    Parameters:
    session_id (str): The session identifier.

    Returns:
    ChatMessageHistory: The chat message history for the given session ID.
    """

    if session_id not in store:
        store[session_id] = ChatMessageHistory()

    return store[session_id]



def create_msg_history(chain):
    """
    Creates a chain with message history functionality.

    Parameters:
    chain (object): The chain object to be wrapped with message history.

    Returns:
    tuple: A tuple containing:
        - chain_with_message_history (RunnableWithMessageHistory): The chain wrapped with message history.
        - store (dict): The store containing message histories by session ID.
    """

    chain_with_message_history = RunnableWithMessageHistory(
        chain,
        get_by_session_id,
        input_messages_key="input",
        history_messages_key="chat_history",
    )
    return chain_with_message_history,store

def save_chat_history(file_path,new_data):
    """
    Saves the chat history to a JSON file.

    Parameters:
    file_path (str): The path to the JSON file where the chat history will be saved.
    new_data (dict): The new data to be added to the chat history.

    Returns:
    None
    """
    
    if os.path.exists(file_path):
        with open(file_path,'r') as file:
            try:
                data = json.load(file)
            except (json.JSONDecodeError,FileNotFoundError):
                data = {}

    else:
        data = {}

    data.update(new_data)

    with open(file_path,'w') as file:
        json.dump(data,file,indent=4)
