#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/pruebaELF.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('pruebaELF', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('pruebaELF')
    valorAsociación = {'out': 'datosResultado', 'expected': 'esperado', 'phoff': 'desfaseEncabezadoPrograma', 'offset': 'valorDesfase', 'invalid': 'datosInválido', 'path': 'ruta', 'executable': 'imagenCódigoEjecutable', 'rejected': 'resultadoRechazo', 'linux_example': 'ejemploLinux', 'original': 'original', 'result': 'resultado', 'format_': 'especificarFormato', 'main': 'ponerEnMarcha', 'content': 'valorContenidoValor', 'source': 'datosOriginal', 'name': 'nombre', 'reference': 'líneaReferenciaComparación', 'ROOT': 'raízProyecto', 'value': 'valor', 'report': 'informeValidación'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
