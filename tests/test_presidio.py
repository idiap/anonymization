#
# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Théophile Gentilhomme <theophile.gentilhomme@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#
# anonymization: Text ner and pii
#

import json
import unittest
from pprint import pprint
from typing import List

from presidio_analyzer import AnalyzerEngine
from presidio_analyzer import EntityRecognizer
from presidio_analyzer import Pattern
from presidio_analyzer import PatternRecognizer
from presidio_analyzer import RecognizerResult
from presidio_analyzer.nlp_engine import NlpArtifacts
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

from anonymization.pii import BankAcount


class TestAttention(unittest.TestCase):
    def test_start(self):
        text = "His name is Mr. Jones and his phone number is 212-555-5555"

        analyzer = AnalyzerEngine()
        analyzer_results = analyzer.analyze(text=text, language="en")
        print(analyzer_results)

    def test_titles(self):
        titles_list = [
            "Sir",
            "Ma'am",
            "Madam",
            "Mr.",
            "Mrs.",
            "Ms.",
            "Miss",
            "Dr.",
            "Professor",
            "M.",
            "Mme",
        ]
        titles_recognizer = PatternRecognizer(
            supported_entity="TITLE", deny_list=titles_list
        )

        # Call recognizer directly
        text1 = "I suspect Professor Plum, in the Dining Room, with the candlestick"
        result = titles_recognizer.analyze(text1, entities=["TITLE"])
        print(f"Result:\n {result}")

        # Add in the analyser engine
        analyzer = AnalyzerEngine()
        analyzer.registry.add_recognizer(titles_recognizer)

        results = analyzer.analyze(text=text1, language="en")
        print("Results:")
        print(results)

        print("Identified these PII entities:")
        for result in results:
            print(f"- {text1[result.start:result.end]} as {result.entity_type}")

    def test_bk_ac(self):
        recognizer = BankAcount()
        text2 = "My acompt is CH256212360005"

        numbers_result = recognizer.analyze(text=text2, entities=["BANK_ACCOUNT"])

        print("Result regx:")
        print(numbers_result)

    def test_num_reco(self):
        class NumbersRecognizer(EntityRecognizer):

            expected_confidence_level = (
                0.7  # expected confidence level for this recognizer
            )

            def load(self) -> None:
                """No loading is required."""
                pass

            def analyze(
                self, text: str, entities: List[str], nlp_artifacts: NlpArtifacts
            ) -> List[RecognizerResult]:
                """
                Analyzes test to find tokens which represent numbers (either 123 or One Two Three).
                """
                results = []

                # iterate over the spaCy tokens, and call `token.like_num`
                for token in nlp_artifacts.tokens:
                    if token.like_num:
                        result = RecognizerResult(
                            entity_type="NUMBER",
                            start=token.idx,
                            end=token.idx + len(token),
                            score=self.expected_confidence_level,
                        )
                        results.append(result)
                return results

        # Instantiate the new NumbersRecognizer:
        new_numbers_recognizer = NumbersRecognizer(supported_entities=["NUMBER"])
        text3 = "Roberto lives in Five 10 Broad st."
        analyzer = AnalyzerEngine()
        analyzer.registry.add_recognizer(new_numbers_recognizer)

        numbers_results2 = analyzer.analyze(text=text3, language="en")
        print("Results:")
        print("\n".join([str(res) for res in numbers_results2]))

    def test_lang(self):
        configuration = {
            "nlp_engine_name": "spacy",
            "models": [
                {"lang_code": "fr", "model_name": "fr_core_news_lg"},
                {"lang_code": "en", "model_name": "en_core_web_lg"},
            ],
        }
        # Define the regex pattern in a Presidio `Pattern` object:
        numbers_pattern = Pattern(
            name="numbers_pattern", regex="\d+", score=0.5  # noqa: W605
        )

        # Define the recognizer with one or more patterns
        number_recognizer = PatternRecognizer(
            supported_entity="NUMBER", patterns=[numbers_pattern]
        )
        # Create NLP engine based on configuration
        provider = NlpEngineProvider(nlp_configuration=configuration)
        nlp_engine_with_spanish = provider.create_engine()

        # Pass the created NLP engine and supported_languages to the AnalyzerEngine
        analyzer = AnalyzerEngine(
            nlp_engine=nlp_engine_with_spanish, supported_languages=["en", "fr"]
        )
        analyzer.registry.add_recognizer(number_recognizer)

        text1 = """
        Boulanger, habitant à Boulanger et travaillant dans
        le magasin Boulanger situé dans la ville de Boulanger.
        Boulanger a écrit le livre éponyme Boulanger édité par
        la maison d'édition Boulanger. Som numéro de téléphone
        est 0763252698. Son compte bancaire CH756625551233.
        """
        # Analyze in different languages
        results_fr = analyzer.analyze(text=text1, language="fr")
        print("Results from French request:")
        pprint(results_fr)

        anonymizer = AnonymizerEngine()

        anonymized_results = anonymizer.anonymize(
            text=text1,
            analyzer_results=results_fr,
            operators={
                "DEFAULT": OperatorConfig("replace", {"new_value": "<ANONYMIZED>"}),
                "PHONE_NUMBER": OperatorConfig(
                    "mask",
                    {
                        "type": "mask",
                        "masking_char": "*",
                        "chars_to_mask": 12,
                        "from_end": True,
                    },
                ),
                "TITLE": OperatorConfig("redact", {}),
            },
        )

        print(f"text: {anonymized_results.text}")
        print("detailed response:")

        pprint(json.loads(anonymized_results.to_json()))

        results_english = analyzer.analyze(text="My name is Morris", language="en")
        print("Results from English request:")
        print(results_english)


if __name__ == "__main__":
    unittest.main()
