#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/pruebaSwing.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('pruebaSwing', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('pruebaSwing')
    valorAsociación = {'wait': 'esperarFin', 'x': 'coordenadaCoordenadaHorizontal', 's': 'datosCadena', 'i': 'índiceOrdinal', 'sel': 'Selector', 'seconds': 'unidadSegundos', 'log': 'registroEntradaDiario', 'data': 'Datos', 'at': 'posiciónActual', 'send': 'enviar', 'main': 'ponerEnMarcha', 'req': 'valorPetición', 'hot': 'valorAtajo', 'pump': 'eventoManejador', 'ROOT': 'raízProyecto', 'marker': 'marcador', 'b': 'valorSegundo', 'command': 'comando', 'shell': 'intérpreteComandos', 'f': 'entradaElementoArchivo', 'click': 'botónPulsarRatón', 'k': 'índiceTercero', 'c': 'códigoCarácter', 'r': 'valorDevuelto', 'p': 'posiciónDatos', 'command_mode': 'modoComando', 'end': 'desfaseFin', 'classes': 'rutaClase', 'key': 'valorPulsado', 'y': 'coordenadaCoordenadaVertical', 'result': 'resultado', 'report': 'informeValidación', 'dest': 'posiciónValorDestino', 'work': 'rutaTrabajoEnCurso', 'qmp': 'conexiónControlDoblePrueba'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
