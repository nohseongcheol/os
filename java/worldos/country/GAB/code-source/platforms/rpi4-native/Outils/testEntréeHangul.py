#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from vueBureau import Clavier


class testEntréeHangul(unittest.TestCase):
    def setUp(valeurSoi):
        valeurSoi.tamponTexte = ''
        def envoyer(Données):
            for donnéesCaractère in Données.decode('utf-8'):
                if donnéesCaractère == '\x7f': valeurSoi.tamponTexte = valeurSoi.tamponTexte[:-1]
                else: valeurSoi.tamponTexte += donnéesCaractère
        valeurSoi.entréeÉlémentClavier = Clavier(envoyer)

    def toucheEnfoncer(valeurSoi, valeurSymbole):
        valeurSoi.entréeÉlémentClavier.valeurEnfoncé(True, valeurSymbole)
        valeurSoi.entréeÉlémentClavier.valeurEnfoncé(False, valeurSymbole)

    def catégorieType(valeurSoi, touchesEnfoncé):
        for valeurEnfoncé in touchesEnfoncé: valeurSoi.toucheEnfoncer(ord(valeurEnfoncé))

    def testMots(valeurSoi):
        for touchesEnfoncé,attendu in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with valeurSoi.subTest(touchesEnfoncé=touchesEnfoncé):
                valeurSoi.setUp(); valeurSoi.toucheEnfoncer(0xffc6); valeurSoi.catégorieType(touchesEnfoncé)
                valeurSoi.assertEqual(valeurSoi.tamponTexte, attendu)

    def testRetourArrière(valeurSoi):
        valeurSoi.toucheEnfoncer(0xff31); valeurSoi.catégorieType('dlfr')
        valeurSoi.assertEqual(valeurSoi.tamponTexte,'읽')
        for attendu in ('일','이','ㅇ',''):
            valeurSoi.toucheEnfoncer(0xff08); valeurSoi.assertEqual(valeurSoi.tamponTexte,attendu)
        valeurSoi.catégorieType('gksk'); valeurSoi.assertEqual(valeurSoi.tamponTexte,'valeurUn')
        valeurSoi.toucheEnfoncer(0xff08); valeurSoi.assertEqual(valeurSoi.tamponTexte,'하ㄴ')

    def testConfirmerEtRépéterModes(valeurSoi):
        valeurSoi.catégorieType('echo ')
        valeurSoi.entréeÉlémentClavier.valeurEnfoncé(True,0xffe1)
        valeurSoi.entréeÉlémentClavier.valeurEnfoncé(True,32); valeurSoi.entréeÉlémentClavier.valeurEnfoncé(True,32)
        valeurSoi.entréeÉlémentClavier.valeurEnfoncé(False,32); valeurSoi.entréeÉlémentClavier.valeurEnfoncé(False,0xffe1)
        valeurSoi.assertTrue(valeurSoi.entréeÉlémentClavier.coréen)
        valeurSoi.catégorieType('gksrmf'); valeurSoi.toucheEnfoncer(0xff31); valeurSoi.catégorieType(' English')
        valeurSoi.assertEqual(valeurSoi.tamponTexte,'echo 한글 English')
        valeurSoi.assertFalse(valeurSoi.entréeÉlémentClavier.coréen)
        valeurSoi.toucheEnfoncer(0xffc6); valeurSoi.catégorieType('rk'); valeurSoi.toucheEnfoncer(0xff51)
        valeurSoi.catégorieType('sk'); valeurSoi.assertTrue(valeurSoi.tamponTexte.endswith('opérandePremier\x1b[D나'))

    def testUnicodeEtColler(valeurSoi):
        valeurSoi.toucheEnfoncer(0xffc6); valeurSoi.catégorieType('rk')
        valeurSoi.entréeÉlémentClavier.valeurPressePapiers='valeurColler'.encode()
        valeurSoi.entréeÉlémentClavier.valeurEnfoncé(True,0xffe3); valeurSoi.entréeÉlémentClavier.valeurEnfoncé(True,0xffe1)
        valeurSoi.toucheEnfoncer(ord('v'))
        valeurSoi.entréeÉlémentClavier.valeurEnfoncé(False,0xffe1); valeurSoi.entréeÉlémentClavier.valeurEnfoncé(False,0xffe3)
        valeurSoi.toucheEnfoncer(0x0100d55c); valeurSoi.catégorieType('sk')
        valeurSoi.assertEqual(valeurSoi.tamponTexte,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
