#
# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Théophile Gentilhomme <theophile.gentilhomme@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#
# anonymization: Text ner and pii
#


import os

config_dir = os.path.abspath(os.path.dirname(__file__))
models_config_paths = {
    "config_camemBERT": f"{config_dir}/../tests/config_camemBERT.yml"
}
