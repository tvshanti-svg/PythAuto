import streamlit as st
import pyttsx3
import os
from moviepy.editor import ColorClip, AudioFileClip

# Initialize page config
st.set_page_config(page_title="TTS to MP4 Generator", page_icon="🎙️")

# Helper to get voices
def get_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    return {v.name: v.id for v in voices}

st.title("🎙️ Text-to-Speech MP4 Creator")
st.write("Convert your text into a video file with custom system voices.")

# 1. Voice Selection Sidebar
voices_dict = get_voices()
selected_voice_name = st.selectbox("Select a Voice", options=list(voices_dict.keys()))
voice_id = voices_dict[selected_voice_name]

# 2. Text Input
text_input = st.text_area("Enter your script here:", height=200, placeholder="Hello, this is a test of the Microsoft David voice...")

# 3. Generate Logic
if st.button("Generate MP4 Video"):
    if not text_input.strip():
        st.error("Please enter some text first!")
    else:
        with st.spinner("Converting text to speech and rendering video..."):
            try:
                # Setup Paths
                audio_path = "temp_audio.wav"
                video_path = "output_video.mp4"

                # A. Generate Audio
                engine = pyttsx3.init()
                engine.setProperty('voice', voice_id)
                engine.save_to_file(text_input, audio_path)
                engine.runAndWait()

                # B. Create Video (MP4)
                audio_clip = AudioFileClip(audio_path)
                # Create a simple dark background
                video_clip = ColorClip(size=(1280, 720), color=(15, 15, 35), duration=audio_clip.duration)
                video_clip = video_clip.set_audio(audio_clip)
                
                # Write file (using low preset for speed)
                video_clip.write_videofile(video_path, fps=24, codec="libx264", audio_codec="aac", logger=None)
                
                audio_clip.close()
                video_clip.close()

                # C. Display & Download
                st.success("✅ Video Generated Successfully!")
                st.video(video_path)
                
                with open(video_path, "rb") as file:
                    st.download_button(
                        label="Download MP4",
                        data=file,
                        file_name="tts_video.mp4",
                        mime="video/mp4"
                    )
                
                # Cleanup temporary files
                os.remove(audio_path)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

st.info("Note: This app uses your system's built-in voices. Ensure 'Microsoft David' is installed in your Windows Speech settings.")
