#
# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Théophile Gentilhomme <theophile.gentilhomme@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#
# anonymization: Text ner and pii
#

from .custom_recognizer import BankAcount  # noqa: F401
from .custom_recognizer import SwissZipCode  # noqa: F401
from .pii import Anonymize  # noqa: F401
from .pii import PIIDetection  # noqa: F401
