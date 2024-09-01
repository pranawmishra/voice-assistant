import os 
def index_manager(pc,embeddings,create_pinecone_db,load_existing_pinecone_db,index_name,index_exist):
    """
    Manages the indexing of restaurant documents in a Pinecone database.

    If the restaurant index does not exist, it creates a new index using the provided document path.
    If the restaurant index already exists, it loads the existing index.

    Parameters:
    restaurant_num (str): The restaurant identifier number.
    pc (object): The Pinecone client instance.
    embeddings (object): The embeddings object used to create/load the Pinecone vector store.
    create_pinecone_db (function): The function to create a new Pinecone database.
    load_existing_pinecone_db (function): The function to load an existing Pinecone database.

    Returns:
    object: A retriever object for querying the Pinecone database.
    """
    
    # existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
    pdf_folder = 'sample_file'
    pdf_file = os.listdir(pdf_folder)[0]
    # index_name = 'index001'
    pdf_path = pdf_folder+'/'+pdf_file
    # if index_name not in existing_indexes:
    if index_exist==False:
        print('Creating Index....')
        docsearch = create_pinecone_db(pdf_path,index_name,pc,embeddings)
        index = pc.Index(index_name)
        retriever = docsearch.as_retriever()
        return retriever
    else:
        index = pc.Index(index_name)
        docsearch = load_existing_pinecone_db(index_name,pc,embeddings)
        retriever = docsearch.as_retriever()
        return retriever