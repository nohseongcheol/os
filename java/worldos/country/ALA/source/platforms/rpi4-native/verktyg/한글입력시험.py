#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from Dator_vy import tangentbord


class 한글입력시험(unittest.TestCase):
    def setUp(자신):
        자신.SMS_buffra = ''
        def skicka(data):
            for teckendata in data.decode('utf-8'):
                if teckendata == '\x7f': 자신.SMS_buffra = 자신.SMS_buffra[:-1]
                else: 자신.SMS_buffra += teckendata
        자신.tangentbord_post = tangentbord(skicka)

    def tryck_Nyckel(자신, symbol_värde):
        자신.tangentbord_post.누름값(True, symbol_värde)
        자신.tangentbord_post.누름값(False, symbol_värde)

    def Typ_område(자신, 누름열):
        for 누름값 in 누름열: 자신.tryck_Nyckel(ord(누름값))

    def test_낱말(자신):
        for 누름열,예상결과 in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with 자신.subTest(누름열=누름열):
                자신.setUp(); 자신.tryck_Nyckel(0xffc6); 자신.Typ_område(누름열)
                자신.assertEqual(자신.SMS_buffra, 예상결과)

    def test_앞글자지우기(자신):
        자신.tryck_Nyckel(0xff31); 자신.Typ_område('dlfr')
        자신.assertEqual(자신.SMS_buffra,'읽')
        for 예상결과 in ('일','이','ㅇ',''):
            자신.tryck_Nyckel(0xff08); 자신.assertEqual(자신.SMS_buffra,예상결과)
        자신.Typ_område('gksk'); 자신.assertEqual(자신.SMS_buffra,'하나')
        자신.tryck_Nyckel(0xff08); 자신.assertEqual(자신.SMS_buffra,'하ㄴ')

    def test_전환반복확정(자신):
        자신.Typ_område('echo ')
        자신.tangentbord_post.누름값(True,0xffe1)
        자신.tangentbord_post.누름값(True,32); 자신.tangentbord_post.누름값(True,32)
        자신.tangentbord_post.누름값(False,32); 자신.tangentbord_post.누름값(False,0xffe1)
        자신.assertTrue(자신.tangentbord_post.한글여부)
        자신.Typ_område('gksrmf'); 자신.tryck_Nyckel(0xff31); 자신.Typ_område(' English')
        자신.assertEqual(자신.SMS_buffra,'echo 한글 English')
        자신.assertFalse(자신.tangentbord_post.한글여부)
        자신.tryck_Nyckel(0xffc6); 자신.Typ_område('rk'); 자신.tryck_Nyckel(0xff51)
        자신.Typ_område('sk'); 자신.assertTrue(자신.SMS_buffra.endswith('가\x1b[D나'))

    def test_klistra_in_AND_UNICODE(자신):
        자신.tryck_Nyckel(0xffc6); 자신.Typ_område('rk')
        자신.tangentbord_post.Urklipp_värde='klistra_in_värde'.encode()
        자신.tangentbord_post.누름값(True,0xffe3); 자신.tangentbord_post.누름값(True,0xffe1)
        자신.tryck_Nyckel(ord('v'))
        자신.tangentbord_post.누름값(False,0xffe1); 자신.tangentbord_post.누름값(False,0xffe3)
        자신.tryck_Nyckel(0x0100d55c); 자신.Typ_område('sk')
        자신.assertEqual(자신.SMS_buffra,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
