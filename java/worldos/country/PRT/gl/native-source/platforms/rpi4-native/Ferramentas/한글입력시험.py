#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from escritorio_ver import teclado


class 한글입력시험(unittest.TestCase):
    def setUp(자신):
        자신.SMS_búfer = ''
        def enviar(datos):
            for carácter_datos in datos.decode('utf-8'):
                if carácter_datos == '\x7f': 자신.SMS_búfer = 자신.SMS_búfer[:-1]
                else: 자신.SMS_búfer += carácter_datos
        자신.teclado_introdución = teclado(enviar)

    def pulsar_Chave(자신, símbolo_VALOR):
        자신.teclado_introdución.누름값(True, símbolo_VALOR)
        자신.teclado_introdución.누름값(False, símbolo_VALOR)

    def TIPO_Categoría(자신, 누름열):
        for 누름값 in 누름열: 자신.pulsar_Chave(ord(누름값))

    def test_낱말(자신):
        for 누름열,예상결과 in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with 자신.subTest(누름열=누름열):
                자신.setUp(); 자신.pulsar_Chave(0xffc6); 자신.TIPO_Categoría(누름열)
                자신.assertEqual(자신.SMS_búfer, 예상결과)

    def test_앞글자지우기(자신):
        자신.pulsar_Chave(0xff31); 자신.TIPO_Categoría('dlfr')
        자신.assertEqual(자신.SMS_búfer,'읽')
        for 예상결과 in ('일','이','ㅇ',''):
            자신.pulsar_Chave(0xff08); 자신.assertEqual(자신.SMS_búfer,예상결과)
        자신.TIPO_Categoría('gksk'); 자신.assertEqual(자신.SMS_búfer,'하나')
        자신.pulsar_Chave(0xff08); 자신.assertEqual(자신.SMS_búfer,'하ㄴ')

    def test_전환반복확정(자신):
        자신.TIPO_Categoría('echo ')
        자신.teclado_introdución.누름값(True,0xffe1)
        자신.teclado_introdución.누름값(True,32); 자신.teclado_introdución.누름값(True,32)
        자신.teclado_introdución.누름값(False,32); 자신.teclado_introdución.누름값(False,0xffe1)
        자신.assertTrue(자신.teclado_introdución.한글여부)
        자신.TIPO_Categoría('gksrmf'); 자신.pulsar_Chave(0xff31); 자신.TIPO_Categoría(' English')
        자신.assertEqual(자신.SMS_búfer,'echo 한글 English')
        자신.assertFalse(자신.teclado_introdución.한글여부)
        자신.pulsar_Chave(0xffc6); 자신.TIPO_Categoría('rk'); 자신.pulsar_Chave(0xff51)
        자신.TIPO_Categoría('sk'); 자신.assertTrue(자신.SMS_búfer.endswith('가\x1b[D나'))

    def test_붙이기유니코드(자신):
        자신.pulsar_Chave(0xffc6); 자신.TIPO_Categoría('rk')
        자신.teclado_introdución.portapapeis_VALOR='pegar_VALOR'.encode()
        자신.teclado_introdución.누름값(True,0xffe3); 자신.teclado_introdución.누름값(True,0xffe1)
        자신.pulsar_Chave(ord('v'))
        자신.teclado_introdución.누름값(False,0xffe1); 자신.teclado_introdución.누름값(False,0xffe3)
        자신.pulsar_Chave(0x0100d55c); 자신.TIPO_Categoría('sk')
        자신.assertEqual(자신.SMS_búfer,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
