#
# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Théophile Gentilhomme <theophile.gentilhomme@idiap.ch>
#
# SPDX-License-Identifier: LicenseRef-anonymization
#
# anonymization: Text ner and pii
#


def gen_default_config():
    """
    Generate default configuration file for anonymization.
    """
    out = {
        "language": "fr",
        "use_camembert": True,
        "use_swiss_ner": True,
        "use_spacy": True,
        "entities": [
            "PERSON",
            "LOCATION",
            "ADDRESS_NUMBER",
            "DATE_TIME",
            "BANK_ACCOUNT",
            "CH_ZIPCODE",
            "ORGANIZATION",
            "EMAIL_ADDRESS",
            "PHONE_NUMBER",
            "ID",
            "MISC",
            "URL",
        ],
        "pseudonymize": [
            # "PERSON",
            # "DATE_TIME",
            # "ORGANIZATION",
            # "LOCATION",
        ],
        "flag_only": True,
        "process_columns": [5],
    }
    return out
