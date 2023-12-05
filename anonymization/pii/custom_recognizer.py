#
# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Théophile Gentilhomme <theophile.gentilhomme@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#
# anonymization: Text ner and pii
#


from typing import List
from typing import Optional

from presidio_analyzer import Pattern
from presidio_analyzer import PatternRecognizer


class BankAcount(PatternRecognizer):
    """
    Recognize Bank accounts.

    This function performs recognition of bank account numbers using a list of provided patterns.
    It takes the input parameters, such as patterns, context words, supported language, and supported entity,
    to increase confidence in the detection of bank account numbers.

    Parameters:
        patterns (list): List of patterns to be used by this recognizer for detecting bank account numbers.
        context (list, optional): List of context words that can be used to provide additional context to the
                                  recognition process. Default is None.
        supported_language (str, optional): Language code representing the language this recognizer supports.
                                            Default is None.
        supported_entity (str, optional): The type of entity (e.g., 'BANK_ACCOUNT', 'IBAN') that this recognizer
                                          can detect. Default is None.

    Returns:
        List of recognized bank account numbers.
    """

    PATTERNS = [
        Pattern(
            "All Bank accounts (weak)",
            r"[A-Za-z]{2}[0-9-,_]{4}[0-9-,_]+",  # noqa: E501
            0.9,
        ),
    ]

    CONTEXT = [
        "account",
        "bank",
        "transaction",
        "mastercard",
        "account number",
        "banking",
        "ubs",
        "UBS",
        "Crédit Suisse",
        "BCV",
        "BCVs",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "fr",
        supported_entity: str = "BANK_ACCOUNT",
    ):
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )


class SwissZipCode(PatternRecognizer):
    """
    Recognize Swiss ZIP codes.

    This function performs recognition of Swiss ZIP codes using a list of provided patterns.
    It takes the input parameters, such as patterns, context words, supported language, and supported entity,
    to increase confidence in the detection of Swiss ZIP codes.

    Parameters:
        patterns (list): List of patterns to be used by this recognizer for detecting Swiss ZIP codes.
        context (list, optional): List of context words that can be used to provide additional context to the
                                  recognition process. Default is None.
        supported_language (str, optional): Language code representing the language this recognizer supports.
                                            Default is None.
        supported_entity (str, optional): The type of entity (e.g., 'ZIP_CODE', 'POSTAL_CODE') that this recognizer
                                          can detect. Default is None.

    Returns:
        List of recognized Swiss ZIP codes.
    """

    PATTERNS = [
        Pattern(
            "Swiss Zip code (weak)",
            r", [0-9]{4}, ",  # noqa: E501
            0.9,
        ),
    ]

    CONTEXT = ["habite" "adresse", "vit à", "ville", "chemin", "route", "rue", "avenue"]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "fr",
        supported_entity: str = "CH_ZIPCODE",
    ):
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )


class AddressNumber(PatternRecognizer):
    """
    Recognize address numbers.

    Parameters:
        patterns (list): List of patterns for detecting address numbers.
        context (list, optional): List of context words to enhance recognition confidence.
        supported_language (str, optional): Supported language code for this recognizer.
        supported_entity (str, optional): Type of entity (e.g., 'ADDRESS_NUMBER') detected.

    Returns:
        List of recognized address numbers.
    """

    PATTERNS = [
        Pattern(
            "All Bank accounts (weak)",
            r"\b \d{1,3},",  # noqa: E501
            0.9,
        ),
    ]

    CONTEXT = ["route", "avenue", "rue", "chemin", "passage"]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "fr",
        supported_entity: str = "ADDRESS_NUMBER",
    ):
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )
