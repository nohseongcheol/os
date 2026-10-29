#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/ejecutarComando.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('ejecutarComando', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('ejecutarComando')
    valorAsociación = {'supported': 'funcionalidadesAdmitido', 'parser': 'analizador', 'qemu': 'MáquinaDoblePrueba', 'run_desktop': 'ponerEnMarchaEscritorio', 'main': 'ponerEnMarcha', 'host': 'Anfitrión', 'status': 'valorEstadoValor', 'NetworkBridge': 'puenteRed', 'ROOT': 'raízProyecto', 'bridge': 'puente', 'loader': 'cargador', 'base': 'valorFondo', 'options': 'opciones', 'binary': 'binario', 'args': 'arregloArgumento', 'command': 'comando'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
