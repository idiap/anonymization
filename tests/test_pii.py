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

from anonymization.pii import Anonymize
from anonymization.pii import PIIDetection
from anonymization.pii.anonym_ops import gen_operators
from anonymization.pii.config import gen_default_config


class TestAttention(unittest.TestCase):
    def test_ner(self):
        text = """Boulanger, habitant à Boulanger,
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
        irlandaises et cherokees.

        Il est prénommé d'après Quint Asper,
        le personnage joué par Burt Reynolds dans la série Gunsmoke
        et Quentin Compson, personnage du roman Le Bruit et la Fureur.
        Son père quitte le domicile familial avant même sa naissance.
        En 1965, sa mère déménage à Torrance, dans la banlieue sud de
        Los Angeles, et se remarie avec Curtis Zastoupil, un pianiste
        de bar, qui lui fait découvrir le cinéma.
        Le couple divorce
        alors que le jeune Quentin a une dizaine d'années.

        M. Japser a fait un virement sur son compte Crédit Suisse de 30 CHF.
        Mme Japser aimerait mettre tous leurs fonds à la BCVs. Le compte joint
        est CH255562366441.
        """
        detector = PIIDetection()
        results = detector.analyse(text)
        for result in results:
            print(f"- {text[result.start:result.end]} as {result.entity_type}")

        print("Pseudomization:")
        anonym = Anonymize(operators=gen_operators(config=gen_default_config()))
        final = anonym.anonymise(text, results)
        print(final)


if __name__ == "__main__":
    unittest.main()
