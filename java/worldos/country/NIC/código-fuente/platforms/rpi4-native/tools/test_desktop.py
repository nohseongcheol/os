#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/pruebaEscritorio.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('pruebaEscritorio', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('pruebaEscritorio')
    valorAsociación = {'x': 'coordenadaCoordenadaHorizontal', 'typing': 'carácterIngresado', 'message': 'textoNotificación', 'start': 'ponerEnMarcha', 'down': 'esPulsaciónEnCurso', 'exact': 'valorExacto', 'i': 'índiceOrdinal', 'press': 'teclaPulsar', 'rectangles': 'listaRectángulos', 'sym': 'símbolo', 'j': 'ordinalInterior', 'deadline': 'tiempoPlazo', 'proc': 'proceso', 'data': 'Datos', 'main': 'ponerEnMarcha', 'w': 'valorAnchuraSolicitado', 'init': 'valorInicialValor', 'block': 'bloqueDatos', 'ROOT': 'raízProyecto', 'text': 'texto', 'marker': 'marcador', 'report': 'informeValidación', 'until': 'hasta', 'clipboard': 'valorPortapapeles', 'dst': 'direcciónDestino', 'seen': 'entradasVisto', 'poll': 'monitorEstadoDisponibilidad', 'transcript': 'transcripción', 'port': 'númeroPuerto', 'offset': 'valorDesfase', 'h': 'valorAlturaSolicitado', 'src': 'direcciónOriginal', 'event': 'evento', 'encoding': 'juegoCaracteres', 'size': 'tamaño', 'key': 'valorPulsado', 'pixels': 'listaPíxeles', 'y': 'coordenadaCoordenadaVertical', 'output': 'salida', 'symbol': 'valorSímbolo', 'client': 'cliente', 'char': 'datosCarácter', 'rgb': 'colorRGB'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
