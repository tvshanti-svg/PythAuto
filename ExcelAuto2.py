import streamlit as st
from gtts import gTTS
import os
import moviepy.editor as mp

# Initialize page config
st.set_page_config(page_title="Cloud TTS to MP4", page_icon="☁️")

st.title("🎙️ Cloud TTS to MP4 Creator")
st.write("Convert text to video using Google's Cloud Voices.")

# 1. Voice/Language Selection (Cloud Friendly)
languages = {
    "English (US)": "en",
    "English (UK)": "en-uk",
    "English (India)": "en-in",
    "Spanish": "es",
    "French": "fr"
}
selected_lang = st.selectbox("Select Language Accent", options=list(languages.keys()))
lang_code = languages[selected_lang]

# 2. Text Input
text_input = st.text_area("Enter your script here:", height=200, placeholder="Type something...")

# 3. Generate Logic
if st.button("Generate MP4 Video"):
    if not text_input.strip():
        st.error("Please enter some text first!")
    else:
        with st.spinner("Rendering your video on the server..."):
            try:
                audio_path = "temp_audio.mp3"
                video_path = "output_video.mp4"

                # A. Generate Audio (gTTS works on Linux/Cloud)
                tts = gTTS(text=text_input, lang=lang_code)
                tts.save(audio_path)

                # B. Create Video (MP4)
                audio_clip = mp.AudioFileClip(audio_path)
                video_clip = mp.ColorClip(size=(1280, 720), color=(15, 15, 35), duration=audio_clip.duration)
                video_clip = video_clip.set_audio(audio_clip)
                
                # Write file
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
                
                # Cleanup
                if os.path.exists(audio_path): os.remove(audio_path)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
