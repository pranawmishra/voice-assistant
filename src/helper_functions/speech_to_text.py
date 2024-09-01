from openai import OpenAI
import datetime

def stt(audio_file,api_key):
  """
  Transcribes an audio file using OpenAI's Whisper model.

  Parameters:
  audio_file (str): The path to the audio file to be transcribed.
  api_key (str): The API key for accessing the OpenAI service.

  Returns:
  tuple: A tuple containing:
      - transcription.text (str): The transcribed text from the audio file.
      - time_taken (datetime.timedelta): The time taken to perform the transcription.
  """

  client = OpenAI(api_key=api_key)
  t1 = datetime.datetime.now()
  audio_file= open(audio_file, "rb")
  transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
  )
  t2 = datetime.datetime.now()
  return(transcription.text, t2-t1)