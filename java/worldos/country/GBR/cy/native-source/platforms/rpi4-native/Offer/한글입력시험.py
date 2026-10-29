#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from bwrdd_gwaith_Gwedd import allweddell


class 한글입력시험(unittest.TestCase):
    def setUp(자신):
        자신.SMS_byffer = ''
        def anfon(data):
            for nod_data in data.decode('utf-8'):
                if nod_data == '\x7f': 자신.SMS_byffer = 자신.SMS_byffer[:-1]
                else: 자신.SMS_byffer += nod_data
        자신.allweddell_cofnod = allweddell(anfon)

    def pwyso_bysell(자신, symbol_VALUE):
        자신.allweddell_cofnod.누름값(True, symbol_VALUE)
        자신.allweddell_cofnod.누름값(False, symbol_VALUE)

    def TYPE_ardal(자신, 누름열):
        for 누름값 in 누름열: 자신.pwyso_bysell(ord(누름값))

    def test_낱말(자신):
        for 누름열,예상결과 in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with 자신.subTest(누름열=누름열):
                자신.setUp(); 자신.pwyso_bysell(0xffc6); 자신.TYPE_ardal(누름열)
                자신.assertEqual(자신.SMS_byffer, 예상결과)

    def test_앞글자지우기(자신):
        자신.pwyso_bysell(0xff31); 자신.TYPE_ardal('dlfr')
        자신.assertEqual(자신.SMS_byffer,'읽')
        for 예상결과 in ('일','이','ㅇ',''):
            자신.pwyso_bysell(0xff08); 자신.assertEqual(자신.SMS_byffer,예상결과)
        자신.TYPE_ardal('gksk'); 자신.assertEqual(자신.SMS_byffer,'하나')
        자신.pwyso_bysell(0xff08); 자신.assertEqual(자신.SMS_byffer,'하ㄴ')

    def test_전환반복확정(자신):
        자신.TYPE_ardal('echo ')
        자신.allweddell_cofnod.누름값(True,0xffe1)
        자신.allweddell_cofnod.누름값(True,32); 자신.allweddell_cofnod.누름값(True,32)
        자신.allweddell_cofnod.누름값(False,32); 자신.allweddell_cofnod.누름값(False,0xffe1)
        자신.assertTrue(자신.allweddell_cofnod.한글여부)
        자신.TYPE_ardal('gksrmf'); 자신.pwyso_bysell(0xff31); 자신.TYPE_ardal(' English')
        자신.assertEqual(자신.SMS_byffer,'echo 한글 English')
        자신.assertFalse(자신.allweddell_cofnod.한글여부)
        자신.pwyso_bysell(0xffc6); 자신.TYPE_ardal('rk'); 자신.pwyso_bysell(0xff51)
        자신.TYPE_ardal('sk'); 자신.assertTrue(자신.SMS_byffer.endswith('가\x1b[D나'))

    def test_붙이기유니코드(자신):
        자신.pwyso_bysell(0xffc6); 자신.TYPE_ardal('rk')
        자신.allweddell_cofnod.clipfwrdd_VALUE='gludo_VALUE'.encode()
        자신.allweddell_cofnod.누름값(True,0xffe3); 자신.allweddell_cofnod.누름값(True,0xffe1)
        자신.pwyso_bysell(ord('v'))
        자신.allweddell_cofnod.누름값(False,0xffe1); 자신.allweddell_cofnod.누름값(False,0xffe3)
        자신.pwyso_bysell(0x0100d55c); 자신.TYPE_ardal('sk')
        자신.assertEqual(자신.SMS_byffer,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
