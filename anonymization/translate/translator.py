from typing import Any

from easynmt import EasyNMT


class Translator(object):
    """
    Text Translator using EasyNMT.

    This class initializes a text translator for translating text from the source
    language to the target language
    using the specified translation model.

    Args:
        source_lan (str, optional): The source language code for translation. Default is 'fr'.
        target_lan (str, optional): The target language code for translation. Default is 'en'.
        model (str, optional): The name or identifier of the translation model to use. Default is 'opus-mt'.

    Note:
        - The source and target language codes should follow the ISO 639-1
        two-letter language codes (e.g., 'fr', 'en', 'de').

    Example Usage:
        # Create the Translator instance with default parameters
        # (source: 'fr', target: 'en', model: 'opus-mt')
        translator = Translator()

        # Translate a text from French to English
        input_text = "Bonjour tout le monde!"
        translated_text = translator(input_text)

        # Print the translated text
        print(translated_text)
    """

    def __init__(
        self, source_lan: str = "fr", target_lan: str = "en", model: str = "opus-mt"
    ) -> None:
        """
        Initialize the Translator instance.

        Parameters:
            source_lan (str, optional): The source language code for translation. Default is 'fr'.
            target_lan (str, optional): The target language code for translation. Default is 'en'.
            model (str, optional): The name or identifier of the translation model to use. Default is 'opus-mt'.
        """
        self.target = target_lan
        self.model = EasyNMT(model, source_lang=source_lan)

    def __call__(self, text: str) -> Any:
        """
        Translate the input text from the source language to the target language.

        Parameters:
            text (str): The input text to be translated.

        Returns:
            Any: The translated text in the target language.
        """
        return self.model.translate(text, target_lang=self.target)
