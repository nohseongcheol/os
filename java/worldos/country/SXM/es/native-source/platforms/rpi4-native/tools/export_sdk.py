#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/sDKExportar.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('sDKExportar', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('sDKExportar')
    valorAsociación = {'out': 'datosResultado', 'obj': 'archivoDestino', 'relative': 'rutaRelativo', 'compiler_archive': 'archivoComprimidoCompilador', 'sdk': 'juegoHerramientasDesarrollo', 'dist': 'rutaDistribución', 'archive': 'archivoComprimido', 'main': 'ponerEnMarcha', 'posix': 'pOSIX', 'files': 'listaArchivo', 'source': 'datosOriginal', 'name': 'nombre', 'target': 'valorObjetivo', 'ROOT': 'raízProyecto', 'destination': 'direcciónDatosDestino', 'manifest': 'manifiestoPaquete', 'work': 'rutaTrabajoEnCurso'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
