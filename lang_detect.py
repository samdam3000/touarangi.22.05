# lang_detect.py

from langdetect import detect
from googletrans import Translator

translator = Translator()

def detect_language_and_translate(text):
    """
    Detects the language of input text and translates it to English if needed.
    Returns the original text if it's already in English or if translation fails.
    """
    try:
        language = detect(text)
        if language != "en":
            translated = translator.translate(text, src=language, dest="en")
            return translated.text
        return text
    except Exception as e:
        print(f"[Translation Error] {e}")
        return text