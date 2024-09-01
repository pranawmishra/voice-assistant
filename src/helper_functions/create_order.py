from typing import Optional,List

from langchain_core.pydantic_v1 import BaseModel, Field


class Menu(BaseModel):
    """Information about Menu Items."""

    # ^ Doc-string for the entity Person.
    # This doc-string is sent to the LLM as the description of the schema Person,
    # and it can help to improve extraction results.

    # Note that:
    # 1. Each field is an `optional` -- this allows the model to decline to extract it!
    # 2. Each field has a `description` -- this description is used by the LLM.
    # Having a good description can help improve extraction results.
    dish_name: Optional[str] = Field(
        default=None, description="The dish ordered by customer")
    
    dish_quantity: Optional[str] = Field(
        default=None, description="The total no. of times the dish was ordered")
    
    dish_price: Optional[str] = Field(
        default=None, description="give price ony if available in the order else give Not Available")
    
    dish_modification:Optional[str] = Field(
        default=None, description='give any modification in dish made by customer in the order else give Not Available')
    


class Data(BaseModel):
    """Extracted data about people."""

    # Creates a model so that we can extract multiple entities.
    Menu: List[Menu]