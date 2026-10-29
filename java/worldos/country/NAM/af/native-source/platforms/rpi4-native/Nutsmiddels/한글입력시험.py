#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from werkskerm_bekyk import sleutelbord


class 한글입력시험(unittest.TestCase):
    def setUp(자신):
        자신.SMS_buffer = ''
        def e_pos(data):
            for karakter_data in data.decode('utf-8'):
                if karakter_data == '\x7f': 자신.SMS_buffer = 자신.SMS_buffer[:-1]
                else: 자신.SMS_buffer += karakter_data
        자신.sleutelbord_inskrywing = sleutelbord(e_pos)

    def druk_Sleutel(자신, simbool_VALUE):
        자신.sleutelbord_inskrywing.누름값(True, simbool_VALUE)
        자신.sleutelbord_inskrywing.누름값(False, simbool_VALUE)

    def TYPE_kategorie(자신, 누름열):
        for 누름값 in 누름열: 자신.druk_Sleutel(ord(누름값))

    def test_낱말(자신):
        for 누름열,예상결과 in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with 자신.subTest(누름열=누름열):
                자신.setUp(); 자신.druk_Sleutel(0xffc6); 자신.TYPE_kategorie(누름열)
                자신.assertEqual(자신.SMS_buffer, 예상결과)

    def test_앞글자지우기(자신):
        자신.druk_Sleutel(0xff31); 자신.TYPE_kategorie('dlfr')
        자신.assertEqual(자신.SMS_buffer,'읽')
        for 예상결과 in ('일','이','ㅇ',''):
            자신.druk_Sleutel(0xff08); 자신.assertEqual(자신.SMS_buffer,예상결과)
        자신.TYPE_kategorie('gksk'); 자신.assertEqual(자신.SMS_buffer,'하나')
        자신.druk_Sleutel(0xff08); 자신.assertEqual(자신.SMS_buffer,'하ㄴ')

    def test_전환반복확정(자신):
        자신.TYPE_kategorie('echo ')
        자신.sleutelbord_inskrywing.누름값(True,0xffe1)
        자신.sleutelbord_inskrywing.누름값(True,32); 자신.sleutelbord_inskrywing.누름값(True,32)
        자신.sleutelbord_inskrywing.누름값(False,32); 자신.sleutelbord_inskrywing.누름값(False,0xffe1)
        자신.assertTrue(자신.sleutelbord_inskrywing.한글여부)
        자신.TYPE_kategorie('gksrmf'); 자신.druk_Sleutel(0xff31); 자신.TYPE_kategorie(' English')
        자신.assertEqual(자신.SMS_buffer,'echo 한글 English')
        자신.assertFalse(자신.sleutelbord_inskrywing.한글여부)
        자신.druk_Sleutel(0xffc6); 자신.TYPE_kategorie('rk'); 자신.druk_Sleutel(0xff51)
        자신.TYPE_kategorie('sk'); 자신.assertTrue(자신.SMS_buffer.endswith('가\x1b[D나'))

    def test_붙이기유니코드(자신):
        자신.druk_Sleutel(0xffc6); 자신.TYPE_kategorie('rk')
        자신.sleutelbord_inskrywing.knipbord_VALUE='plak_VALUE'.encode()
        자신.sleutelbord_inskrywing.누름값(True,0xffe3); 자신.sleutelbord_inskrywing.누름값(True,0xffe1)
        자신.druk_Sleutel(ord('v'))
        자신.sleutelbord_inskrywing.누름값(False,0xffe1); 자신.sleutelbord_inskrywing.누름값(False,0xffe3)
        자신.druk_Sleutel(0x0100d55c); 자신.TYPE_kategorie('sk')
        자신.assertEqual(자신.SMS_buffer,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
