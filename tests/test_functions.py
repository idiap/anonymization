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

from anonymization.translate import Translator


class TestAttention(unittest.TestCase):
    def test_translate(self):
        translator = Translator("fr", "en")
        input = """
            Dans le courant d'une onde pure.
            Un Loup survient à jeun qui cherchait aventure,
            Et que la faim en ces lieux attirait.
            Qui te rend si hardi de troubler mon breuvage ?
            Dit cet animal plein de rage :
            Tu seras châtié de ta témérité.
            - Sire, répond l'Agneau, que votre Majesté
            Ne se mette pas en colère ;
            Mais plutôt qu'elle considère
            Que je me vas désaltérant
            Dans le courant,
            Plus de vingt pas au-dessous d'Elle,
            Et que par conséquent, en aucune façon,
            Je ne puis troubler sa boisson.
            - Tu la troubles, reprit cette bête cruelle,
            Et je sais que de moi tu médis l'an passé.
            - Comment l'aurais-je fait si je n'étais pas né ?
            Reprit l'Agneau, je tette encor ma mère.
            - Si ce n'est toi, c'est donc ton frère.
            - Je n'en ai point. - C'est donc quelqu'un des tiens :
            Car vous ne m'épargnez guère,
            Vous, vos bergers, et vos chiens.
            On me l'a dit : il faut que je me venge.
            Là-dessus, au fond des forêts
            Le Loup l'emporte, et puis le mange,
            Sans autre forme de procès.
        """
        print(input)
        out = translator(input)
        print(out)
        translator2 = Translator("en", "fr")
        out = translator2(out)
        print(out)


if __name__ == "__main__":
    unittest.main()
