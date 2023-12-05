#
# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Théophile Gentilhomme <theophile.gentilhomme@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#
# anonymization: Text ner and pii
#

import random
import string
from datetime import date

import gender_guesser.detector as gender
from faker import Faker

from anonymization.utils import clean_string
from anonymization.utils import get_title

keywords_to_types = {
    "university": ["université", "école", "institut"],
    "hospital": ["hôpital", "clinique", "médical"],
    "ngo": ["association", "fondation"],
    "bank": [
        "banque",
        "crédit",
        "finance",
        "credit suisse",
        "ubs",
        "zurich cantonal bank",
        "julius baer",
        "raiffeisen",
        "pictet",
        "lombard odier",
        "cantonal bank of geneva",
        "swiss cantonal bank",
        "bcv (banque cantonale vaudoise)",
        "bcv",
        "bcge (banque cantonale de genève)",
        "bcge",
        "bern cantonal bank",
        "zuger cantonal bank",
        "luzerner kantonalbank",
        "schaffhauser kantonalbank",
        "basler kantonalbank",
        "graubündner kantonalbank",
        "thurgauer kantonalbank",
        "st. gallen cantonal bank",
        "valiant bank",
        "glarner kantonalbank",
        "obwaldner kantonalbank",
        "uri cantonal bank",
        "bordier",
        "edmond de rothschild",
        "bank coop",
        "schroder & co bank",
        "vontobel",
        "falcon private bank",
        "piguet galland & cie",
        "habib bank",
        "mirabaud",
        "gazprombank (switzerland)",
        "j. safra sarasin",
        "julius baer",
        "arab bank (switzerland)",
        "bank hapoalim (switzerland)",
        "bordier & cie",
        "btg pactual (switzerland)",
        "century financial consultants",
        "eiger fx",
        "hyposwiss",
        "union bancaire privée (ubp)",
        "ubp",
        "hyposwiss private bank genève",
        "arab national bank (switzerland)",
        "wir bank",
        "notenstein privatbank",
        "bank am bellevue",
        "landolt & cie",
        "bank la roche",
        "hyposwiss private bank zürich",
        "bank j. safra sarasin",
        "cbh compagnie bancaire helvétique",
        "linth bank",
        "banque cantonale du jura",
        "bank co-op ag",
        "hypothekarbank lenzburg ag",
        "aargauische kantonalbank",
        "appenzeller kantonalbank",
        "banca dello stato del canton ticino",
        "banque cantonale neuchâteloise",
        "bcf (banque cantonale de fribourg)",
        "banque cantonale du valais",
        "raiffeisen gruppe",
        "hypothekarbank vital",
        "helsinki-bank",
        "zurcher kantonalbank",
        "schwyzer kantonalbank",
        "migros bank",
        "credit agricole next bank",
        "axion swiss bank",
        "bank co-op",
        "baloise bank soba",
        "credit mutuel-cic (suisse)",
        "bnp paribas (suisse)",
        "goldman sachs (switzerland)",
        "bank linth llb",
        "axa bank europe (switzerland)",
        "volksbank",
        "jpmorgan chase (suisse)",
        "hypothekarbank bern",
        "lenzburgische kantonalbank",
        "banque cantonale vaudoise (bcv)",
        "hypothekarbank luzern",
        "glarner kantonalbank",
        "bank coop",
        "coop bank",
        "zuger kantonalbank",
        "cembra money bank",
        "schaffhauser kantonalbank",
        "sparkasse schwyz",
        "axion swiss bank",
        "luzerner kantonalbank",
        "bank coop ag",
        "zuricher kantonalbank",
        "luzerner kantonalbank",
        "st. gallen cantonal bank",
        "union bank of switzerland (ubs)",
        "vontobel holding",
        "winterthur group",
        "zurcher kantonalbank",
        "luzerner kantonalbank",
        "nacional bank",
    ],
    "assurance": ["assurance", "assureur", "assurance-maladie", "mutuelle"],
    "law_firm": ["avocat", "avocats", "cabinet d'avocats", "lawyer", "law firm"],
    "notaire": ["notaire"],
    "fiduciaire": ["fiduciaire"],
    "company": ["société", "entreprise"],
}

MEM_FAKE = dict()


def reset_mem_fake():
    """
    Reset the global MEM_FAKE dictionary.

    This function clears the global MEM_FAKE dictionary, which is used to store fake names for entities.
    """
    global MEM_FAKE
    MEM_FAKE = dict()


def check_name(original_name, entity):
    """
    Check if a fake name for the given original name and entity exists.

    Parameters:
        original_name (str): The original name for which to check if a fake name exists.
        entity (str): The type of entity for which the fake name is associated.

    Returns:
        str or None: The fake name associated with the original name and entity if it exists, otherwise None.
    """
    clean = clean_string(original_name)
    return MEM_FAKE.get((clean, entity))


def add_name(original_name, entity, fake_name):
    """
    Add a fake name for the given original name and entity.

    Parameters:
        original_name (str): The original name for which to add the fake name.
        entity (str): The type of entity associated with the fake name.
        fake_name (str): The fake name to be associated with the original name and entity.
    """
    clean = clean_string(original_name)
    MEM_FAKE[(clean, entity)] = fake_name


def deduce_gender(name):
    """
    Deduce the gender of a given name.

    Parameters:
        name (str): The name for which to deduce the gender.

    Returns:
        str or None: The deduced gender ('male', 'female', 'andy') or None if the gender couldn't be determined.
    """
    # Create an instance of the Detector class from gender-guesser
    detector = gender.Detector()

    # Get the gender guess for the name
    gender_guess = detector.get_gender(name)

    # Clean up the gender guess and return it
    if gender_guess == "mostly_male":
        return "male"
    elif gender_guess == "mostly_female":
        return "female"
    elif gender_guess in ["male", "female", "andy"]:
        return gender_guess
    else:
        return None


def fake_name(original_name):
    """
    Generate a fake name based on the original name.

    Parameters:
        original_name (str): The original name for which to generate the fake name.

    Returns:
        str: The generated fake name.
    """
    title = get_title(original_name)
    fake_name = check_name(original_name, "PERSON")
    if fake_name is None:
        fake = Faker("fr_CH")
        original_gender = deduce_gender(original_name)
        if title is not None:
            fake_name = fake.last_name()
        elif original_gender == "male":
            fake_name = fake.name_male()
        elif original_gender == "female":
            fake_name = fake.name_female()
        else:
            fake_name = fake.name()
    add_name(original_name, "PERSON", fake_name)
    if title is not None:
        fake_name = title + " " + fake_name
    return " {} ".format(fake_name)


def fake_phone(x):
    """
    Generate a fake phone number.

    Parameters:
        x (str): Not used in the function. Can be any value.

    Returns:
        str: The generated fake phone number.
    """
    fake = Faker("fr_CH")
    # Generate a random phone number for the specified country
    return " {} ".format(fake.phone_number())


def fake_swiss_location(input_text):
    """
    Generate a fake Swiss location name or address.

    Parameters:
        input_text (str): The input text from which to generate the fake location.

    Returns:
        str: The generated fake Swiss location name or address.
    """
    fake = Faker("fr_CH")
    # Common Swiss address keywords and comma check
    address_keywords = [
        "rue",
        "avenue",
        "boulevard",
        "place",
        "chemin",
        "route",
        "impasse",
        "allée",
    ]
    has_comma = "," in input_text

    if has_comma:
        # Assume it's an address with comma-separated elements
        return " {} ".format(fake.address())

    input_lower = input_text.lower()

    if any(keyword in input_lower for keyword in address_keywords):
        # Generate a fake full address
        return " {} ".format(fake.address())

    # Generate a fake Swiss city name
    fake_city = fake.city()
    add_name(input_text, "CITY", fake_name)
    return " {} ".format(fake_city)


def fake_swiss_french_organization(input_text):
    """
    Generate a fake Swiss French organization name.

    Parameters:
        input_text (str): The input text from which to generate the fake organization name.

    Returns:
        str: The generated fake Swiss French organization name.
    """
    out = check_name(input_text, "ORGANIZATION")
    if out is not None:
        return " {} ".format(out)

    fake = Faker("fr_CH")
    organization_type = None

    # Check for common keywords to determine organization type
    if input_text:
        input_lower = input_text.lower()
        for org_type, keywords in keywords_to_types.items():
            if any(keyword in input_lower for keyword in keywords):
                organization_type = org_type
                break

    # Generate fake organization based on the detected type or default to company
    if organization_type == "university":
        out = fake.university()
    elif organization_type == "hospital":
        out = fake.city() + " Hôpital"
    elif organization_type == "ngo":
        out = fake.last_name() + " Fondation"
    elif organization_type == "bank":
        out = fake.last_name() + " Banque"
    elif organization_type == "assurance":
        out = fake.last_name()() + " Assurance"
    elif organization_type == "law_firm":
        out = fake.last_name() + " Cabinet d'Avocats"
    elif organization_type == "notaire":
        out = fake.last_name() + " Notaire"
    elif organization_type == "fiduciaire":
        out = fake.catch_phrase() + " Fiduciaire"
    else:
        out = fake.company()

    add_name(input_text, "ORGANIZATION", out)
    return " {} ".format(out)


def fake_age(x, min_age=18, max_age=90):
    """
    Generate a fake age between the specified minimum and maximum ages.

    Parameters:
        x (str): Not used in the function. Can be any value.
        min_age (int, optional): The minimum age to generate. Default is 18.
        max_age (int, optional): The maximum age to generate. Default is 90.

    Returns:
        str: The generated fake age.
    """
    fake = Faker()
    today = date.today()
    birth_date = fake.date_of_birth(minimum_age=min_age, maximum_age=max_age)

    # Calculate the age based on the birth date and current date
    age = (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )
    return " {} ".format(age)


def fake_date(x):
    """
    Generate a fake date.

    Parameters:
        x (str): Not used in the function. Can be any value.

    Returns:
        str: The generated fake date in the format "DD.MM.YYYY".
    """
    fake = Faker("fr_CH")
    fake_date = fake.date_this_decade()
    return " {} ".format(fake_date.strftime("%d.%m.%Y"))


def fake_id(x, length=10):
    """
    Generate a fake ID of the specified length.

    Parameters:
        x (str): Not used in the function. Can be any value.
        length (int, optional): The length of the fake ID. Default is 10.

    Returns:
        str: The generated fake ID.
    """
    fake_id = check_name(x, "ID")
    if fake_id is not None:
        return " {} ".format(fake_id)
    characters = string.ascii_letters + string.digits
    # pragma: allowlist secret
    fake_id = "".join(random.choice(characters) for _ in range(length))  # nosec
    add_name(x, "ID", fake_id)
    return " {} ".format(fake_id)


def fake_url(x):
    """
    Generate a fake URL.

    Parameters:
        x (str): Not used in the function. Can be any value.

    Returns:
        str: The generated fake URL.
    """
    fake = check_name(x, "URL")
    if fake is not None:
        return " {} ".format(fake.url())
    fake = Faker("fr_CH")
    add_name(x, "URL", fake)
    return " {} ".format(fake.url())


def fake_email(x):
    """
    Generate a fake email address.

    Parameters:
        x (str): Not used in the function. Can be any value.

    Returns:
        str: The generated fake email address.
    """
    fake = check_name(x, "EMAIL_ADDRESS")
    if fake is not None:
        return " {} ".format(fake.url())
    fake = Faker("fr_CH")
    add_name(x, "EMAIL_ADDRESS", fake)
    return " {} ".format(fake.email())


def fake_swiss_zip_code(x):
    """
    Generate a fake Swiss ZIP code.

    Parameters:
        x (str): Not used in the function. Can be any value.

    Returns:
        str: The generated fake Swiss ZIP code.
    """
    fake = check_name(x, "CH_ZIPCODE")
    if fake is not None:
        return " {} ".format(fake.url())
    fake = Faker("fr_CH")
    add_name(x, "CH_ZIPCODE", fake)
    return ", {}, ".format(fake.postcode())


def fake_bank_account(x):
    """
    Generate a fake bank account number.

    Parameters:
        x (str): Not used in the function. Can be any value.

    Returns:
        str: The generated fake bank account number.
    """
    fake = check_name(x, "BANK_ACCOUNT")
    if fake is not None:
        return " {} ".format(fake.url())
    fake = Faker("fr_CH")
    add_name(x, "BANK_ACCOUNT", fake)
    return " {} ".format(fake.iban())


def fake_address_int(x):
    """
    Generate a fake address integer.

    Parameters:
        x (str): Not used in the function. Can be any value.

    Returns:
        str: The generated fake address integer.
    """
    return "{},".format(random.randint(1, 999))  # nosec
