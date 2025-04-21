import os
import tempfile
from pathlib import Path
import streamlit as st
import assemblyai as aai
from dotenv import load_dotenv

load_dotenv()

aai.settings.api_key= os.getenv("AAI_TOKEN")

def generate_transcript(file):
    try:
        file_extension = Path(file.name).suffix.lower()
        if file_extension not in [".mp3",".m4a",".wav"]:
            raise st.error("Format not supported!")
        
        #creating a temporary file
        with tempfile.NamedTemporaryFile(delete=False,suffix=file_extension) as temp_file:
            temp_file.write(file.getbuffer())
            audio_file_path = temp_file.name
        
        #configuration for assembly ai 
        config = aai.TranscriptionConfig(speaker_labels=True)
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file_path,config=config)

        output_text = ""
        for utterance in transcript.utterances:
            output_text += f"Speaker {utterance.speaker}:{utterance.text}\n"
            print("output",output_text)
        return output_text
    except Exception as e:
        st.error(f"Transcription Error: {e}")
    
    #remove the temporary file after processing
    finally:
        if audio_file_path in locals() and os.path(audio_file_path):
            os.remove(audio_file_path)
