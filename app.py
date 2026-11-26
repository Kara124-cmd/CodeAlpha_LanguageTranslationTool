import streamlit as st
import requests
from gtts import gTTS
import io

# Translation function
def translate(text, from_lang, to_lang):

    url = "https://api.mymemory.translated.net/get"

    params = {
        "q": text,
        "langpair": from_lang + "|" + to_lang
    }

    response = requests.get(url, params=params)

    data = response.json()

    return data["responseData"]["translatedText"]

# Language codes
language_codes = {
    "English": "en",
    "Urdu": "ur",
    "Hindi": "hi"
}

# Application title
st.title("Language Translation Tool")

st.write("Type text, choose languages, and click Translate.")

# Text input
user_text = st.text_area("Enter your text")

# Language selection
source_lang = st.selectbox(
    "From language",
    ["English", "Urdu", "Hindi"]
)

target_lang = st.selectbox(
    "To language",
    ["Urdu", "English", "Hindi"]
)

# Translation button
if st.button("Translate"):

    if user_text == "":
        st.warning("Please enter some text first.")

    else:
        source_code = language_codes[source_lang]
        target_code = language_codes[target_lang]

        result = translate(
            user_text,
            source_code,
            target_code
        )

        # Save translation in session state
        st.session_state["result"] = result
        st.session_state["target_code"] = target_code

# Display saved translation
if "result" in st.session_state:

    result = st.session_state["result"]

    st.subheader("Translated Text:")

    st.success(result)

    # Copy feature
    st.code(result)

    # Speech feature
    if st.button("Listen to translation"):

        tts = gTTS(
            text=result,
            lang=st.session_state["target_code"]
        )

        # FIXED: make the sound in memory, do not save a file.
        # The old lines tts.save("translation.mp3") and
        # st.audio("translation.mp3") gave FileNotFoundError.
        audio_file = io.BytesIO()
        tts.write_to_fp(audio_file)
        st.audio(audio_file.getvalue(), format="audio/mp3")
