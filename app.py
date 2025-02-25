import os
import streamlit as st
import whisper
import subprocess
from tempfile import NamedTemporaryFile

# Ensure FFmpeg is installed (Required for audio processing)
try:
    subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except FileNotFoundError:
    st.error("FFmpeg is not installed on the server. Please install it.")
    st.stop()

# Load the Whisper model (use "base" for better performance on Streamlit Cloud)
model = whisper.load_model("base")

st.title("🎙️ Whisper AI Audio Transcription")
st.write("Upload an audio file and get an instant transcription.")

# File uploader
uploaded_file = st.file_uploader("Choose an audio file...", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    st.success("File uploaded successfully!")

    # Save uploaded file temporarily
    with NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(uploaded_file.read())
        temp_audio_path = temp_audio.name

    # Transcribe the audio
    st.info("Transcribing... Please wait ⏳")

    result = model.transcribe(temp_audio_path)

    # Remove "Transcribing..." message after response is ready
    st.success("Transcription complete! ✅")

    # Display the transcription
    st.text_area("Transcription:", result["text"], height=250)

    # Remove the audio file after transcription
    os.remove(temp_audio_path)
