#
# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Théophile Gentilhomme <theophile.gentilhomme@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#
# anonymization: Text ner and pii
#

import re

titles = [
    "mr.",
    "mrs.",
    "dr.",
    "ms.",
    "miss.",
    "m.",
    "mme.",
    "me.",
    "mlle.",
    "monsieur",
    "madame",
    "mademoiselle",
    "mr",
    "mrs",
    "dr",
    "ms",
    "miss",
    "m",
    "mme",
    "me",
    "mlle",
    "prof.",
    "prof",
]


def get_title(person):
    """
    Extract the title from a person's name.

    This function takes a person's name and tries to extract the title (e.g., 'Mr', 'Mrs', 'Dr')
    from the beginning of the name. If a valid title is found, it is returned as the output.

    Parameters:
        person (str): The person's name from which to extract the title.

    Returns:
        str or None: The extracted title if found, otherwise None.
    """
    # Convert the string to lowercase
    person = person.strip()
    cleaned_name = person.lower().strip().split(" ")[0]

    title = None
    for tit in titles:
        if cleaned_name == tit:
            title = person[: len(tit)].lstrip()
            break

    return title


def clean_string(input_string):
    """
    Clean the input string by removing titles and leading/trailing whitespaces.

    This function takes an input string and performs the following cleaning operations:
    - Convert the string to lowercase
    - Remove any titles (e.g., 'Mr', 'Mrs') from the beginning of the string
    - Remove leading and trailing whitespaces

    Parameters:
        input_string (str): The input string to be cleaned.

    Returns:
        str: The cleaned input string.
    """
    # Convert the string to lowercase
    cleaned_string = input_string.lower().strip()

    # Remove titles from the beginning of the string
    for title in titles:
        if cleaned_string.startswith(title):
            cleaned_string = cleaned_string[len(title) :].lstrip()  # noqa: E203

    # Remove empty spaces at the beginning and end of the string
    cleaned_string = cleaned_string.strip()

    return cleaned_string


def improve_text(text):
    """
    Improve the formatting of the input text.

    This function performs the following formatting improvements on the input text:
    - Replaces consecutive spaces with a single space
    - Removes undesirable spaces before periods and commas
    - Removes double periods and commas

    Parameters:
        text (str): The input text to be formatted.

    Returns:
        str: The text with improved formatting.
    """
    # Replace consecutive spaces with a single space
    text = " ".join(text.split())

    # Remove undesirable spaces before periods and commas
    text = text.replace(" ,", ",").replace(" .", ".")
    text = " ".join(text.split())
    # Remove double periods and commas
    text = re.sub(r"([.,])\1+", r"\1", text)
    return text
