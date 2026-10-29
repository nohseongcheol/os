#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from työpöytä_Näkymä import näppäimistö


class 한글입력시험(unittest.TestCase):
    def setUp(자신):
        자신.SMS_puskuri = ''
        def lähettää(data):
            for merkkitiedot in data.decode('utf-8'):
                if merkkitiedot == '\x7f': 자신.SMS_puskuri = 자신.SMS_puskuri[:-1]
                else: 자신.SMS_puskuri += merkkitiedot
        자신.näppäimistö_merkintä = näppäimistö(lähettää)

    def paina_Avain(자신, symboli_ARVO):
        자신.näppäimistö_merkintä.누름값(True, symboli_ARVO)
        자신.näppäimistö_merkintä.누름값(False, symboli_ARVO)

    def TYYPPI_alue(자신, 누름열):
        for 누름값 in 누름열: 자신.paina_Avain(ord(누름값))

    def test_낱말(자신):
        for 누름열,예상결과 in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with 자신.subTest(누름열=누름열):
                자신.setUp(); 자신.paina_Avain(0xffc6); 자신.TYYPPI_alue(누름열)
                자신.assertEqual(자신.SMS_puskuri, 예상결과)

    def test_앞글자지우기(자신):
        자신.paina_Avain(0xff31); 자신.TYYPPI_alue('dlfr')
        자신.assertEqual(자신.SMS_puskuri,'읽')
        for 예상결과 in ('일','이','ㅇ',''):
            자신.paina_Avain(0xff08); 자신.assertEqual(자신.SMS_puskuri,예상결과)
        자신.TYYPPI_alue('gksk'); 자신.assertEqual(자신.SMS_puskuri,'하나')
        자신.paina_Avain(0xff08); 자신.assertEqual(자신.SMS_puskuri,'하ㄴ')

    def test_전환반복확정(자신):
        자신.TYYPPI_alue('echo ')
        자신.näppäimistö_merkintä.누름값(True,0xffe1)
        자신.näppäimistö_merkintä.누름값(True,32); 자신.näppäimistö_merkintä.누름값(True,32)
        자신.näppäimistö_merkintä.누름값(False,32); 자신.näppäimistö_merkintä.누름값(False,0xffe1)
        자신.assertTrue(자신.näppäimistö_merkintä.한글여부)
        자신.TYYPPI_alue('gksrmf'); 자신.paina_Avain(0xff31); 자신.TYYPPI_alue(' English')
        자신.assertEqual(자신.SMS_puskuri,'echo 한글 English')
        자신.assertFalse(자신.näppäimistö_merkintä.한글여부)
        자신.paina_Avain(0xffc6); 자신.TYYPPI_alue('rk'); 자신.paina_Avain(0xff51)
        자신.TYYPPI_alue('sk'); 자신.assertTrue(자신.SMS_puskuri.endswith('가\x1b[D나'))

    def testi_liitä_JA_UNICODE(자신):
        자신.paina_Avain(0xffc6); 자신.TYYPPI_alue('rk')
        자신.näppäimistö_merkintä.leikepöytä_ARVO='liitä_ARVO_8e45bfbb'.encode()
        자신.näppäimistö_merkintä.누름값(True,0xffe3); 자신.näppäimistö_merkintä.누름값(True,0xffe1)
        자신.paina_Avain(ord('v'))
        자신.näppäimistö_merkintä.누름값(False,0xffe1); 자신.näppäimistö_merkintä.누름값(False,0xffe3)
        자신.paina_Avain(0x0100d55c); 자신.TYYPPI_alue('sk')
        자신.assertEqual(자신.SMS_puskuri,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
