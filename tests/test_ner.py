#
# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Théophile Gentilhomme <theophile.gentilhomme@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#
# anonymization: Text ner and pii
#

import unittest

from transformers import pipeline


class TestAttention(unittest.TestCase):
    def test_ner(self):
        ner = pipeline(
            task="ner",
            model="Jean-Baptiste/camembert-ner-with-dates",
            tokenizer="Jean-Baptiste/camembert-ner-with-dates",
            aggregation_strategy="simple",
        )
        result = ner(
            """Boulanger, habitant à Boulanger,
            au chemin du Bouchot 26, 1889, Etoy
            et travaillant dans
            le magasin Boulanger situé dans la ville de Boulanger.
            Boulanger a écrit le livre éponyme Boulanger édité par
            la maison d'édition Boulanger. Som numéro de téléphone
            est 0763252698. Son compte bancaire CH756625551233 chez UBS.
            Vous pouvez également le contacter à cette adresse b.azur@youpi.com.
            Quentin Jerome Tarantino naît le 27 mars 1963 à Knoxville,
            dans le Tennessee. Il est le fils de Connie McHugh,
            une infirmière, née le 3 septembre 1946, et de Tony Tarantino,
            acteur et musicien amateur né à New York. Ce dernier
            est d'origine italienne par son père ; sa mère a des ascendances
            irlandaises et cherokees. Il est prénommé d'après Quint Asper,
            le personnage joué par Burt Reynolds dans la série Gunsmoke
            et Quentin Compson, personnage du roman Le Bruit et la Fureur.
            Son père quitte le domicile familial avant même sa naissance.
            En 1965, sa mère déménage à Torrance, dans la banlieue sud de
            Los Angeles, et se remarie avec Curtis Zastoupil, un pianiste
            de bar, qui lui fait découvrir le cinéma. Le couple divorce
            alors que le jeune Quentin a une dizaine d'années.
            """
        )
        print(result)

    def test_swiss_ner(self):
        token_classifier = pipeline(
            model="ZurichNLP/swissbert-ner",
            aggregation_strategy="simple",
        )

        token_classifier.model.set_default_language("de_CH")
        res = token_classifier("Mein Name sei Gantenbein.")
        print(res)

        token_classifier.model.set_default_language("fr_CH")
        results = token_classifier("J'habite à Lausanne.")
        print(results)


if __name__ == "__main__":
    unittest.main()
