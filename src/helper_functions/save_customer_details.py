import os
import json
from typing import Optional
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

# Define a custom prompt to provide instructions and any additional context.
# 1) You can add examples into the prompt template to improve extraction quality
# 2) Introduce additional parameters to take context into account (e.g., include metadata
#    about the document from which the text was extracted.)
class Extract_Name(BaseModel):
    """Information about Menu Items."""
    customer_name: Optional[str] = Field(
        default=None, description="The full name of the customer")


def prompt_to_store_caller_detail(api_key):
    """
    Creates a prompt to extract customer details from a given text using the ChatGroq model.

    Parameters:
    api_key (str): The API key for accessing the Groq service.

    Returns:
    Runnable: A runnable object that processes the input text and extracts the customer details.
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert extraction algorithm. "
                "Only extract relevant information from the text. "
                "If you do not know the value of an attribute asked to extract or if you find the text empty, "
                "return null for the attribute's value",
            ),

            ("human", "{text}"),
        ]
    )


    llm = ChatGroq(temperature=0, model_name="llama3-70b-8192",api_key=api_key)

    runnable = prompt | llm.with_structured_output(schema=Extract_Name)

    return runnable




def save_details_in_json(phone_number,customer_detail):
    """
    Saves the customer details in a JSON file.

    Parameters:
    phone_number (str): The phone number of the customer.
    customer_detail (dict): The extracted customer details.

    Returns:
    None
    """

    print('------> Save details in json')
    filename = 'src/data/callers_info.json'

    full_name = dict(customer_detail)['customer_name']
    print(dict(customer_detail))

    if os.path.exists(filename):
        # If the file exists, load existing data
        with open(filename, 'r') as file:
            data = json.load(file)
    else:
        # If the file does not exist, initialize an empty structure
        data = {'phone_number': [], 'full_name': []}

    # Append new caller info if not already present
    if phone_number not in data['phone_number']:
        data['phone_number'].append(phone_number)
        data['full_name'].append(full_name)

    # Save the updated data back to the JSON file
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

    print(f'Saved caller info for name {full_name}')
def save_customer_detail(phone_number,session_id,api_key,menu_to_extract_text):
    # json_file_path = f'src/call_logs/{session_id}.json'
    # with open(json_file_path, 'r') as j:
    #     contents = json.loads(j.read())

    # menu_to_extract_text = ' '.join(contents['Human'][:2])
    print('------> Inside save_customer_detail_function')
    runnable = prompt_to_store_caller_detail(api_key)
    print(menu_to_extract_text)
    customer_detail = runnable.invoke({"text": menu_to_extract_text})

    save_details_in_json(phone_number,customer_detail)