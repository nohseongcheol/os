#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from darbalaukis_rodyti import klaviatūra


class 한글입력시험(unittest.TestCase):
    def setUp(자신):
        자신.SMS_kaupti = ''
        def siųsti(duomenys):
            for simbolių_duomenys in duomenys.decode('utf-8'):
                if simbolių_duomenys == '\x7f': 자신.SMS_kaupti = 자신.SMS_kaupti[:-1]
                else: 자신.SMS_kaupti += simbolių_duomenys
        자신.klaviatūra_įrašas = klaviatūra(siųsti)

    def paspausti_Raktas(자신, simbolis_VALUE):
        자신.klaviatūra_įrašas.누름값(True, simbolis_VALUE)
        자신.klaviatūra_įrašas.누름값(False, simbolis_VALUE)

    def TYPE_sritis(자신, 누름열):
        for 누름값 in 누름열: 자신.paspausti_Raktas(ord(누름값))

    def test_낱말(자신):
        for 누름열,예상결과 in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with 자신.subTest(누름열=누름열):
                자신.setUp(); 자신.paspausti_Raktas(0xffc6); 자신.TYPE_sritis(누름열)
                자신.assertEqual(자신.SMS_kaupti, 예상결과)

    def test_앞글자지우기(자신):
        자신.paspausti_Raktas(0xff31); 자신.TYPE_sritis('dlfr')
        자신.assertEqual(자신.SMS_kaupti,'읽')
        for 예상결과 in ('일','이','ㅇ',''):
            자신.paspausti_Raktas(0xff08); 자신.assertEqual(자신.SMS_kaupti,예상결과)
        자신.TYPE_sritis('gksk'); 자신.assertEqual(자신.SMS_kaupti,'하나')
        자신.paspausti_Raktas(0xff08); 자신.assertEqual(자신.SMS_kaupti,'하ㄴ')

    def test_전환반복확정(자신):
        자신.TYPE_sritis('echo ')
        자신.klaviatūra_įrašas.누름값(True,0xffe1)
        자신.klaviatūra_įrašas.누름값(True,32); 자신.klaviatūra_įrašas.누름값(True,32)
        자신.klaviatūra_įrašas.누름값(False,32); 자신.klaviatūra_įrašas.누름값(False,0xffe1)
        자신.assertTrue(자신.klaviatūra_įrašas.한글여부)
        자신.TYPE_sritis('gksrmf'); 자신.paspausti_Raktas(0xff31); 자신.TYPE_sritis(' English')
        자신.assertEqual(자신.SMS_kaupti,'echo 한글 English')
        자신.assertFalse(자신.klaviatūra_įrašas.한글여부)
        자신.paspausti_Raktas(0xffc6); 자신.TYPE_sritis('rk'); 자신.paspausti_Raktas(0xff51)
        자신.TYPE_sritis('sk'); 자신.assertTrue(자신.SMS_kaupti.endswith('가\x1b[D나'))

    def test_붙이기유니코드(자신):
        자신.paspausti_Raktas(0xffc6); 자신.TYPE_sritis('rk')
        자신.klaviatūra_įrašas.mainų_sritis_VALUE='Įklijuoti_VALUE'.encode()
        자신.klaviatūra_įrašas.누름값(True,0xffe3); 자신.klaviatūra_įrašas.누름값(True,0xffe1)
        자신.paspausti_Raktas(ord('v'))
        자신.klaviatūra_įrašas.누름값(False,0xffe1); 자신.klaviatūra_įrašas.누름값(False,0xffe3)
        자신.paspausti_Raktas(0x0100d55c); 자신.TYPE_sritis('sk')
        자신.assertEqual(자신.SMS_kaupti,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
