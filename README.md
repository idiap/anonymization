# Anonymization

Text anonymization is a Python library for anonymizing sensitive information in text data. Focused on Swiss French banking data.

Based on presidio for PII detection and [camembert](https://huggingface.co/Jean-Baptiste/camembert-ner-with-dates) for NER.


## Install

You must have [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) and [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed.

Create a conda environment with python 3.10 and activate it:

```bash
conda create -n my_env python=3.10
conda activate my_env
```

Clone the project and install it:

```bash
git clone https://github.com/idiap/anonymization.git
cd anonymization
pip install -e . # install in editable mode
configure  # Download models
pytest -sv tests  # (optional) run the test suite to make sure everything is working as expected
```

## Quick start

Anonymize your text (.txt), CSV (.csv) or Excel (.xslx) `/path/to/my_file.xslx` file by calling:

```bash
anonymize -f /path/to/my_file.xslx
```
This generates an anonymized file here `/path/to/my_file_anonymized.xslx`

You can use the test example:
```bash
anoymize -f ./tests/example.txt -c ./tests/config.json
```

## Advanced configuration

You can pass a customized configuration to run your anonymization.

To generate a default configuration file (used by default when running anonymize):
```bash
gen_config
```
This creates `.json` file with the following fields:
| Keyword | Description |
| --------------- | --------------- |
| entities | List of entites you want to anonymize. By default it listed all the available entities. For example: "Mon nom est Alfred, voici mon numéro: 079563684" results in "Mon nom est <ANONYM_PER>, voici mon numéro <ANONYM_PHONE>"|
| flag_only | Boolean. If True, the anonymization will only flag sensitive component of the text but will not remove them. For example: "Mon nom est Alfred, voici mon numéro: 079563684" results in "Mon nom est <FLAG Alfred>, voici mon numéro <FLAG 079563684>".
| language | Language selection in "fr", "en", "de". However, the current version is specialized for French language.|
| process_columns | List of integers. If your input file is an Excel of CSV file, the anonymization is only applied to the specified columns of the data. |
| pseudonymize | List of entities to pseudomize, i.e. replace the flaged text with fake one (e.g. use fake names). Should list entities already present in entities list. Entities that are not pseudomized are anonymized. For example, if onle "PERSON" is given to pseudonymize: "Mon nom est Alfred, voici mon numéro: 079563684" results in "Mon nom est Bernard, voici mon numéro <ANONYM_PHONE>"|
| use_camembert | Boolean. If true, use french camembert_ner for NER recognition. Detectors are cumulative (default all used).|
| use_spacy | Boolean. If true, use spacy for NER and PII detection. Detectors are cumulative (default all used).|
| use_swiss_ner | Boolean. If true, use spacy for NER sepcialized in Swiss entity recognition. Detectors are cumulative (default all used). |


To use a constomized `config.json` configuration file:
```bash
anonymize -f /path/to/my_file.xslx -c config.json
```

For more help:
```bash
anonymize -h
```

# DECLARATIONS

Please be advised that the use of this code comes with no guarantees or warranties. Users are responsible for its application, and no liability is assumed by the developer for any consequences arising from its use.

# ACKNOWLEDGEMENTS

This package was developed with the support of the Banque Cantonale du Valais (BCVs).

# LICENCE

SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Théophile Gentilhomme <theophile.gentilhomme@idiap.ch>

SPDX-License-Identifier: GPL-3.0-only
