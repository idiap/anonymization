#
# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Théophile Gentilhomme <theophile.gentilhomme@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#
# anonymization: Text ner and pii
#


from presidio_anonymizer.entities import OperatorConfig

from anonymization.pii.fake_gen import fake_address_int
from anonymization.pii.fake_gen import fake_age
from anonymization.pii.fake_gen import fake_bank_account
from anonymization.pii.fake_gen import fake_date
from anonymization.pii.fake_gen import fake_email
from anonymization.pii.fake_gen import fake_id
from anonymization.pii.fake_gen import fake_name
from anonymization.pii.fake_gen import fake_phone
from anonymization.pii.fake_gen import fake_swiss_french_organization
from anonymization.pii.fake_gen import fake_swiss_location
from anonymization.pii.fake_gen import fake_swiss_zip_code
from anonymization.pii.fake_gen import fake_url

OPS = {
    "DEFAULT": OperatorConfig("replace", {"new_value": " <ANONYMIZED>"}),
    "PHONE_NUMBER": OperatorConfig("replace", {"new_value": " <ANONYM_PHONE>"}),
    "PERSON": OperatorConfig("replace", {"new_value": " <ANONYM_PER>"}),
    "LOCATION": OperatorConfig("replace", {"new_value": " <ANONYM_LOC>"}),
    "ORGANIZATION": OperatorConfig("replace", {"new_value": " <ANONYM_ORG>"}),
    "AGE": OperatorConfig("replace", {"new_value": " <ANONYM_AGE>"}),
    "DATE_TIME": OperatorConfig("replace", {"new_value": " <ANONYM_DATE_TIME>"}),
    "ID": OperatorConfig("replace", {"new_value": " <ANONYM_ID>"}),
    "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": " <ANONYM_EMAIL>"}),
    "URL": OperatorConfig("replace", {"new_value": " <ANONYM_URL>"}),
    "CH_ZIPCODE": OperatorConfig("replace", {"new_value": " <ANONYM_ZIP>"}),
    "BANK_ACCOUNT": OperatorConfig("replace", {"new_value": " <ANONYM_BK_ACCOUNT>"}),
    "ADDRESS_NUMBER": OperatorConfig("replace", {"new_value": " <ANONYM_ADS_NUM>"}),
}


OPS_FAKE = {
    "PERSON": OperatorConfig("custom", {"lambda": fake_name}),
    "PHONE_NUMBER": OperatorConfig("custom", {"lambda": fake_phone}),
    "AGE": OperatorConfig("custom", {"lambda": fake_age}),
    "LOCATION": OperatorConfig("custom", {"lambda": fake_swiss_location}),
    "ORGANIZATION": OperatorConfig(
        "custom", {"lambda": fake_swiss_french_organization}
    ),
    "DATE_TIME": OperatorConfig("custom", {"lambda": fake_date}),
    "ID": OperatorConfig("custom", {"lambda": fake_id}),
    "EMAIL_ADDRESS": OperatorConfig("custom", {"lambda": fake_email}),
    "URL": OperatorConfig("custom", {"lambda": fake_url}),
    "CH_ZIPCODE": OperatorConfig("custom", {"lambda": fake_swiss_zip_code}),
    "BANK_ACCOUNT": OperatorConfig("custom", {"lambda": fake_bank_account}),
    "ADDRESS_NUMBER": OperatorConfig("custom", {"lambda": fake_address_int}),
}


def flag(x):
    return " <FLAG {}> ".format(x)


OPS_FLAG = {
    "PERSON": OperatorConfig("custom", {"lambda": flag}),
    "PHONE_NUMBER": OperatorConfig("custom", {"lambda": flag}),
    "AGE": OperatorConfig("custom", {"lambda": fake_age}),
    "LOCATION": OperatorConfig("custom", {"lambda": flag}),
    "ORGANIZATION": OperatorConfig("custom", {"lambda": flag}),
    "DATE_TIME": OperatorConfig("custom", {"lambda": flag}),
    "ID": OperatorConfig("custom", {"lambda": flag}),
    "EMAIL_ADDRESS": OperatorConfig("custom", {"lambda": flag}),
    "URL": OperatorConfig("custom", {"lambda": flag}),
    "CH_ZIPCODE": OperatorConfig("custom", {"lambda": flag}),
    "BANK_ACCOUNT": OperatorConfig("custom", {"lambda": flag}),
    "ADDRESS_NUMBER": OperatorConfig("custom", {"lambda": flag}),
}


def gen_operators(config):
    """Generate anonymization operators based on configuration.

    Args:
        config (dict): Configuration

    Returns:
        dict: OperatorConfig
    """
    out = {
        "DEFAULT": OperatorConfig("replace", {"new_value": " <ANONYMIZED>"}),
    }
    if config.get("flag_only", False):
        return OPS_FLAG

    for item in config.get("pseudonymize", []):
        if item in OPS_FAKE:
            out[item] = OPS_FAKE[item]
    for item, value in OPS.items():
        if item not in out:
            out[item] = value
    return out
