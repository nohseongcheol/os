#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from desktop_Exibir import teclado


class 한글입력시험(unittest.TestCase):
    def setUp(자신):
        자신.SMS_buffer = ''
        def enviar(dados):
            for dados_de_caractere in dados.decode('utf-8'):
                if dados_de_caractere == '\x7f': 자신.SMS_buffer = 자신.SMS_buffer[:-1]
                else: 자신.SMS_buffer += dados_de_caractere
        자신.teclado_entrada = teclado(enviar)

    def 글쇠누르기(자신, símbolo_VALOR):
        자신.teclado_entrada.누름값(True, símbolo_VALOR)
        자신.teclado_entrada.누름값(False, símbolo_VALOR)

    def TIPO_área(자신, 누름열):
        for 누름값 in 누름열: 자신.글쇠누르기(ord(누름값))

    def test_낱말(자신):
        for 누름열,예상결과 in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with 자신.subTest(누름열=누름열):
                자신.setUp(); 자신.글쇠누르기(0xffc6); 자신.TIPO_área(누름열)
                자신.assertEqual(자신.SMS_buffer, 예상결과)

    def test_앞글자지우기(자신):
        자신.글쇠누르기(0xff31); 자신.TIPO_área('dlfr')
        자신.assertEqual(자신.SMS_buffer,'읽')
        for 예상결과 in ('일','이','ㅇ',''):
            자신.글쇠누르기(0xff08); 자신.assertEqual(자신.SMS_buffer,예상결과)
        자신.TIPO_área('gksk'); 자신.assertEqual(자신.SMS_buffer,'하나')
        자신.글쇠누르기(0xff08); 자신.assertEqual(자신.SMS_buffer,'하ㄴ')

    def test_전환반복확정(자신):
        자신.TIPO_área('echo ')
        자신.teclado_entrada.누름값(True,0xffe1)
        자신.teclado_entrada.누름값(True,32); 자신.teclado_entrada.누름값(True,32)
        자신.teclado_entrada.누름값(False,32); 자신.teclado_entrada.누름값(False,0xffe1)
        자신.assertTrue(자신.teclado_entrada.한글여부)
        자신.TIPO_área('gksrmf'); 자신.글쇠누르기(0xff31); 자신.TIPO_área(' English')
        자신.assertEqual(자신.SMS_buffer,'echo 한글 English')
        자신.assertFalse(자신.teclado_entrada.한글여부)
        자신.글쇠누르기(0xffc6); 자신.TIPO_área('rk'); 자신.글쇠누르기(0xff51)
        자신.TIPO_área('sk'); 자신.assertTrue(자신.SMS_buffer.endswith('가\x1b[D나'))

    def teste_colar_E_UNICODE(자신):
        자신.글쇠누르기(0xffc6); 자신.TIPO_área('rk')
        자신.teclado_entrada.área_de_transferência_VALOR='colar_VALOR'.encode()
        자신.teclado_entrada.누름값(True,0xffe3); 자신.teclado_entrada.누름값(True,0xffe1)
        자신.글쇠누르기(ord('v'))
        자신.teclado_entrada.누름값(False,0xffe1); 자신.teclado_entrada.누름값(False,0xffe3)
        자신.글쇠누르기(0x0100d55c); 자신.TIPO_área('sk')
        자신.assertEqual(자신.SMS_buffer,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
