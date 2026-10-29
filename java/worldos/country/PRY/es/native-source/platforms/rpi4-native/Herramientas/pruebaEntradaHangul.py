#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from vistaEscritorio import Teclado


class pruebaEntradaHangul(unittest.TestCase):
    def setUp(valorPropio):
        valorPropio.búferTexto = ''
        def enviar(Datos):
            for datosCarácter in Datos.decode('utf-8'):
                if datosCarácter == '\x7f': valorPropio.búferTexto = valorPropio.búferTexto[:-1]
                else: valorPropio.búferTexto += datosCarácter
        valorPropio.entradaElementoTeclado = Teclado(enviar)

    def teclaPulsar(valorPropio, valorSímbolo):
        valorPropio.entradaElementoTeclado.valorPulsado(True, valorSímbolo)
        valorPropio.entradaElementoTeclado.valorPulsado(False, valorSímbolo)

    def categoríaTipo(valorPropio, teclasPulsado):
        for valorPulsado in teclasPulsado: valorPropio.teclaPulsar(ord(valorPulsado))

    def pruebaPalabras(valorPropio):
        for teclasPulsado,esperado in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with valorPropio.subTest(teclasPulsado=teclasPulsado):
                valorPropio.setUp(); valorPropio.teclaPulsar(0xffc6); valorPropio.categoríaTipo(teclasPulsado)
                valorPropio.assertEqual(valorPropio.búferTexto, esperado)

    def pruebaRetroceso(valorPropio):
        valorPropio.teclaPulsar(0xff31); valorPropio.categoríaTipo('dlfr')
        valorPropio.assertEqual(valorPropio.búferTexto,'읽')
        for esperado in ('일','이','ㅇ',''):
            valorPropio.teclaPulsar(0xff08); valorPropio.assertEqual(valorPropio.búferTexto,esperado)
        valorPropio.categoríaTipo('gksk'); valorPropio.assertEqual(valorPropio.búferTexto,'valorUno')
        valorPropio.teclaPulsar(0xff08); valorPropio.assertEqual(valorPropio.búferTexto,'하ㄴ')

    def pruebaConfirmarYRepetirModos(valorPropio):
        valorPropio.categoríaTipo('echo ')
        valorPropio.entradaElementoTeclado.valorPulsado(True,0xffe1)
        valorPropio.entradaElementoTeclado.valorPulsado(True,32); valorPropio.entradaElementoTeclado.valorPulsado(True,32)
        valorPropio.entradaElementoTeclado.valorPulsado(False,32); valorPropio.entradaElementoTeclado.valorPulsado(False,0xffe1)
        valorPropio.assertTrue(valorPropio.entradaElementoTeclado.coreano)
        valorPropio.categoríaTipo('gksrmf'); valorPropio.teclaPulsar(0xff31); valorPropio.categoríaTipo(' English')
        valorPropio.assertEqual(valorPropio.búferTexto,'echo 한글 English')
        valorPropio.assertFalse(valorPropio.entradaElementoTeclado.coreano)
        valorPropio.teclaPulsar(0xffc6); valorPropio.categoríaTipo('rk'); valorPropio.teclaPulsar(0xff51)
        valorPropio.categoríaTipo('sk'); valorPropio.assertTrue(valorPropio.búferTexto.endswith('operandoPrimero\x1b[D나'))

    def pruebaUnicodeYPegar(valorPropio):
        valorPropio.teclaPulsar(0xffc6); valorPropio.categoríaTipo('rk')
        valorPropio.entradaElementoTeclado.valorPortapapeles='valorPegar'.encode()
        valorPropio.entradaElementoTeclado.valorPulsado(True,0xffe3); valorPropio.entradaElementoTeclado.valorPulsado(True,0xffe1)
        valorPropio.teclaPulsar(ord('v'))
        valorPropio.entradaElementoTeclado.valorPulsado(False,0xffe1); valorPropio.entradaElementoTeclado.valorPulsado(False,0xffe3)
        valorPropio.teclaPulsar(0x0100d55c); valorPropio.categoríaTipo('sk')
        valorPropio.assertEqual(valorPropio.búferTexto,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
