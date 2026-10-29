#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from destof_s import kibod


class 한글입력시험(unittest.TestCase):
    def setUp(자신):
        자신.SMS_Tunani_na_wucin_gadi = ''
        def Aika(Tarin_bayani):
            for Harafi_Tarin_bayani in Tarin_bayani.decode('utf-8'):
                if Harafi_Tarin_bayani == '\x7f': 자신.SMS_Tunani_na_wucin_gadi = 자신.SMS_Tunani_na_wucin_gadi[:-1]
                else: 자신.SMS_Tunani_na_wucin_gadi += Harafi_Tarin_bayani
        자신.kibod_Mashigar_bayanai = kibod(Aika)

    def 글쇠누르기(자신, alama_Daraja):
        자신.kibod_Mashigar_bayanai.누름값(True, alama_Daraja)
        자신.kibod_Mashigar_bayanai.누름값(False, alama_Daraja)

    def rubuta_ɓangare(자신, 누름열):
        for 누름값 in 누름열: 자신.글쇠누르기(ord(누름값))

    def test_낱말(자신):
        for 누름열,예상결과 in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with 자신.subTest(누름열=누름열):
                자신.setUp(); 자신.글쇠누르기(0xffc6); 자신.rubuta_ɓangare(누름열)
                자신.assertEqual(자신.SMS_Tunani_na_wucin_gadi, 예상결과)

    def test_앞글자지우기(자신):
        자신.글쇠누르기(0xff31); 자신.rubuta_ɓangare('dlfr')
        자신.assertEqual(자신.SMS_Tunani_na_wucin_gadi,'읽')
        for 예상결과 in ('일','이','ㅇ',''):
            자신.글쇠누르기(0xff08); 자신.assertEqual(자신.SMS_Tunani_na_wucin_gadi,예상결과)
        자신.rubuta_ɓangare('gksk'); 자신.assertEqual(자신.SMS_Tunani_na_wucin_gadi,'하나')
        자신.글쇠누르기(0xff08); 자신.assertEqual(자신.SMS_Tunani_na_wucin_gadi,'하ㄴ')

    def test_전환반복확정(자신):
        자신.rubuta_ɓangare('echo ')
        자신.kibod_Mashigar_bayanai.누름값(True,0xffe1)
        자신.kibod_Mashigar_bayanai.누름값(True,32); 자신.kibod_Mashigar_bayanai.누름값(True,32)
        자신.kibod_Mashigar_bayanai.누름값(False,32); 자신.kibod_Mashigar_bayanai.누름값(False,0xffe1)
        자신.assertTrue(자신.kibod_Mashigar_bayanai.한글여부)
        자신.rubuta_ɓangare('gksrmf'); 자신.글쇠누르기(0xff31); 자신.rubuta_ɓangare(' English')
        자신.assertEqual(자신.SMS_Tunani_na_wucin_gadi,'echo 한글 English')
        자신.assertFalse(자신.kibod_Mashigar_bayanai.한글여부)
        자신.글쇠누르기(0xffc6); 자신.rubuta_ɓangare('rk'); 자신.글쇠누르기(0xff51)
        자신.rubuta_ɓangare('sk'); 자신.assertTrue(자신.SMS_Tunani_na_wucin_gadi.endswith('가\x1b[D나'))

    def test_붙이기유니코드(자신):
        자신.글쇠누르기(0xffc6); 자신.rubuta_ɓangare('rk')
        자신.kibod_Mashigar_bayanai.Allon_zane_Daraja='manna_Daraja'.encode()
        자신.kibod_Mashigar_bayanai.누름값(True,0xffe3); 자신.kibod_Mashigar_bayanai.누름값(True,0xffe1)
        자신.글쇠누르기(ord('v'))
        자신.kibod_Mashigar_bayanai.누름값(False,0xffe1); 자신.kibod_Mashigar_bayanai.누름값(False,0xffe3)
        자신.글쇠누르기(0x0100d55c); 자신.rubuta_ɓangare('sk')
        자신.assertEqual(자신.SMS_Tunani_na_wucin_gadi,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
