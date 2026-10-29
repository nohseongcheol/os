#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/entradaHangul.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('entradaHangul', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('entradaHangul')
    valorAsociación = {'old': 'elementoListaElementoPrevio', 'backspace': 'retroceso', 'committed': 'confirmado', 'KEYS': 'disposiciónTecla', 'self': 'valorPropio', 'FINALS': 'letraHangulFinalPalabraCompuesta', 'VOWELS': 'letraHangulVocalMedialPalabraCompuesta', 'INITIAL': 'tablaLetraHangulInicialValor', 'initial': 'letraHangulInicialValor', 'commit': 'composiciónConfirmar', 'feed': 'teclaAlimentar', 'vowel': 'letraHangulVocalMedial', 'Hangul': 'componerHangul', 'SPLIT': 'separarLetraHangulFinal', 'final': 'letraHangulFinal', 'key': 'valorPulsado', 'send': 'enviar', 'left': 'ladoIzquierdo', 'FINAL': 'tablaLetraHangulFinal', 'history': 'historial', 'pair': 'parUno', 'char': 'datosCarácter', 'VOWEL': 'tablaLetraHangulVocalMedial', 'right': 'derecho', 'value': 'valor', 'text': 'texto'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
