
import streamlit as st
import whisper
import pyaudio
import wave
from googletrans import Translator
from io import BytesIO



def recordAudio(sec):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    frames = []

    for i in range(0, int(44100 / 1024 * sec)):  
        data = stream.read(1024)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    filename = "myrecording.wav"
    sound_file = wave.open(filename, "wb")
    sound_file.setnchannels(1)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames))
    sound_file.close()

    return filename 

def transcribe_audio(audio):
    audio = whisper.load_audio(audio)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)
    return result.text

def translate_text(text, target_language):
    translator = Translator()
    try:
        translation = translator.translate(text, dest=target_language)
        translated_text = translation.text
        return translated_text
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return None



nav_choice = st.sidebar.selectbox("", ["Home", "Record Audio", "Text Output"])
st.title("Speech to Text Translation System")
st.header("Team Members")
st.write("1. Ivan D'Silva - 9193")
st.write("2. Vailantan Fernandes - 9197")
st.write("3. Mathew Lobo - 9204")
st.markdown(
    f'<img style="left: 345px; width: 500px;top:-160px; position: absolute;" src="https://i.imgur.com/JhvWFLx.png" alt="cat gif">',
    unsafe_allow_html=True,
)
st.header("Mentor")
st.write("Prof. Supriya Kamoji")

if nav_choice=="Home Page":
    st.write("Welcome to the Speech to Text and Translation App!")
    st.write("Select a tab from the sidebar to get started.")

if nav_choice== "Record Audio":
    st.write("Record Audio")
    user_input = st.text_input("Enter duration to record in seconds")
    if st.button("Start Recording"):
        filename = recordAudio(int(user_input))
        audio_file = open(filename, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/wav')

if nav_choice == "Text Output":
    model = whisper.load_model("large-v2.pt")
    st.write("Text Output")
    language_option = st.selectbox("Select Target Language:", ["en (English)", "hi (Hindi)"])
    target_language = language_option.split(" ")[0]

    transcribed_text = transcribe_audio("myrecording.wav")

    if st.button("Translate"):
        translated_text = translate_text(transcribed_text, target_language)
        st.write(f"Transcribed Text: {transcribed_text}")
        st.write(f"Translated Text ({target_language}): {translated_text}")
    else:
        st.write(f"Transcribed Text: {transcribed_text}")