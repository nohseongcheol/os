#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from desktop_vizualiza import tastatură


class 한글입력시험(unittest.TestCase):
    def setUp(자신):
        자신.SMS_tampon = ''
        def trimite(date):
            for date_de_tip_caracter in date.decode('utf-8'):
                if date_de_tip_caracter == '\x7f': 자신.SMS_tampon = 자신.SMS_tampon[:-1]
                else: 자신.SMS_tampon += date_de_tip_caracter
        자신.tastatură_intrare = tastatură(trimite)

    def apăsa_Cheie(자신, simbol_VALUE):
        자신.tastatură_intrare.누름값(True, simbol_VALUE)
        자신.tastatură_intrare.누름값(False, simbol_VALUE)

    def Tip_zonă(자신, 누름열):
        for 누름값 in 누름열: 자신.apăsa_Cheie(ord(누름값))

    def test_낱말(자신):
        for 누름열,예상결과 in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with 자신.subTest(누름열=누름열):
                자신.setUp(); 자신.apăsa_Cheie(0xffc6); 자신.Tip_zonă(누름열)
                자신.assertEqual(자신.SMS_tampon, 예상결과)

    def test_앞글자지우기(자신):
        자신.apăsa_Cheie(0xff31); 자신.Tip_zonă('dlfr')
        자신.assertEqual(자신.SMS_tampon,'읽')
        for 예상결과 in ('일','이','ㅇ',''):
            자신.apăsa_Cheie(0xff08); 자신.assertEqual(자신.SMS_tampon,예상결과)
        자신.Tip_zonă('gksk'); 자신.assertEqual(자신.SMS_tampon,'하나')
        자신.apăsa_Cheie(0xff08); 자신.assertEqual(자신.SMS_tampon,'하ㄴ')

    def test_전환반복확정(자신):
        자신.Tip_zonă('echo ')
        자신.tastatură_intrare.누름값(True,0xffe1)
        자신.tastatură_intrare.누름값(True,32); 자신.tastatură_intrare.누름값(True,32)
        자신.tastatură_intrare.누름값(False,32); 자신.tastatură_intrare.누름값(False,0xffe1)
        자신.assertTrue(자신.tastatură_intrare.한글여부)
        자신.Tip_zonă('gksrmf'); 자신.apăsa_Cheie(0xff31); 자신.Tip_zonă(' English')
        자신.assertEqual(자신.SMS_tampon,'echo 한글 English')
        자신.assertFalse(자신.tastatură_intrare.한글여부)
        자신.apăsa_Cheie(0xffc6); 자신.Tip_zonă('rk'); 자신.apăsa_Cheie(0xff51)
        자신.Tip_zonă('sk'); 자신.assertTrue(자신.SMS_tampon.endswith('가\x1b[D나'))

    def test_붙이기유니코드(자신):
        자신.apăsa_Cheie(0xffc6); 자신.Tip_zonă('rk')
        자신.tastatură_intrare.clipboard_VALUE='lipi_VALUE'.encode()
        자신.tastatură_intrare.누름값(True,0xffe3); 자신.tastatură_intrare.누름값(True,0xffe1)
        자신.apăsa_Cheie(ord('v'))
        자신.tastatură_intrare.누름값(False,0xffe1); 자신.tastatură_intrare.누름값(False,0xffe3)
        자신.apăsa_Cheie(0x0100d55c); 자신.Tip_zonă('sk')
        자신.assertEqual(자신.SMS_tampon,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
