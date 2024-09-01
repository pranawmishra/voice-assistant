from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def create_chain(groq_api_key,SYSTEM_TEMPLATE):
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
    
    chat = ChatGroq(temperature=0, model_name="llama3-70b-8192",api_key=groq_api_key)

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