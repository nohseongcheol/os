#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from escriptori_visualitzar import teclat


class 한글입력시험(unittest.TestCase):
    def setUp(자신):
        자신.SMS_memòria_intermèdia = ''
        def enviar(dades):
            for caràcter_dades in dades.decode('utf-8'):
                if caràcter_dades == '\x7f': 자신.SMS_memòria_intermèdia = 자신.SMS_memòria_intermèdia[:-1]
                else: 자신.SMS_memòria_intermèdia += caràcter_dades
        자신.teclat_introducció = teclat(enviar)

    def prémer_Clau(자신, símbol_VALOR):
        자신.teclat_introducció.누름값(True, símbol_VALOR)
        자신.teclat_introducció.누름값(False, símbol_VALOR)

    def TIPUS_Categoria(자신, 누름열):
        for 누름값 in 누름열: 자신.prémer_Clau(ord(누름값))

    def test_낱말(자신):
        for 누름열,예상결과 in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with 자신.subTest(누름열=누름열):
                자신.setUp(); 자신.prémer_Clau(0xffc6); 자신.TIPUS_Categoria(누름열)
                자신.assertEqual(자신.SMS_memòria_intermèdia, 예상결과)

    def test_앞글자지우기(자신):
        자신.prémer_Clau(0xff31); 자신.TIPUS_Categoria('dlfr')
        자신.assertEqual(자신.SMS_memòria_intermèdia,'읽')
        for 예상결과 in ('일','이','ㅇ',''):
            자신.prémer_Clau(0xff08); 자신.assertEqual(자신.SMS_memòria_intermèdia,예상결과)
        자신.TIPUS_Categoria('gksk'); 자신.assertEqual(자신.SMS_memòria_intermèdia,'하나')
        자신.prémer_Clau(0xff08); 자신.assertEqual(자신.SMS_memòria_intermèdia,'하ㄴ')

    def test_전환반복확정(자신):
        자신.TIPUS_Categoria('echo ')
        자신.teclat_introducció.누름값(True,0xffe1)
        자신.teclat_introducció.누름값(True,32); 자신.teclat_introducció.누름값(True,32)
        자신.teclat_introducció.누름값(False,32); 자신.teclat_introducció.누름값(False,0xffe1)
        자신.assertTrue(자신.teclat_introducció.한글여부)
        자신.TIPUS_Categoria('gksrmf'); 자신.prémer_Clau(0xff31); 자신.TIPUS_Categoria(' English')
        자신.assertEqual(자신.SMS_memòria_intermèdia,'echo 한글 English')
        자신.assertFalse(자신.teclat_introducció.한글여부)
        자신.prémer_Clau(0xffc6); 자신.TIPUS_Categoria('rk'); 자신.prémer_Clau(0xff51)
        자신.TIPUS_Categoria('sk'); 자신.assertTrue(자신.SMS_memòria_intermèdia.endswith('가\x1b[D나'))

    def test_붙이기유니코드(자신):
        자신.prémer_Clau(0xffc6); 자신.TIPUS_Categoria('rk')
        자신.teclat_introducció.Porta_retalls_VALOR='enganxar_VALOR'.encode()
        자신.teclat_introducció.누름값(True,0xffe3); 자신.teclat_introducció.누름값(True,0xffe1)
        자신.prémer_Clau(ord('v'))
        자신.teclat_introducció.누름값(False,0xffe1); 자신.teclat_introducció.누름값(False,0xffe3)
        자신.prémer_Clau(0x0100d55c); 자신.TIPUS_Categoria('sk')
        자신.assertEqual(자신.SMS_memòria_intermèdia,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
