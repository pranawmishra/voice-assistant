import azure.cognitiveservices.speech as speechsdk
import time
from datetime import datetime
from dotenv import load_dotenv
import pyaudio
import wave
import sounddevice as sd 
already_spoken = {}

def play_audio(file_name):
    """
    Plays an audio file.

    Parameters:
    file_name (str): The path to the audio file to be played.

    Returns:
    None
    """

    chunk = 1024
    wf = wave.open(file_name, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(chunk)
    while data:
        stream.write(data)
        data = wf.readframes(chunk)
    stream.stop_stream()
    stream.close()
    p.terminate()


def speak(text, SPEECH_REGION,SPEECH_KEY,SPEECH_LANGUAGE,OPENAI_KEY,silent=False, output_folder="Output"):
    """
    Converts text to speech using Azure Cognitive Services and plays the audio.

    Parameters:
    text (str): The text to be converted to speech.
    SPEECH_REGION (str): The Azure region for the speech service.
    SPEECH_KEY (str): The API key for Azure Cognitive Services.
    SPEECH_LANGUAGE (str): The language for the speech synthesis.
    OPENAI_KEY (str): The API key for OpenAI (not used in this function).
    silent (bool): If True, the audio will not be played. Default is False.
    output_folder (str): The folder where the audio file will be saved. Default is "Output".

    Returns:
    str: The input text.
    """
    if text in already_spoken:  # if the speech was already synthetized
        if not silent:
            play_audio(already_spoken[text])
        return
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(
        subscription=SPEECH_KEY, region=SPEECH_REGION)
    file_name = f'src/{output_folder}/{datetime.now().strftime("%Y%m%d_%H%M%S")}.wav'
    audio_config = speechsdk.audio.AudioOutputConfig(
        use_default_speaker=True, filename=file_name)
    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name = 'en-US-JennyNeural'
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config)
    speech_synthesis_result = speech_synthesizer.speak_text(text)  # .get()
    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("AI Assistant: {}".format(text.replace("\n", "")))
        if not silent:
            play_audio(file_name)
        already_spoken[text] = file_name
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(
            cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(
                    cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")
    return text



                                                                                                                    

                                                                                                                    