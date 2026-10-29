#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/construirColecciónEjemplos.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('construirColecciónEjemplos', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('construirColecciónEjemplos')
    valorAsociación = {'out': 'datosResultado', 'build_examples': 'crearColecciónEjemplos', 'files': 'listaArchivo', 'java': 'ejecutarJava', 'run': 'ejecutarComando', 'path': 'ruta', 'p': 'posiciónDatos', 'readme': 'léame', 'build_java_library': 'crearBibliotecaJava', 'code': 'secuenciaInstrucciónMáquina', 'index': 'índiceBuscar', 'classes': 'rutaClase', 'repo': 'rutaRepositorio', 'root': 'direcciónRaíz', 'content': 'valorContenidoValor', 'source': 'datosOriginal', 'name': 'nombre', 'target': 'valorObjetivo', 'manifest': 'manifiestoPaquete', 'language': 'Lengua'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
