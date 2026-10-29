#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from pc_Weergave import toetsenbord


class 한글입력시험(unittest.TestCase):
    def setUp(자신):
        자신.sms_buffer = ''
        def e_mailen(gegevens):
            for tekengegevens in gegevens.decode('utf-8'):
                if tekengegevens == '\x7f': 자신.sms_buffer = 자신.sms_buffer[:-1]
                else: 자신.sms_buffer += tekengegevens
        자신.toetsenbord_invoer = toetsenbord(e_mailen)

    def 글쇠누르기(자신, symbool_WAARDE):
        자신.toetsenbord_invoer.누름값(True, symbool_WAARDE)
        자신.toetsenbord_invoer.누름값(False, symbool_WAARDE)

    def TYPE_gebied(자신, 누름열):
        for 누름값 in 누름열: 자신.글쇠누르기(ord(누름값))

    def test_낱말(자신):
        for 누름열,예상결과 in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with 자신.subTest(누름열=누름열):
                자신.setUp(); 자신.글쇠누르기(0xffc6); 자신.TYPE_gebied(누름열)
                자신.assertEqual(자신.sms_buffer, 예상결과)

    def test_앞글자지우기(자신):
        자신.글쇠누르기(0xff31); 자신.TYPE_gebied('dlfr')
        자신.assertEqual(자신.sms_buffer,'읽')
        for 예상결과 in ('일','이','ㅇ',''):
            자신.글쇠누르기(0xff08); 자신.assertEqual(자신.sms_buffer,예상결과)
        자신.TYPE_gebied('gksk'); 자신.assertEqual(자신.sms_buffer,'하나')
        자신.글쇠누르기(0xff08); 자신.assertEqual(자신.sms_buffer,'하ㄴ')

    def test_전환반복확정(자신):
        자신.TYPE_gebied('echo ')
        자신.toetsenbord_invoer.누름값(True,0xffe1)
        자신.toetsenbord_invoer.누름값(True,32); 자신.toetsenbord_invoer.누름값(True,32)
        자신.toetsenbord_invoer.누름값(False,32); 자신.toetsenbord_invoer.누름값(False,0xffe1)
        자신.assertTrue(자신.toetsenbord_invoer.한글여부)
        자신.TYPE_gebied('gksrmf'); 자신.글쇠누르기(0xff31); 자신.TYPE_gebied(' English')
        자신.assertEqual(자신.sms_buffer,'echo 한글 English')
        자신.assertFalse(자신.toetsenbord_invoer.한글여부)
        자신.글쇠누르기(0xffc6); 자신.TYPE_gebied('rk'); 자신.글쇠누르기(0xff51)
        자신.TYPE_gebied('sk'); 자신.assertTrue(자신.sms_buffer.endswith('가\x1b[D나'))

    def test_plakken_EN_UNICODE(자신):
        자신.글쇠누르기(0xffc6); 자신.TYPE_gebied('rk')
        자신.toetsenbord_invoer.klembord_WAARDE='plakken_WAARDE'.encode()
        자신.toetsenbord_invoer.누름값(True,0xffe3); 자신.toetsenbord_invoer.누름값(True,0xffe1)
        자신.글쇠누르기(ord('v'))
        자신.toetsenbord_invoer.누름값(False,0xffe1); 자신.toetsenbord_invoer.누름값(False,0xffe3)
        자신.글쇠누르기(0x0100d55c); 자신.TYPE_gebied('sk')
        자신.assertEqual(자신.sms_buffer,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
