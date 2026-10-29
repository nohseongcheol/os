#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from desktop_Pamja import tastiera


class 한글입력시험(unittest.TestCase):
    def setUp(자신):
        자신.SMS_ndërmemorie = ''
        def dërgoj(të_dhëna):
            for karakter_të_dhëna in të_dhëna.decode('utf-8'):
                if karakter_të_dhëna == '\x7f': 자신.SMS_ndërmemorie = 자신.SMS_ndërmemorie[:-1]
                else: 자신.SMS_ndërmemorie += karakter_të_dhëna
        자신.tastiera_futje = tastiera(dërgoj)

    def shtyp_tast(자신, simbol_VALUE):
        자신.tastiera_futje.누름값(True, simbol_VALUE)
        자신.tastiera_futje.누름값(False, simbol_VALUE)

    def TYPE_kategori(자신, 누름열):
        for 누름값 in 누름열: 자신.shtyp_tast(ord(누름값))

    def test_낱말(자신):
        for 누름열,예상결과 in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with 자신.subTest(누름열=누름열):
                자신.setUp(); 자신.shtyp_tast(0xffc6); 자신.TYPE_kategori(누름열)
                자신.assertEqual(자신.SMS_ndërmemorie, 예상결과)

    def test_앞글자지우기(자신):
        자신.shtyp_tast(0xff31); 자신.TYPE_kategori('dlfr')
        자신.assertEqual(자신.SMS_ndërmemorie,'읽')
        for 예상결과 in ('일','이','ㅇ',''):
            자신.shtyp_tast(0xff08); 자신.assertEqual(자신.SMS_ndërmemorie,예상결과)
        자신.TYPE_kategori('gksk'); 자신.assertEqual(자신.SMS_ndërmemorie,'하나')
        자신.shtyp_tast(0xff08); 자신.assertEqual(자신.SMS_ndërmemorie,'하ㄴ')

    def test_전환반복확정(자신):
        자신.TYPE_kategori('echo ')
        자신.tastiera_futje.누름값(True,0xffe1)
        자신.tastiera_futje.누름값(True,32); 자신.tastiera_futje.누름값(True,32)
        자신.tastiera_futje.누름값(False,32); 자신.tastiera_futje.누름값(False,0xffe1)
        자신.assertTrue(자신.tastiera_futje.한글여부)
        자신.TYPE_kategori('gksrmf'); 자신.shtyp_tast(0xff31); 자신.TYPE_kategori(' English')
        자신.assertEqual(자신.SMS_ndërmemorie,'echo 한글 English')
        자신.assertFalse(자신.tastiera_futje.한글여부)
        자신.shtyp_tast(0xffc6); 자신.TYPE_kategori('rk'); 자신.shtyp_tast(0xff51)
        자신.TYPE_kategori('sk'); 자신.assertTrue(자신.SMS_ndërmemorie.endswith('가\x1b[D나'))

    def test_붙이기유니코드(자신):
        자신.shtyp_tast(0xffc6); 자신.TYPE_kategori('rk')
        자신.tastiera_futje.kujtesa_e_fragmenteve_VALUE='ngjit_VALUE'.encode()
        자신.tastiera_futje.누름값(True,0xffe3); 자신.tastiera_futje.누름값(True,0xffe1)
        자신.shtyp_tast(ord('v'))
        자신.tastiera_futje.누름값(False,0xffe1); 자신.tastiera_futje.누름값(False,0xffe3)
        자신.shtyp_tast(0x0100d55c); 자신.TYPE_kategori('sk')
        자신.assertEqual(자신.SMS_ndërmemorie,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
