#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/pruebaJVM.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('pruebaJVM', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('pruebaJVM')
    valorAsociación = {'message': 'textoNotificación', 's': 'datosCadena', 'actual': 'resultadoEfectivo', 'match': 'esIgual', 'payload': 'datosCargaÚtil', 'cases': 'pruebaCaso', 'fixture': 'pruebaDatos', 'main': 'ponerEnMarcha', 'ROOT': 'raízProyecto', 'text': 'texto', 'valid': 'válido', 'includes': 'inclusiones', 'include': 'incluir', 'expected': 'esperado', 'sources': 'ListaFuentes', 'tmp': 'rutaTemporal', 'done': 'importeCompletado', 'classes': 'rutaClase', 'output': 'salida', 'result': 'resultado', 'cmd': 'argumentosComando', 'name': 'nombre', 'jar': 'paqueteJava', 'report': 'informeValidación', 'tests': 'pruebaLista'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
