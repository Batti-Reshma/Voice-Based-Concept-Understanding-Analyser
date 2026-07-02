import whisper
import os

# Load Whisper model once
model = whisper.load_model("base")

def transcribe_audio(audio_path):
    """
    Transcribes an audio file into text using OpenAI Whisper.
    """

    if not os.path.exists(audio_path):
        raise FileNotFoundError("Audio file not found.")

    result = model.transcribe(audio_path)

    return result["text"]