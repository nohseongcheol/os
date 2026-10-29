#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from biro_kollal import tappirde


class 한글입력시험(unittest.TestCase):
    def setUp(자신):
        자신.binndi_resordu_sabbordu = ''
        def neldude(keɓe):
            for alkulal_keɓe in keɓe.decode('utf-8'):
                if alkulal_keɓe == '\x7f': 자신.binndi_resordu_sabbordu = 자신.binndi_resordu_sabbordu[:-1]
                else: 자신.binndi_resordu_sabbordu += alkulal_keɓe
        자신.tappirde_naatnugol = tappirde(neldude)

    def 글쇠누르기(자신, 심볼):
        자신.tappirde_naatnugol.누름값(True, 심볼)
        자신.tappirde_naatnugol.누름값(False, 심볼)

    def 유형(자신, 누름열):
        for 누름값 in 누름열: 자신.글쇠누르기(ord(누름값))

    def test_낱말(자신):
        for 누름열,예상결과 in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with 자신.subTest(누름열=누름열):
                자신.setUp(); 자신.글쇠누르기(0xffc6); 자신.유형(누름열)
                자신.assertEqual(자신.binndi_resordu_sabbordu, 예상결과)

    def test_앞글자지우기(자신):
        자신.글쇠누르기(0xff31); 자신.유형('dlfr')
        자신.assertEqual(자신.binndi_resordu_sabbordu,'읽')
        for 예상결과 in ('일','이','ㅇ',''):
            자신.글쇠누르기(0xff08); 자신.assertEqual(자신.binndi_resordu_sabbordu,예상결과)
        자신.유형('gksk'); 자신.assertEqual(자신.binndi_resordu_sabbordu,'하나')
        자신.글쇠누르기(0xff08); 자신.assertEqual(자신.binndi_resordu_sabbordu,'하ㄴ')

    def test_전환반복확정(자신):
        자신.유형('echo ')
        자신.tappirde_naatnugol.누름값(True,0xffe1)
        자신.tappirde_naatnugol.누름값(True,32); 자신.tappirde_naatnugol.누름값(True,32)
        자신.tappirde_naatnugol.누름값(False,32); 자신.tappirde_naatnugol.누름값(False,0xffe1)
        자신.assertTrue(자신.tappirde_naatnugol.한글여부)
        자신.유형('gksrmf'); 자신.글쇠누르기(0xff31); 자신.유형(' English')
        자신.assertEqual(자신.binndi_resordu_sabbordu,'echo 한글 English')
        자신.assertFalse(자신.tappirde_naatnugol.한글여부)
        자신.글쇠누르기(0xffc6); 자신.유형('rk'); 자신.글쇠누르기(0xff51)
        자신.유형('sk'); 자신.assertTrue(자신.binndi_resordu_sabbordu.endswith('가\x1b[D나'))

    def test_붙이기유니코드(자신):
        자신.글쇠누르기(0xffc6); 자신.유형('rk')
        자신.tappirde_naatnugol.ɗakkitorde_njaru='ɗakkude_njaru'.encode()
        자신.tappirde_naatnugol.누름값(True,0xffe3); 자신.tappirde_naatnugol.누름값(True,0xffe1)
        자신.글쇠누르기(ord('v'))
        자신.tappirde_naatnugol.누름값(False,0xffe1); 자신.tappirde_naatnugol.누름값(False,0xffe3)
        자신.글쇠누르기(0x0100d55c); 자신.유형('sk')
        자신.assertEqual(자신.binndi_resordu_sabbordu,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
