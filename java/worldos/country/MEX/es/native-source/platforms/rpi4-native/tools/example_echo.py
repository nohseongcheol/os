#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/ServidorEcoEjemplo.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('ServidorEcoEjemplo', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('ServidorEcoEjemplo')
    valorAsociación = {'data': 'Datos', 'sock': 'valorConectorRed', 'tcp_port': 'puertoTCP', 'chunk': 'valorFragmento', 'received': 'tieneRecibido', 'self': 'valorPropio', 'UDP': 'peticiónManejadorDatagrama', 'thread': 'tareaFondo', 'echo': 'entradaElementoServidorRepetirEntrada', 'TCP': 'peticiónConexiónManejador', 'EchoServers': 'ServidoresRepetirEntrada', 'parser': 'analizador', 'server': 'valorServidor', 'udp_port': 'puertoUDP', 'args': 'arregloArgumento'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
