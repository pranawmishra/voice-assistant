import azure.cognitiveservices.speech as speechsdk
import datetime

def from_mic(SPEECH_KEY,SPEECH_REGION):
    """
    Recognizes speech from the microphone using Azure Cognitive Services and returns the transcribed text and duration.

    Parameters:
    SPEECH_KEY (str): The subscription key for Azure Cognitive Services.
    SPEECH_REGION (str): The region associated with the Azure Cognitive Services account.

    Returns:
    tuple: A tuple containing:
        - result.text (str): The transcribed text from the speech input.
        - duration (datetime.timedelta): The time taken to perform the speech recognition.
    """
    
    t1 = datetime.datetime.now()
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Speak into your microphone.")
    result = speech_recognizer.recognize_once_async().get()
    t2 = datetime.datetime.now()
    return (result.text, t2-t1)