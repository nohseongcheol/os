#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/pruebaFlujo.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('pruebaFlujo', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('pruebaFlujo')
    valorAsociación = {'out': 'datosResultado', 'main': 'ponerEnMarcha', 'ROOT': 'raízProyecto', 'p': 'posiciónDatos', 'text': 'texto', 'report': 'informeValidación'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
