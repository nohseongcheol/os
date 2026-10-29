#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/construirEspacioUsuario.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('construirEspacioUsuario', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('construirEspacioUsuario')
    valorAsociación = {'mode': 'modoMétodo', 'header': 'valorEncabezado', 'i': 'índiceOrdinal', 'build_ccompiler': 'crearCompiladorC', 'ar': 'herramientaArchivoComprimido', 'posix': 'pOSIX', 'payload': 'datosCargaÚtil', 'flags': 'bitsConfiguración', 'cases': 'pruebaCaso', 'cc': 'CompiladorC', 'data': 'Datos', 'build_java_library': 'crearBibliotecaJava', 'ld': 'herramientaEnlazador', 'repo': 'rutaRepositorio', 'build_python': 'crearPython', 'inc': 'rutaIncluir', 'argument': 'valorReenviado', 'text': 'texto', 'headers': 'listaEncabezado', 'cxx': 'compiladorCpp', 'valid': 'válido', 'build': 'construir', 'build_users': 'crearEspacioUsuario', 'compiler': 'herramientaCompilador', 'uzlib': 'bibliotecaDescompresión', 'extra': 'regiónAdicional', 'phoff': 'desfaseEncabezadoPrograma', 'offset': 'valorDesfase', 'text_address': 'direcciónComando', 'abi': 'ABILlamada', 'assembly': 'ensamblador', 'run': 'ejecutarComando', 'path': 'ruta', 'p': 'posiciónDatos', 'changed': 'cambiado', 'n': 'númeroElementosElementoLista', 'flag': 'valorAjustes', 'index': 'índiceBuscar', 'classes': 'rutaClase', 'output': 'salida', 'loads': 'cargas', 'data_address': 'direcciónDatos', 'symbol': 'valorSímbolo', 'root': 'direcciónRaíz', 'patches': 'modificaciones', 'source': 'datosOriginal', 'sizes': 'tamaños', 'blobs': 'bloquesBinarios', 'name': 'nombre', 'value': 'valor', 'fmt': 'formatoDatos', 'work': 'rutaTrabajoEnCurso'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
