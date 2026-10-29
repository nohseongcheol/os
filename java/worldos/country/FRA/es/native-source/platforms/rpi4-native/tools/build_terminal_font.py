#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/construirFuenteTipográficaTerminal.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('construirFuenteTipográficaTerminal', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('construirFuenteTipográficaTerminal')
    valorAsociación = {'data': 'Datos', 'img': 'Dibujo', 'bits': 'listaBits', 'x': 'coordenadaCoordenadaHorizontal', 'draw': 'dibujarPantalla', 'licences': 'licencias', 'paths': 'listaRuta', 'y': 'coordenadaCoordenadaVertical', 'main': 'ponerEnMarcha', 'src': 'direcciónOriginal', 'fonts': 'listaFuenteTipográfica', 'ROOT': 'raízProyecto', 'p': 'posiciónDatos', 'cp': 'codificaciónEstadoCarácter', 'target': 'valorObjetivo'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
