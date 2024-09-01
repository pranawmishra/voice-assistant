# Import Guard and Validator
# from guardrails.hub import RestrictToTopic
from guardrails.hub.tryolabs.restricttotopic.validator import RestrictToTopic
from guardrails import Guard
import openai
import os

def restrict_topic_guardrail(message):
    """
    Validates if a given message falls within the specified valid topics using Guard's RestrictToTopic validator.

    Parameters:
    message (str): The message to be validated.

    Returns:
    bool: True if the message is within the valid topics, False otherwise.
    """
    
    # Setup Guard
    guard = Guard().use(
        RestrictToTopic(
            valid_topics=[
                "food", "restaurant", "cuisine", "dining", "recipes", "cooking", 
                "restaurants", "meals", "greeting", "hello", "hi", "good morning", 
                "good afternoon", "good evening", "Telling my name"
            ],
            invalid_topics=["sports", "music", "technology", "politics", "science", "health", "travel", "movies"],
            disable_classifier=False,
            disable_llm=True,
            on_fail="exception"
        )
    )

    try:
        value = guard.validate(message)  # Validator passes
        return value.validation_passed
    except Exception as e:
        return False

