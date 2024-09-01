import pickle

def serialize_retriever(retriever):
    """
    Serializes a retriever object using pickle.

    Parameters:
    retriever (object): The retriever object to be serialized.

    Returns:
    bytes: The serialized retriever object.
    """

    return pickle.dumps(retriever)

def deserialize_retriever(serialized_retriever):
    """
    Deserializes a retriever object from its serialized form using pickle.

    Parameters:
    serialized_retriever (bytes): The serialized retriever object.

    Returns:
    object: The deserialized retriever object.
    """
    
    return pickle.loads(serialized_retriever)
