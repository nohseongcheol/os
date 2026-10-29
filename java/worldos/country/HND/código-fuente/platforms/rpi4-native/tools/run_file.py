#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/ejecutarArchivo.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('ejecutarArchivo', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('ejecutarArchivo')
    valorAsociación = {'timeout': 'tiempoEsperaEjecución', 's': 'datosCadena', 'i': 'índiceOrdinal', 'match': 'esIgual', 'files': 'listaArchivo', 'program': 'programa', 'executable': 'imagenCódigoEjecutable', 'args': 'arregloArgumento', 'chunk': 'valorFragmento', 'data': 'Datos', 'proc': 'proceso', 'send': 'enviar', 'main': 'ponerEnMarcha', 'marker': 'marcador', 'command': 'comando', 'include': 'incluir', 'dumped': 'volcado', 'run': 'ejecutarComando', 'p': 'posiciónDatos', 'parser': 'analizador', 'options': 'opciones', 'kind': 'valorCategoría', 'selector': 'selector', 'upload_data': 'datosSubir', 'end': 'desfaseFin', 'n': 'númeroElementosElementoLista', 'd': 'datosDestino', 'key': 'valorPulsado', 'output': 'salida', 'line': 'línea', 'name': 'nombre', 'upload_name': 'nombreSubir', 'receive': 'recibirMensaje'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
