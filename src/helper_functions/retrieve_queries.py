def retreive_queries(question,retriever,session_id,messgae_history_chain):
    """
    Retrieves AI-generated content based on a given question using a retriever and message history chain.

    Parameters:
    question (str): The question to be processed.
    retriever (object): The retriever object used to fetch related queries.
    session_id (str): The session identifier.
    message_history_chain (object): The message history chain object.

    Returns:
    dict: A dictionary of AI-generated content with other metadata
    str: The AI-generated content.
    """

    ai_content = messgae_history_chain.invoke(
        {"input": question,
        "context": retriever.invoke(question)},
        {"configurable": {"session_id": session_id}},
    )

    content = dict(ai_content)['content']
    return ai_content,content