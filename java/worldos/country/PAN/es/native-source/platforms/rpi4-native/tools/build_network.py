#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/construirRed.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('construirRed', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('construirRed')
    valorAsociación = {'obj': 'archivoDestino', 'objects': 'archivosDestino', 'library': 'biblioteca', 'output': 'salida', 'port': 'númeroPuerto', 'root': 'direcciónRaíz', 'files': 'listaArchivo', 'source': 'datosOriginal', 'run': 'ejecutarComando', 'flags': 'bitsConfiguración', 'path': 'ruta', 'build_network': 'crearRed', 'cc': 'CompiladorC', 'ar': 'herramientaArchivoComprimido'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
