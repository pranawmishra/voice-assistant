from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import json

# Define a custom prompt to provide instructions and any additional context.
# 1) You can add examples into the prompt template to improve extraction quality
# 2) Introduce additional parameters to take context into account (e.g., include metadata
#    about the document from which the text was extracted.)

def prompt_to_store_order(Data,api_key):
    """
    Creates a prompt to extract ordered food items, quantities, and prices from a customer's final order text.

    Parameters:
    Data (dict): The schema to structure the output data.
    api_key (str): The API key for accessing the Groq service.

    Returns:
    Runnable: A runnable object that processes the input text and extracts the food order details.
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                '''You are a system that processes food orderss. Given a detailed text of a customer's final order, extract the ordered food items
                along with their quantaties and prices. Output the  result as a list of tuples where each tuple contains the food item name, the 
                total number of item, and their toal price

                
                Output format: [(food_item_1, quantity_1, total_price_1),(food_item_2, quantity_2, total_price_2),....]

                Example:
                Order: "The customer ordered one chicken wings for $5 and 2 margherita pizza for 12 dollars"
                Output: [('chicken wings', 1,5),('margherita pizza',2,12)]
                ''',
            ),
            # Please see the how-to about improving performance with
            # reference examples.
            # MessagesPlaceholder('examples'),
            ("human", "{text}"),
        ]
    )


    llm = ChatGroq(temperature=0, model_name="llama3-70b-8192",api_key=api_key)

    runnable = prompt | llm.with_structured_output(schema=Data)

    return runnable

def save_in_json(menu_items,session_id):
    """
    Saves the extracted menu items into a JSON file named after the session ID.

    Parameters:
    menu_items (object): The menu items to be saved.
    session_id (str): The session identifier for naming the JSON file.

    Returns:
    None
    """
    
    file_path = f'src/order_history/{session_id}.json'
    final_menu_items = []
    for item in (menu_items.Menu):
        final_menu_items.append(dict(item))


    menu_dictionary = {
    'menu_items': final_menu_items
    }

    with open(file_path, 'w') as file:
        json.dump(menu_dictionary, file,indent=4)
