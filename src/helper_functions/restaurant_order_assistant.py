from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def create_chain(groq_api_key,SYSTEM_TEMPLATE,model):
    """
    Creates a question-answering chain using ChatGroq and a custom prompt template.

    This function initializes a ChatGroq instance with specified parameters and
    constructs a question-answering prompt template. It then combines the prompt
    template and the ChatGroq instance into a processing chain for handling
    question-answering tasks.

    Parameters:
    groq_api_key (str): The API key for accessing the ChatGroq service.
    SYSTEM_TEMPLATE (str): A Role and set of instruction that the LLM should following while giving out the answer

    Returns:
    chain (Pipeline): A processing chain that takes in user input and chat history
                      to generate responses based on the custom prompt template
                      and ChatGroq model.
    """
    
    chat = ChatGroq(temperature=0, model_name=model,api_key=groq_api_key)

    question_answering_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                SYSTEM_TEMPLATE,
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )

    chain = question_answering_prompt | chat

    return chain

def chain(groq_api_key:str,create_msg_history,model:str):
    """
    Creates a message history chain for a polite restaurant staff assistant.

    This function sets up a system template for the assistant's behavior and uses it to create a chain.
    It then initializes a message history chain with the given chain.

    Parameters:
    groq_api_key (str): The API key for accessing the Groq service.
    create_chain (function): The function to create the initial chain with the given template.
    create_msg_history (function): The function to create the message history chain.

    Returns:
    tuple: A tuple containing:
        - messgage_history_chain (object): The initialized message history chain.
        - store (dict): The store containing message histories by session ID.
    """

    SYSTEM_TEMPLATE ="""you are helpful assistant who help user in answering questions that is asked to you from provided context
                        {context}
                        """

    chain = create_chain(groq_api_key,SYSTEM_TEMPLATE,model)

    messgage_history_chain,store = create_msg_history(chain)
    return messgage_history_chain,store
