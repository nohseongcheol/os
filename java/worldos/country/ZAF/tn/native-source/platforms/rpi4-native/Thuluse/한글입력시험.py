#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from desekethopo_Tebego import Khiiboto


class 한글입력시험(unittest.TestCase):
    def setUp(자신):
        자신.SMS_kemelwa = ''
        def romela(tshedimosetso):
            for Letshwao_tshedimosetso in tshedimosetso.decode('utf-8'):
                if Letshwao_tshedimosetso == '\x7f': 자신.SMS_kemelwa = 자신.SMS_kemelwa[:-1]
                else: 자신.SMS_kemelwa += Letshwao_tshedimosetso
        자신.Khiiboto_tsenyo = Khiiboto(romela)

    def 글쇠누르기(자신, letshwao_Boleng):
        자신.Khiiboto_tsenyo.누름값(True, letshwao_Boleng)
        자신.Khiiboto_tsenyo.누름값(False, letshwao_Boleng)

    def tlanya_setlhopha(자신, 누름열):
        for 누름값 in 누름열: 자신.글쇠누르기(ord(누름값))

    def test_낱말(자신):
        for 누름열,예상결과 in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with 자신.subTest(누름열=누름열):
                자신.setUp(); 자신.글쇠누르기(0xffc6); 자신.tlanya_setlhopha(누름열)
                자신.assertEqual(자신.SMS_kemelwa, 예상결과)

    def test_앞글자지우기(자신):
        자신.글쇠누르기(0xff31); 자신.tlanya_setlhopha('dlfr')
        자신.assertEqual(자신.SMS_kemelwa,'읽')
        for 예상결과 in ('일','이','ㅇ',''):
            자신.글쇠누르기(0xff08); 자신.assertEqual(자신.SMS_kemelwa,예상결과)
        자신.tlanya_setlhopha('gksk'); 자신.assertEqual(자신.SMS_kemelwa,'하나')
        자신.글쇠누르기(0xff08); 자신.assertEqual(자신.SMS_kemelwa,'하ㄴ')

    def test_전환반복확정(자신):
        자신.tlanya_setlhopha('echo ')
        자신.Khiiboto_tsenyo.누름값(True,0xffe1)
        자신.Khiiboto_tsenyo.누름값(True,32); 자신.Khiiboto_tsenyo.누름값(True,32)
        자신.Khiiboto_tsenyo.누름값(False,32); 자신.Khiiboto_tsenyo.누름값(False,0xffe1)
        자신.assertTrue(자신.Khiiboto_tsenyo.한글여부)
        자신.tlanya_setlhopha('gksrmf'); 자신.글쇠누르기(0xff31); 자신.tlanya_setlhopha(' English')
        자신.assertEqual(자신.SMS_kemelwa,'echo 한글 English')
        자신.assertFalse(자신.Khiiboto_tsenyo.한글여부)
        자신.글쇠누르기(0xffc6); 자신.tlanya_setlhopha('rk'); 자신.글쇠누르기(0xff51)
        자신.tlanya_setlhopha('sk'); 자신.assertTrue(자신.SMS_kemelwa.endswith('가\x1b[D나'))

    def test_붙이기유니코드(자신):
        자신.글쇠누르기(0xffc6); 자신.tlanya_setlhopha('rk')
        자신.Khiiboto_tsenyo.peelodimamaretswa_Boleng='kgomaretsa_Boleng'.encode()
        자신.Khiiboto_tsenyo.누름값(True,0xffe3); 자신.Khiiboto_tsenyo.누름값(True,0xffe1)
        자신.글쇠누르기(ord('v'))
        자신.Khiiboto_tsenyo.누름값(False,0xffe1); 자신.Khiiboto_tsenyo.누름값(False,0xffe3)
        자신.글쇠누르기(0x0100d55c); 자신.tlanya_setlhopha('sk')
        자신.assertEqual(자신.SMS_kemelwa,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
