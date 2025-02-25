import streamlit as st
import whisper
import tempfile
import os

# Load the Whisper model
st.title("🎤 Audio to Text Transcription App")
st.write("Upload an audio file, and the app will transcribe it using Whisper.")

model = whisper.load_model("base")

# File uploader
uploaded_file = st.file_uploader("Upload an audio file (MP3, WAV, etc.)", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/mp3")

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(uploaded_file.read())
        temp_audio_path = temp_audio.name

    # Transcribe the audio
    st.write("Transcribing...")
    result = model.transcribe(temp_audio_path)

    # Display the transcribed text
    st.subheader("Transcribed Text:")
    st.write(result["text"])

    # Clean up
    os.remove(temp_audio_path)
