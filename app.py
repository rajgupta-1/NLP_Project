# app.py

import streamlit as st
import pyttsx3
import speech_recognition as sr
import tempfile
import os

st.set_page_config(page_title="Speech App", layout="centered")
st.title("🗣️ Speech App")

option = st.selectbox("Choose an Operation", ["Select", "Text to Speech (OP1)", "Speech to Text + Speak (OP2)"])

if option == "Text to Speech (OP1)":
    text = st.text_area("Enter text to speak:")
    if st.button("Speak"):
        if text:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
            st.success("✅ Speaking done!")
        else:
            st.warning("Please enter some text.")

elif option == "Speech to Text + Speak (OP2)":
    st.info("🎤 Click below to start recording from your microphone.")
    if st.button("Start Recording"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("🟡 Listening...")
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                st.success(f"📝 You said: `{text}`")

                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()

            except sr.UnknownValueError:
                st.error("❌ Could not understand audio.")
            except sr.RequestError:
                st.error("❌ Speech service is down.")
