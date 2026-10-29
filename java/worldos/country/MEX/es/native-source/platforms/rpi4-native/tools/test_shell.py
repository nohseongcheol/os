#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/pruebaIntérpreteComandos.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('pruebaIntérpreteComandos', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('pruebaIntérpreteComandos')
    valorAsociación = {'timeout': 'tiempoEsperaEjecución', 'x': 'coordenadaCoordenadaHorizontal', 'msg': 'mensajeRed', 'i': 'índiceOrdinal', 'reply': 'respuesta', 'call': 'invocar', 'args': 'arregloArgumento', 'chunk': 'valorFragmento', 'data': 'Datos', 'proc': 'proceso', 'long_text': 'textoLargo', 'restored': 'datosRestaurado', 'send': 'enviar', 'file': 'Archivo', 'main': 'ponerEnMarcha', 'found': 'buscarCoincidenciaResultado', 'ROOT': 'raízProyecto', 'text': 'texto', 'marker': 'marcador', 'command': 'comando', 'expected': 'esperado', 'pixel': 'píxel', 'shell': 'intérpreteComandos', 'poll': 'monitorEstadoDisponibilidad', 'transcript': 'transcripción', 'end': 'desfaseFin', 'image': 'imagen', 'key': 'valorPulsado', 'y': 'coordenadaCoordenadaVertical', 'output': 'salida', 'result': 'resultado', 'client': 'cliente', 'line': 'línea', 'stream': 'valorFlujo', 'name': 'nombre', 'value': 'valor', 'receive': 'recibirMensaje', 'report': 'informeValidación', 'work': 'rutaTrabajoEnCurso', 'qmp': 'conexiónControlDoblePrueba'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
