#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/construirBibliotecaJava.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('construirBibliotecaJava', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('construirBibliotecaJava')
    valorAsociación = {'header': 'valorEncabezado', 'sources': 'ListaFuentes', 'i': 'índiceOrdinal', 'info': 'informaciónSistema', 'payload': 'datosCargaÚtil', 'src': 'direcciónOriginal', 'run': 'ejecutarComando', 'build_java_library': 'crearBibliotecaJava', 'relative': 'rutaRelativo', 'classes': 'rutaClase', 'dist': 'rutaDistribución', 'archive': 'archivoComprimido', 'output': 'salida', 'root': 'direcciónRaíz', 'name': 'nombre', 'jar': 'paqueteJava', 'b': 'valorSegundo', 'entries': 'listaEntradas'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
