def chain(groq_api_key,create_chain,create_msg_history):
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

    chain = create_chain(groq_api_key,SYSTEM_TEMPLATE)

    messgage_history_chain,store = create_msg_history(chain)
    return messgage_history_chain,store
