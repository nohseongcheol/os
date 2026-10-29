#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/construirCompiladorC.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('construirCompiladorC', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('construirCompiladorC')
    valorAsociación = {'out': 'datosResultado', 'builtins': 'elementosIntegrados', 'header': 'valorEncabezado', 'sdk': 'juegoHerramientasDesarrollo', 'build_ccompiler': 'crearCompiladorC', 'i': 'índiceOrdinal', 'elf': 'archivoCódigoEjecutable', 'run': 'ejecutarComando', 'flags': 'bitsConfiguración', 'path': 'ruta', 'p': 'posiciónDatos', 'cc': 'CompiladorC', 'obj': 'archivoDestino', 'flag': 'valorAjustes', 'ld': 'herramientaEnlazador', 'objects': 'archivosDestino', 'repo': 'rutaRepositorio', 'v': 'datosTemporal', 'upstream': 'origenSuperior', 'root': 'direcciónRaíz', 'assets': 'recursosVisuales', 'source': 'datosOriginal', 'name': 'nombre', 'includes': 'inclusiones'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
