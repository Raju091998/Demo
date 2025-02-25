import streamlit as st
import whisper
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

model = whisper.load_model("base")

st.title("Audio to Text Converter with Whisper")

uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/mp3")

    if st.button("Transcribe"):
        with st.spinner("Transcribing..."):
            file_path = f"temp_audio.{uploaded_file.name.split('.')[-1]}"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            result = model.transcribe(file_path)
            st.success("Transcription completed!")
            st.text_area("Transcribed Text", result["text"], height=200)

            import os
            os.remove(file_path)
