#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from arbeitsflächeAnsicht import Tastatur


class hangulEingabePrüfung(unittest.TestCase):
    def setUp(selbstWert):
        selbstWert.textPuffer = ''
        def senden(Daten):
            for zeichenDaten in Daten.decode('utf-8'):
                if zeichenDaten == '\x7f': selbstWert.textPuffer = selbstWert.textPuffer[:-1]
                else: selbstWert.textPuffer += zeichenDaten
        selbstWert.tastaturEintrag = Tastatur(senden)

    def drückenTaste(selbstWert, symbolWert):
        selbstWert.tastaturEintrag.gedrücktWert(True, symbolWert)
        selbstWert.tastaturEintrag.gedrücktWert(False, symbolWert)

    def typKategorie(selbstWert, gedrücktTasten):
        for gedrücktWert in gedrücktTasten: selbstWert.drückenTaste(ord(gedrücktWert))

    def wörterPrüfung(selbstWert):
        for gedrücktTasten,erwartet in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with selbstWert.subTest(gedrücktTasten=gedrücktTasten):
                selbstWert.setUp(); selbstWert.drückenTaste(0xffc6); selbstWert.typKategorie(gedrücktTasten)
                selbstWert.assertEqual(selbstWert.textPuffer, erwartet)

    def rückschrittPrüfung(selbstWert):
        selbstWert.drückenTaste(0xff31); selbstWert.typKategorie('dlfr')
        selbstWert.assertEqual(selbstWert.textPuffer,'읽')
        for erwartet in ('일','이','ㅇ',''):
            selbstWert.drückenTaste(0xff08); selbstWert.assertEqual(selbstWert.textPuffer,erwartet)
        selbstWert.typKategorie('gksk'); selbstWert.assertEqual(selbstWert.textPuffer,'einsWert')
        selbstWert.drückenTaste(0xff08); selbstWert.assertEqual(selbstWert.textPuffer,'하ㄴ')

    def betriebsartenWiederholenUndBestätigenPrüfung(selbstWert):
        selbstWert.typKategorie('echo ')
        selbstWert.tastaturEintrag.gedrücktWert(True,0xffe1)
        selbstWert.tastaturEintrag.gedrücktWert(True,32); selbstWert.tastaturEintrag.gedrücktWert(True,32)
        selbstWert.tastaturEintrag.gedrücktWert(False,32); selbstWert.tastaturEintrag.gedrücktWert(False,0xffe1)
        selbstWert.assertTrue(selbstWert.tastaturEintrag.koreanisch)
        selbstWert.typKategorie('gksrmf'); selbstWert.drückenTaste(0xff31); selbstWert.typKategorie(' English')
        selbstWert.assertEqual(selbstWert.textPuffer,'echo 한글 English')
        selbstWert.assertFalse(selbstWert.tastaturEintrag.koreanisch)
        selbstWert.drückenTaste(0xffc6); selbstWert.typKategorie('rk'); selbstWert.drückenTaste(0xff51)
        selbstWert.typKategorie('sk'); selbstWert.assertTrue(selbstWert.textPuffer.endswith('ersterOperand\x1b[D나'))

    def einsetzenUndUnicodePrüfung(selbstWert):
        selbstWert.drückenTaste(0xffc6); selbstWert.typKategorie('rk')
        selbstWert.tastaturEintrag.zwischenablageWert='einsetzenWert'.encode()
        selbstWert.tastaturEintrag.gedrücktWert(True,0xffe3); selbstWert.tastaturEintrag.gedrücktWert(True,0xffe1)
        selbstWert.drückenTaste(ord('v'))
        selbstWert.tastaturEintrag.gedrücktWert(False,0xffe1); selbstWert.tastaturEintrag.gedrücktWert(False,0xffe3)
        selbstWert.drückenTaste(0x0100d55c); selbstWert.typKategorie('sk')
        selbstWert.assertEqual(selbstWert.textPuffer,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
