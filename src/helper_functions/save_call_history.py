import json
import os
def save_call_history(session_id,content,question):
    """
    Saves the call history, including the human question and AI-generated content, to a JSON file.

    Parameters:
    session_id (str): The session identifier.
    content (str): The AI-generated content.
    question (str): The human question.

    Returns:
    None
    """
    
    # Specify the path to the JSON file
    file_path = f'src/call_logs/{session_id}.json'

    # Check if the file exists
    if not os.path.exists(file_path):
        # If the file does not exist, create it with some initial data
        initial_data = {
            'Human': [],
            'Agent':[]
        }
        initial_data['Agent'].append(content)
        initial_data['Human'].append(question)
        with open(file_path, 'w') as file:
            json.dump(initial_data, file)
        print("JSON file was created.")
    else:
        print("JSON file already exists.")
        with open(file_path, 'r') as file:
            data = json.load(file)
            
            # Update the data
            data['Agent'].append(content)
            data['Human'].append(question)

            # Save the updated data
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
