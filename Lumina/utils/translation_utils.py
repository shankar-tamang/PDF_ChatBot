import asyncio
from googletrans import Translator

def translate_text(text, target_lang="ne"):
    """Translates text to the specified language using googletrans."""
    try:
        translator = Translator()
        # Use asyncio.run to await the coroutine
        translation = asyncio.run(translator.translate(text, dest=target_lang))
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Return the original text on error

def translate_to_english(text):
    """Translates text from Nepali to English."""
    return translate_text(text, target_lang="en")
