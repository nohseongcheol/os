#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/pruebaEntradaHangul.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('pruebaEntradaHangul', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('pruebaEntradaHangul')
    valorAsociación = {'expected': 'esperado', 'Keyboard': 'Teclado', 'press': 'teclaPulsar', 'self': 'valorPropio', 'test_modes_repeat_and_commit': 'pruebaConfirmarYRepetirModos', 'keys': 'teclasPulsado', 'test_paste_and_unicode': 'pruebaUnicodeYPegar', 'data': 'Datos', 'key': 'valorPulsado', 'send': 'enviar', 'test_words': 'pruebaPalabras', 'InputTests': 'pruebaEntradaHangul', 'test_backspace': 'pruebaRetroceso', 'symbol': 'valorSímbolo', 'char': 'datosCarácter', 'type': 'categoríaTipo'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
