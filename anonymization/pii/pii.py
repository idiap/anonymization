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

from presidio_analyzer import AnalyzerEngine
from presidio_analyzer import RecognizerResult
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine
from transformers import pipeline

from anonymization.pii.config import gen_default_config
from anonymization.pii.conversion import hf_ner_res_to_presidio
from anonymization.pii.custom_recognizer import AddressNumber
from anonymization.pii.custom_recognizer import BankAcount
from anonymization.pii.custom_recognizer import SwissZipCode
from anonymization.utils import improve_text


class PIIDetection(object):
    """
    Personal Identifiable Information (PII) Detector.

    This class performs Named Entity Recognition (NER) and PII analysis on the input text.
    It uses various NER models, such as Camembert NER, SwissBERT NER, and Spacy, to identify
    entities and personally identifiable information present in the text.

    Args:
        config (dict, optional): Configuration dictionary with the following optional keys:
            - "entities" (list): A list of PII entity types to detect. Default is an empty list.
            - "language" (str): The language of the input text (e.g., 'fr', 'de', 'en'). Default is 'fr'.
            - "use_camembert" (bool): Whether to use Camembert NER for French. Default is True.
            - "use_swiss_ner" (bool): Whether to use SwissBERT NER for Swiss languages. Default is True.
            - "use_spacy" (bool): Whether to use Spacy for NER. Default is True.

    Note:
        - The `config` dictionary allows fine-tuning the behavior of the PII detector.

    Example Usage:
        # Create the PIIDetection instance with default configuration
        pii_detector = PIIDetection()

        # Analyze the input text for named entities and PII
        text = "John Doe's bank account number is CH1234567890123456789."
        analysis_results = pii_detector.analyse(text)

        # Print the recognized entities and PII in the text
        for result in analysis_results:
            print(result)
    """

    def __init__(self, config=None) -> None:
        self.config = gen_default_config() if config is None else config
        self.entities = set(self.config.get("entities"))
        self.lang = self.config.get("language", "fr")
        self.camembert_ner = None
        if self.config.get("use_camembert", True) and self.lang == "fr":
            self.camembert_ner = pipeline(
                task="ner",
                model="Jean-Baptiste/camembert-ner-with-dates",
                tokenizer="Jean-Baptiste/camembert-ner-with-dates",
                aggregation_strategy="simple",
            )

        self.swiss_ner = None
        if self.config.get("use_swiss_ner", True):
            self.swiss_ner = pipeline(
                model="ZurichNLP/swissbert-ner",
                aggregation_strategy="simple",
            )
            if self.lang == "de":
                self.swiss_ner.model.set_default_language("de_CH")
            elif self.lang == "fr":
                self.swiss_ner.model.set_default_language("fr_CH")
            else:
                print("Swiss NER only available for fr or de")
                self.swiss_ner = None

        self.spacy_pii = None
        if self.config.get("use_scapy", True):
            models = []
            if self.lang == "fr":
                models = [
                    {"lang_code": "fr", "model_name": "fr_core_news_lg"},
                ]
            elif self.lang == "en":
                models = [
                    {"lang_code": "en", "model_name": "en_core_web_lg"},
                ]
            else:
                models = [
                    {"lang_code": "de", "model_name": "de_core_news_lg"},
                ]
            configuration = {"nlp_engine_name": "spacy", "models": models}
            provider = NlpEngineProvider(nlp_configuration=configuration)
            nlp_engine = provider.create_engine()
            analyzer = AnalyzerEngine(
                nlp_engine=nlp_engine, supported_languages=[self.lang]
            )

            # Custom recognizer
            analyzer.registry.add_recognizer(BankAcount())
            analyzer.registry.add_recognizer(SwissZipCode())
            analyzer.registry.add_recognizer(AddressNumber())
            self.spacy_pii = analyzer

    def _filter(self, list):
        """
        Filter the analysis results based on the PII entity types.

        Parameters:
            results (list): List of RecognizerResult objects.

        Returns:
            list: A filtered list containing RecognizerResult objects with PII entity types.
        """
        out = []
        for item in list:
            if item.entity_type in self.entities:
                out.append(item)
        return out

    def analyse(self, text: str):
        """
        Perform named entity recognition (NER) and personally
        identifiable information (PII) analysis on the input text.

        Args:
            text (str): The input text to be analyzed.

        Returns:
            list: A list containing the analysis results
            for named entities and PII found in the text.
        """
        out = []
        if self.camembert_ner is not None:
            tmp = self.camembert_ner(text)
            tmp = hf_ner_res_to_presidio(tmp, "camembert")
            out += self._filter(tmp)

        if self.swiss_ner is not None:
            tmp = self.swiss_ner(text)
            tmp = hf_ner_res_to_presidio(tmp, "swiss_ner")
            out += self._filter(tmp)

        if self.spacy_pii is not None:
            tmp = self.spacy_pii.analyze(text=text, language=self.lang)
            out += self._filter(tmp)

        return out


class Anonymize(object):
    """
    Anonymize the Personally Identifiable Information (PII) results of the analysis.

    This class takes the PII analysis results and performs anonymization on the identified PII
    using the specified operators.

    Args:
        operators (dict): A dictionary of anonymization operators to be used for each PII entity type.
            The dictionary should have PII entity types as keys (e.g., 'EMAIL_ADDRESS', 'PERSON'),
            and the corresponding anonymization operator as values.

    Example Usage:
        # Create the Anonymize instance with the anonymization operators
        operators = {
            'EMAIL_ADDRESS': 'replace',  # Anonymize email addresses by replacing with a generic value
            'PERSON': 'hash',  # Anonymize personal names using hashing
            'PHONE_NUMBER': 'redact',  # Redact phone numbers from the text
        }
        anonymizer = Anonymize(operators)

        # Analyze the input text for PII
        text = "Please contact John Doe at john.doe@example.com or call 123-456-7890."
        analysis_results = pii_detector.analyse(text)

        # Anonymize the identified PII
        anonymized_results = anonymizer.anonymise(text, analysis_results)

        # Print the anonymized text
        print(anonymized_results)
    """

    def __init__(self, operators) -> None:
        self.operators = operators
        self.anonymizer = AnonymizerEngine()

    def anonymise(self, text: str, analyzer_results: List[RecognizerResult]):
        """
        Anonymize the identified Personally Identifiable Information (PII) in the input text.

        This method takes the original input text and the results of the PII analysis (analyzer_results),
        and performs anonymization on the identified PII using the specified operators.

        Args:
            text (str): The original input text containing Personally Identifiable Information (PII).
            analyzer_results (List[RecognizerResult]): A list of RecognizerResult objects containing
                the analysis results for the identified PII in the text.

        Returns:
            str: The anonymized text with the identified PII replaced or redacted as per the specified operators.
        """
        anonymized_results = self.anonymizer.anonymize(
            text=text, analyzer_results=analyzer_results, operators=self.operators
        )
        return improve_text(anonymized_results.text)
