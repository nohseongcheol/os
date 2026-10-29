#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from dators_Skats import tastatūra


class 한글입력시험(unittest.TestCase):
    def setUp(자신):
        자신.SMS_buferis = ''
        def sūtīt(dati):
            for rakstzīmju_dati in dati.decode('utf-8'):
                if rakstzīmju_dati == '\x7f': 자신.SMS_buferis = 자신.SMS_buferis[:-1]
                else: 자신.SMS_buferis += rakstzīmju_dati
        자신.tastatūra_ievade = tastatūra(sūtīt)

    def nospiest_Atslēga(자신, simbols_VALUE):
        자신.tastatūra_ievade.누름값(True, simbols_VALUE)
        자신.tastatūra_ievade.누름값(False, simbols_VALUE)

    def TYPE_joma(자신, 누름열):
        for 누름값 in 누름열: 자신.nospiest_Atslēga(ord(누름값))

    def test_낱말(자신):
        for 누름열,예상결과 in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with 자신.subTest(누름열=누름열):
                자신.setUp(); 자신.nospiest_Atslēga(0xffc6); 자신.TYPE_joma(누름열)
                자신.assertEqual(자신.SMS_buferis, 예상결과)

    def test_앞글자지우기(자신):
        자신.nospiest_Atslēga(0xff31); 자신.TYPE_joma('dlfr')
        자신.assertEqual(자신.SMS_buferis,'읽')
        for 예상결과 in ('일','이','ㅇ',''):
            자신.nospiest_Atslēga(0xff08); 자신.assertEqual(자신.SMS_buferis,예상결과)
        자신.TYPE_joma('gksk'); 자신.assertEqual(자신.SMS_buferis,'하나')
        자신.nospiest_Atslēga(0xff08); 자신.assertEqual(자신.SMS_buferis,'하ㄴ')

    def test_전환반복확정(자신):
        자신.TYPE_joma('echo ')
        자신.tastatūra_ievade.누름값(True,0xffe1)
        자신.tastatūra_ievade.누름값(True,32); 자신.tastatūra_ievade.누름값(True,32)
        자신.tastatūra_ievade.누름값(False,32); 자신.tastatūra_ievade.누름값(False,0xffe1)
        자신.assertTrue(자신.tastatūra_ievade.한글여부)
        자신.TYPE_joma('gksrmf'); 자신.nospiest_Atslēga(0xff31); 자신.TYPE_joma(' English')
        자신.assertEqual(자신.SMS_buferis,'echo 한글 English')
        자신.assertFalse(자신.tastatūra_ievade.한글여부)
        자신.nospiest_Atslēga(0xffc6); 자신.TYPE_joma('rk'); 자신.nospiest_Atslēga(0xff51)
        자신.TYPE_joma('sk'); 자신.assertTrue(자신.SMS_buferis.endswith('가\x1b[D나'))

    def test_붙이기유니코드(자신):
        자신.nospiest_Atslēga(0xffc6); 자신.TYPE_joma('rk')
        자신.tastatūra_ievade.starpliktuve_VALUE='ielīmēt_VALUE'.encode()
        자신.tastatūra_ievade.누름값(True,0xffe3); 자신.tastatūra_ievade.누름값(True,0xffe1)
        자신.nospiest_Atslēga(ord('v'))
        자신.tastatūra_ievade.누름값(False,0xffe1); 자신.tastatūra_ievade.누름값(False,0xffe3)
        자신.nospiest_Atslēga(0x0100d55c); 자신.TYPE_joma('sk')
        자신.assertEqual(자신.SMS_buferis,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
