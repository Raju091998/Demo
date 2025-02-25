import os
import whisper
import ffmpeg
import streamlit as st
import subprocess

# Ensure FFmpeg is in PATH
FFMPEG_PATH = r"C:\ffmpeg\bin"  # Adjust this path if needed
os.environ["PATH"] += os.pathsep + FFMPEG_PATH

# Check if FFmpeg is accessible
try:
    subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except FileNotFoundError:
    st.error("FFmpeg not found! Please install FFmpeg and add it to PATH.")
    st.stop()

# Streamlit UI
st.title("🎙️ Audio-to-Text Converter (Whisper)")

# File Upload
uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])

if uploaded_file:
    st.audio(uploaded_file, format="audio/mp3")

    # Save uploaded file
    file_ext = uploaded_file.name.split('.')[-1]
    file_path = f"temp_audio.{file_ext}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    # Placeholder for messages
    msg_placeholder = st.empty()

    # Convert to WAV if needed
    wav_path = "converted_audio.wav"
    if file_ext != "wav":
        msg_placeholder.info("Converting to WAV format for better compatibility...")
        try:
            ffmpeg.input(file_path).output(wav_path, format="wav").run(overwrite_output=True)
            file_path = wav_path  # Use the converted file
        except Exception as e:
            st.error(f"FFmpeg conversion error: {e}")
            os.remove(file_path)  # Remove original file on error
            st.stop()

    # Load Whisper model
    model = whisper.load_model("base")

    # Show transcribing message
    msg_placeholder.info("Transcribing audio... This may take a while.")

    # Transcribe audio
    result = model.transcribe(file_path)

    # Remove the loading message
    msg_placeholder.empty()

    # Delete the audio file after transcription
    try:
        os.remove(file_path)
    except Exception as e:
        st.warning(f"Could not delete temporary file: {e}")

    # Display transcription
    st.subheader("📝 Transcribed Text")
    st.write(result["text"])
