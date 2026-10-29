#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from skjáborð_Sýn import lyklaborð


class 한글입력시험(unittest.TestCase):
    def setUp(자신):
        자신.SMS_biðminni = ''
        def senda(gögn):
            for stafur_gögn in gögn.decode('utf-8'):
                if stafur_gögn == '\x7f': 자신.SMS_biðminni = 자신.SMS_biðminni[:-1]
                else: 자신.SMS_biðminni += stafur_gögn
        자신.lyklaborð_færsla = lyklaborð(senda)

    def ýta_Lykill(자신, tákn_VALUE):
        자신.lyklaborð_færsla.누름값(True, tákn_VALUE)
        자신.lyklaborð_færsla.누름값(False, tákn_VALUE)

    def TYPE_tegund(자신, 누름열):
        for 누름값 in 누름열: 자신.ýta_Lykill(ord(누름값))

    def test_낱말(자신):
        for 누름열,예상결과 in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with 자신.subTest(누름열=누름열):
                자신.setUp(); 자신.ýta_Lykill(0xffc6); 자신.TYPE_tegund(누름열)
                자신.assertEqual(자신.SMS_biðminni, 예상결과)

    def test_앞글자지우기(자신):
        자신.ýta_Lykill(0xff31); 자신.TYPE_tegund('dlfr')
        자신.assertEqual(자신.SMS_biðminni,'읽')
        for 예상결과 in ('일','이','ㅇ',''):
            자신.ýta_Lykill(0xff08); 자신.assertEqual(자신.SMS_biðminni,예상결과)
        자신.TYPE_tegund('gksk'); 자신.assertEqual(자신.SMS_biðminni,'하나')
        자신.ýta_Lykill(0xff08); 자신.assertEqual(자신.SMS_biðminni,'하ㄴ')

    def test_전환반복확정(자신):
        자신.TYPE_tegund('echo ')
        자신.lyklaborð_færsla.누름값(True,0xffe1)
        자신.lyklaborð_færsla.누름값(True,32); 자신.lyklaborð_færsla.누름값(True,32)
        자신.lyklaborð_færsla.누름값(False,32); 자신.lyklaborð_færsla.누름값(False,0xffe1)
        자신.assertTrue(자신.lyklaborð_færsla.한글여부)
        자신.TYPE_tegund('gksrmf'); 자신.ýta_Lykill(0xff31); 자신.TYPE_tegund(' English')
        자신.assertEqual(자신.SMS_biðminni,'echo 한글 English')
        자신.assertFalse(자신.lyklaborð_færsla.한글여부)
        자신.ýta_Lykill(0xffc6); 자신.TYPE_tegund('rk'); 자신.ýta_Lykill(0xff51)
        자신.TYPE_tegund('sk'); 자신.assertTrue(자신.SMS_biðminni.endswith('가\x1b[D나'))

    def test_붙이기유니코드(자신):
        자신.ýta_Lykill(0xffc6); 자신.TYPE_tegund('rk')
        자신.lyklaborð_færsla.klippiborð_VALUE='líma_VALUE'.encode()
        자신.lyklaborð_færsla.누름값(True,0xffe3); 자신.lyklaborð_færsla.누름값(True,0xffe1)
        자신.ýta_Lykill(ord('v'))
        자신.lyklaborð_færsla.누름값(False,0xffe1); 자신.lyklaborð_færsla.누름값(False,0xffe3)
        자신.ýta_Lykill(0x0100d55c); 자신.TYPE_tegund('sk')
        자신.assertEqual(자신.SMS_biðminni,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
