#
# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Théophile Gentilhomme <theophile.gentilhomme@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#
# anonymization: Text ner and pii
#

from presidio_analyzer import RecognizerResult

MODEL_TO_PRESIDIO_MAPPING = {
    "PER": "PERSON",
    "LOC": "LOCATION",
    "ORG": "ORGANIZATION",
    "AGE": "AGE",
    "ID": "ID",
    "EMAIL": "EMAIL",
    "PATIENT": "PERSON",
    "STAFF": "PERSON",
    "HOSP": "ORGANIZATION",
    "PATORG": "ORGANIZATION",
    "DATE": "DATE_TIME",
    "PHONE": "PHONE_NUMBER",
    "MISC": "MISC",
    "TITLE": "TITLE",
}


def hf_ner_res_to_presidio(hf_res, ner_name=None):
    """
    Convert Hugging Face NER pipeline result to RecognizerResult.

    This function takes the output of a Named Entity Recognition (NER) model run by Hugging Face
    and converts it into a list of RecognizerResult objects, which is the data format used by
    the Presidio Analyzer for named entity recognition.

    Parameters:
        hf_res (list): A list of dictionaries representing the Hugging Face NER result. Each dictionary
                       should contain the following keys:
                       - 'entity_group' (str): The recognized entity group (e.g., 'PERSON', 'LOCATION').
                       - 'score' (float): The confidence score of the prediction.
                       - 'start' (int): The start index of the recognized entity in the input text.
                       - 'end' (int): The end index of the recognized entity in the input text.

        ner_name (str, optional): The name of the NER model used for the analysis. This parameter will be
                                  stored in the 'analysis_explanation' field of the RecognizerResult objects.
                                  Default is None.

    Returns:
        list: A list of RecognizerResult objects, each representing a recognized entity from the input.

    Example Usage:
        hf_result = [{'entity_group': 'PERSON', 'score': 0.95, 'start': 0, 'end': 4},
                     {'entity_group': 'LOCATION', 'score': 0.87, 'start': 10, 'end': 17}]

        # Convert HF NER result to Presidio RecognizerResult
        presidio_result = hf_ner_res_to_presidio(hf_result, ner_name='My_NER_Model')

        # Print the converted result
        for result in presidio_result:
            print(result)
    """
    out = []
    for ent in hf_res:
        entity_group = ent["entity_group"]
        entity_group = MODEL_TO_PRESIDIO_MAPPING.get(entity_group, entity_group)
        score = ent["score"]
        start = ent["start"]
        end = ent["end"]
        out.append(
            RecognizerResult(
                entity_type=entity_group,
                start=start,
                end=end,
                score=score,
                analysis_explanation=ner_name,
            )
        )
    return out
