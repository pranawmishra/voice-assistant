import json

def save_order_history(session_id,prompt_to_store_order,save_in_json,Data,groq_api_key):
    """
    Extracts order details from the session logs and saves the order history in a JSON file.

    Parameters:
    session_id (str): The session identifier.
    prompt_to_store_order (function): The function to create a prompt for extracting order details.
    save_in_json (function): The function to save the extracted order details in a JSON file.
    Data (dict): The schema to structure the extracted data.
    groq_api_key (str): The API key for accessing the Groq service.

    Returns:
    None
    """
    
    print('Entering save_order_history()')
    json_file_path = f'src/call_logs/{session_id}.json'
    with open(json_file_path, 'r') as j:
        contents = json.loads(j.read())

    menu_to_extract_text = ' '.join(contents['Agent'])

    runnable = prompt_to_store_order(Data,groq_api_key)

    menu_items = runnable.invoke({"text": menu_to_extract_text})
    print('Exiting save_order_history()')

    save_in_json(menu_items,session_id)