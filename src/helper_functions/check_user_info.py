import json

def user_data():
    """
    Reads and returns the user data from a JSON file.

    The JSON file is expected to be located at 'src/data/callers_info.json'.
    
    Returns:
    dict: A dictionary containing user data.
    """

    with open('src/data/callers_info.json', 'r') as f:
        user_data = json.load(f)

    return user_data

def check_user_number(number):

    """
    Checks if a given phone number exists in the user data and returns the associated user's name.

    Parameters:
    number (str): The phone number to check.

    Returns:
    str: The full name of the user associated with the phone number if found, otherwise None.
    """
    
    data = user_data()
    if number in data['phone_number']:
        index_number = data['phone_number'].index(number)
        name = data['full_name'][index_number]
        return name
    return None

