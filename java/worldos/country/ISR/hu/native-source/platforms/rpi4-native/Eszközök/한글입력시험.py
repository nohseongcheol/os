#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from Asztal_Nézet import billentyűzet


class 한글입력시험(unittest.TestCase):
    def setUp(자신):
        자신.SMS_puffer = ''
        def küld(adat):
            for karakteres_adat in adat.decode('utf-8'):
                if karakteres_adat == '\x7f': 자신.SMS_puffer = 자신.SMS_puffer[:-1]
                else: 자신.SMS_puffer += karakteres_adat
        자신.billentyűzet_bejegyzés = billentyűzet(küld)

    def 글쇠누르기(자신, szimbólum_ÉRTÉK):
        자신.billentyűzet_bejegyzés.누름값(True, szimbólum_ÉRTÉK)
        자신.billentyűzet_bejegyzés.누름값(False, szimbólum_ÉRTÉK)

    def beír_terület(자신, 누름열):
        for 누름값 in 누름열: 자신.글쇠누르기(ord(누름값))

    def test_낱말(자신):
        for 누름열,예상결과 in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with 자신.subTest(누름열=누름열):
                자신.setUp(); 자신.글쇠누르기(0xffc6); 자신.beír_terület(누름열)
                자신.assertEqual(자신.SMS_puffer, 예상결과)

    def test_앞글자지우기(자신):
        자신.글쇠누르기(0xff31); 자신.beír_terület('dlfr')
        자신.assertEqual(자신.SMS_puffer,'읽')
        for 예상결과 in ('일','이','ㅇ',''):
            자신.글쇠누르기(0xff08); 자신.assertEqual(자신.SMS_puffer,예상결과)
        자신.beír_terület('gksk'); 자신.assertEqual(자신.SMS_puffer,'하나')
        자신.글쇠누르기(0xff08); 자신.assertEqual(자신.SMS_puffer,'하ㄴ')

    def test_전환반복확정(자신):
        자신.beír_terület('echo ')
        자신.billentyűzet_bejegyzés.누름값(True,0xffe1)
        자신.billentyűzet_bejegyzés.누름값(True,32); 자신.billentyűzet_bejegyzés.누름값(True,32)
        자신.billentyűzet_bejegyzés.누름값(False,32); 자신.billentyűzet_bejegyzés.누름값(False,0xffe1)
        자신.assertTrue(자신.billentyűzet_bejegyzés.한글여부)
        자신.beír_terület('gksrmf'); 자신.글쇠누르기(0xff31); 자신.beír_terület(' English')
        자신.assertEqual(자신.SMS_puffer,'echo 한글 English')
        자신.assertFalse(자신.billentyűzet_bejegyzés.한글여부)
        자신.글쇠누르기(0xffc6); 자신.beír_terület('rk'); 자신.글쇠누르기(0xff51)
        자신.beír_terület('sk'); 자신.assertTrue(자신.SMS_puffer.endswith('가\x1b[D나'))

    def teszt_beilleszt_ÉS_UNICODE(자신):
        자신.글쇠누르기(0xffc6); 자신.beír_terület('rk')
        자신.billentyűzet_bejegyzés.vágólap_ÉRTÉK='beilleszt_ÉRTÉK'.encode()
        자신.billentyűzet_bejegyzés.누름값(True,0xffe3); 자신.billentyűzet_bejegyzés.누름값(True,0xffe1)
        자신.글쇠누르기(ord('v'))
        자신.billentyűzet_bejegyzés.누름값(False,0xffe1); 자신.billentyűzet_bejegyzés.누름값(False,0xffe3)
        자신.글쇠누르기(0x0100d55c); 자신.beír_terület('sk')
        자신.assertEqual(자신.SMS_puffer,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
