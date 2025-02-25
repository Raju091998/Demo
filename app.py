import os
import whisper
import streamlit as st
import torch
import ffmpeg
import subprocess
import asyncio

# Ensure FFmpeg is accessible
FFMPEG_PATH = r"/usr/bin/ffmpeg"  # Default path for Streamlit Cloud
os.environ["PATH"] += os.pathsep + FFMPEG_PATH

# Ensure Torch is properly installed
st.write(f"Torch version: {torch.__version__}")

# Check FFmpeg installation
try:
    subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except FileNotFoundError:
    st.error("FFmpeg is not installed. Please install it.")
    st.stop()

# Handle event loop issue
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

st.title("🎙️ Audio-to-Text Converter (Whisper)")

uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])

if uploaded_file:
    st.audio(uploaded_file, format="audio/mp3")

    # Save uploaded file
    file_path = f"temp_audio.{uploaded_file.name.split('.')[-1]}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    # Convert to WAV if needed
    wav_path = "converted_audio.wav"
    if not file_path.endswith(".wav"):
        try:
            ffmpeg.input(file_path).output(wav_path, format="wav").run(overwrite_output=True)
            file_path = wav_path
        except Exception as e:
            st.error(f"FFmpeg conversion error: {e}")
            os.remove(file_path)
            st.stop()

    # Load Whisper model
    model = whisper.load_model("base")

    # Transcribe audio
    result = model.transcribe(file_path)

    # Remove audio file after transcription
    try:
        os.remove(file_path)
    except Exception as e:
        st.warning(f"Could not delete temporary file: {e}")

    # Display transcription
    st.subheader("📝 Transcribed Text")
    st.write(result["text"])
