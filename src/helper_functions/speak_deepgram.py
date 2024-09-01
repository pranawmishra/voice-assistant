import os
from dotenv import load_dotenv
from pydub import AudioSegment

from deepgram import (
    DeepgramClient,
    SpeakOptions,
)


def speak_deepgram(deepgram_api_key,SPEAK_OPTIONS,filename):
    """
    Uses Deepgram to convert text to speech, saves the audio as a WAV file, converts it to MP3, and removes the WAV file.

    Parameters:
    deepgram_api_key (str): The API key for accessing the Deepgram service.
    SPEAK_OPTIONS (dict): Options for the speech synthesis, including the text to convert to speech.
    filename (str): The name of the output file (without path).

    Returns:
    str: The name of the generated MP3 file if successful, otherwise 'did_not_hear.mp3'.
    """
    
    path = 'static'
    try:
        # STEP 1: Create a Deepgram client using the API key from environment variables
        deepgram = DeepgramClient(api_key=deepgram_api_key)

        # STEP 2: Configure the options (such as model choice, audio configuration, etc.)
        options = SpeakOptions(
            model="aura-asteria-en",
            encoding="linear16",
            container="wav"
        )

        # STEP 3: Call the save method on the speak property
        print('saving as wav file')
        response = deepgram.speak.v("1").save(f'static/{filename}', SPEAK_OPTIONS, options)
        print(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")
    static_folder_files = os.listdir('static')
    
    print('converting wav to mp3')
    if 'output.wav' in static_folder_files:
        AudioSegment.from_wav("static/output.wav").export("static/output.mp3", format="mp3")
        
        
        os.remove('static/output.wav')

        return 'output.mp3'
    else:
        return 'did_not_hear.mp3'
