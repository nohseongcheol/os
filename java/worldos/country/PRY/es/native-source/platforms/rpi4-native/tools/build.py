#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/construirSistema.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('construirSistema', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('construirSistema')
    valorAsociación = {'network': 'red', 'BUILD': 'construirRuta', 'ar': 'herramientaArchivoComprimido', 'build_examples': 'crearColecciónEjemplos', 'posix': 'pOSIX', 'font_data': 'datosFuenteTipográfica', 'flags': 'bitsConfiguración', 'a': 'valorPrimero', 'cc': 'CompiladorC', 'args': 'arregloArgumento', 'source_flags': 'configuraciónOriginal', 'ld': 'herramientaEnlazador', 'method': 'entradaElementoMétodo', 'main': 'ponerEnMarcha', 'objcopy': 'convertidorArchivoObjeto', 'ROOT': 'raízProyecto', 'cxx': 'compiladorCpp', 'includes': 'inclusiones', 'compiler': 'herramientaCompilador', 'build_users': 'crearEspacioUsuario', 'f': 'entradaElementoArchivo', 'extra': 'regiónAdicional', 'exports': 'tablaExportar', 'jobs': 'construirTrabajos', 'run': 'ejecutarComando', 'path': 'ruta', 'REPO': 'raízRepositorio', 'tool': 'Herramientas', 'classes': 'rutaClase', 'output': 'salida', 'samples': 'entradasEjemplo', 'symbol': 'valorSímbolo', 'source': 'datosOriginal', 'name': 'nombre', 'build_network': 'crearRed', 'font_info': 'informaciónFuenteTipográfica', 'manifest': 'manifiestoPaquete', 'work': 'rutaTrabajoEnCurso'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
