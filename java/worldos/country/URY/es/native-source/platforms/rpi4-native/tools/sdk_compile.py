#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/compilarSDK.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('compilarSDK', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('compilarSDK')
    valorAsociación = {'compiler': 'herramientaCompilador', 'obj': 'archivoDestino', 'sdk': 'juegoHerramientasDesarrollo', 'output': 'salida', 'main': 'ponerEnMarcha', 'elf': 'archivoCódigoEjecutable', 'is_c': 'esLenguaC', 'parser': 'analizador', 'language': 'Lengua', 'work': 'rutaTrabajoEnCurso', 'args': 'arregloArgumento'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
