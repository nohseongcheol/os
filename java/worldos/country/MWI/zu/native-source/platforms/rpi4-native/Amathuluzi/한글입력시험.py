#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from ideskithophu_buka import ikhibhodi


class 한글입력시험(unittest.TestCase):
    def setUp(자신):
        자신.I_SMS_isikhumbulo_sesikhana = ''
        def Thumela(imininingwane):
            for uhlamvusimo_imininingwane in imininingwane.decode('utf-8'):
                if uhlamvusimo_imininingwane == '\x7f': 자신.I_SMS_isikhumbulo_sesikhana = 자신.I_SMS_isikhumbulo_sesikhana[:-1]
                else: 자신.I_SMS_isikhumbulo_sesikhana += uhlamvusimo_imininingwane
        자신.ikhibhodi_okufakwayo = ikhibhodi(Thumela)

    def 글쇠누르기(자신, uphawu_inani):
        자신.ikhibhodi_okufakwayo.누름값(True, uphawu_inani)
        자신.ikhibhodi_okufakwayo.누름값(False, uphawu_inani)

    def thayipha_umunxa(자신, 누름열):
        for 누름값 in 누름열: 자신.글쇠누르기(ord(누름값))

    def test_낱말(자신):
        for 누름열,예상결과 in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with 자신.subTest(누름열=누름열):
                자신.setUp(); 자신.글쇠누르기(0xffc6); 자신.thayipha_umunxa(누름열)
                자신.assertEqual(자신.I_SMS_isikhumbulo_sesikhana, 예상결과)

    def test_앞글자지우기(자신):
        자신.글쇠누르기(0xff31); 자신.thayipha_umunxa('dlfr')
        자신.assertEqual(자신.I_SMS_isikhumbulo_sesikhana,'읽')
        for 예상결과 in ('일','이','ㅇ',''):
            자신.글쇠누르기(0xff08); 자신.assertEqual(자신.I_SMS_isikhumbulo_sesikhana,예상결과)
        자신.thayipha_umunxa('gksk'); 자신.assertEqual(자신.I_SMS_isikhumbulo_sesikhana,'하나')
        자신.글쇠누르기(0xff08); 자신.assertEqual(자신.I_SMS_isikhumbulo_sesikhana,'하ㄴ')

    def test_전환반복확정(자신):
        자신.thayipha_umunxa('echo ')
        자신.ikhibhodi_okufakwayo.누름값(True,0xffe1)
        자신.ikhibhodi_okufakwayo.누름값(True,32); 자신.ikhibhodi_okufakwayo.누름값(True,32)
        자신.ikhibhodi_okufakwayo.누름값(False,32); 자신.ikhibhodi_okufakwayo.누름값(False,0xffe1)
        자신.assertTrue(자신.ikhibhodi_okufakwayo.한글여부)
        자신.thayipha_umunxa('gksrmf'); 자신.글쇠누르기(0xff31); 자신.thayipha_umunxa(' English')
        자신.assertEqual(자신.I_SMS_isikhumbulo_sesikhana,'echo 한글 English')
        자신.assertFalse(자신.ikhibhodi_okufakwayo.한글여부)
        자신.글쇠누르기(0xffc6); 자신.thayipha_umunxa('rk'); 자신.글쇠누르기(0xff51)
        자신.thayipha_umunxa('sk'); 자신.assertTrue(자신.I_SMS_isikhumbulo_sesikhana.endswith('가\x1b[D나'))

    def test_붙이기유니코드(자신):
        자신.글쇠누르기(0xffc6); 자신.thayipha_umunxa('rk')
        자신.ikhibhodi_okufakwayo.ibhodi_yokunamathisela_inani='namathisela_inani'.encode()
        자신.ikhibhodi_okufakwayo.누름값(True,0xffe3); 자신.ikhibhodi_okufakwayo.누름값(True,0xffe1)
        자신.글쇠누르기(ord('v'))
        자신.ikhibhodi_okufakwayo.누름값(False,0xffe1); 자신.ikhibhodi_okufakwayo.누름값(False,0xffe3)
        자신.글쇠누르기(0x0100d55c); 자신.thayipha_umunxa('sk')
        자신.assertEqual(자신.I_SMS_isikhumbulo_sesikhana,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
