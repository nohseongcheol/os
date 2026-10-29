#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from namizje_Pogled import tipkovnica


class 한글입력시험(unittest.TestCase):
    def setUp(자신):
        자신.SMS_medpomnilnik = ''
        def poslati(podatki):
            for znakovni_podatki in podatki.decode('utf-8'):
                if znakovni_podatki == '\x7f': 자신.SMS_medpomnilnik = 자신.SMS_medpomnilnik[:-1]
                else: 자신.SMS_medpomnilnik += znakovni_podatki
        자신.tipkovnica_vnos = tipkovnica(poslati)

    def pritisniti_Ključ(자신, simbol_VALUE):
        자신.tipkovnica_vnos.누름값(True, simbol_VALUE)
        자신.tipkovnica_vnos.누름값(False, simbol_VALUE)

    def Tip_območje(자신, 누름열):
        for 누름값 in 누름열: 자신.pritisniti_Ključ(ord(누름값))

    def test_낱말(자신):
        for 누름열,예상결과 in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with 자신.subTest(누름열=누름열):
                자신.setUp(); 자신.pritisniti_Ključ(0xffc6); 자신.Tip_območje(누름열)
                자신.assertEqual(자신.SMS_medpomnilnik, 예상결과)

    def test_앞글자지우기(자신):
        자신.pritisniti_Ključ(0xff31); 자신.Tip_območje('dlfr')
        자신.assertEqual(자신.SMS_medpomnilnik,'읽')
        for 예상결과 in ('일','이','ㅇ',''):
            자신.pritisniti_Ključ(0xff08); 자신.assertEqual(자신.SMS_medpomnilnik,예상결과)
        자신.Tip_območje('gksk'); 자신.assertEqual(자신.SMS_medpomnilnik,'하나')
        자신.pritisniti_Ključ(0xff08); 자신.assertEqual(자신.SMS_medpomnilnik,'하ㄴ')

    def test_전환반복확정(자신):
        자신.Tip_območje('echo ')
        자신.tipkovnica_vnos.누름값(True,0xffe1)
        자신.tipkovnica_vnos.누름값(True,32); 자신.tipkovnica_vnos.누름값(True,32)
        자신.tipkovnica_vnos.누름값(False,32); 자신.tipkovnica_vnos.누름값(False,0xffe1)
        자신.assertTrue(자신.tipkovnica_vnos.한글여부)
        자신.Tip_območje('gksrmf'); 자신.pritisniti_Ključ(0xff31); 자신.Tip_območje(' English')
        자신.assertEqual(자신.SMS_medpomnilnik,'echo 한글 English')
        자신.assertFalse(자신.tipkovnica_vnos.한글여부)
        자신.pritisniti_Ključ(0xffc6); 자신.Tip_območje('rk'); 자신.pritisniti_Ključ(0xff51)
        자신.Tip_območje('sk'); 자신.assertTrue(자신.SMS_medpomnilnik.endswith('가\x1b[D나'))

    def preskusiti_prilepiti_AND_UNICODE(자신):
        자신.pritisniti_Ključ(0xffc6); 자신.Tip_območje('rk')
        자신.tipkovnica_vnos.odložišče_VALUE='prilepiti_VALUE'.encode()
        자신.tipkovnica_vnos.누름값(True,0xffe3); 자신.tipkovnica_vnos.누름값(True,0xffe1)
        자신.pritisniti_Ključ(ord('v'))
        자신.tipkovnica_vnos.누름값(False,0xffe1); 자신.tipkovnica_vnos.누름값(False,0xffe3)
        자신.pritisniti_Ključ(0x0100d55c); 자신.Tip_območje('sk')
        자신.assertEqual(자신.SMS_medpomnilnik,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
