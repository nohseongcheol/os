#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/crearImagen.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('crearImagen', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('crearImagen')
    valorAsociación = {'total': 'capacidadTotal', 'start': 'ponerEnMarcha', 'firmware': 'valorProgramaFijo', 'files': 'listaArchivo', 'archive_base': 'baseArchivoComprimido', 'partition': 'archivoPartición', 'archive': 'archivoComprimido', 'main': 'ponerEnMarcha', 'block': 'bloqueDatos', 'ROOT': 'raízProyecto', 'boot': 'rutaArranque', 'stage': 'valorEtapa', 'out': 'datosResultado', 'expected': 'esperado', 'f': 'entradaElementoArchivo', 'src': 'direcciónOriginal', 'path': 'ruta', 'p': 'posiciónDatos', 'extracted': 'extraído', 'member': 'miembro', 'mbr': 'RegistroEntradaArranqueMaestro', 'image': 'imagen', 'sector_count': 'númeroElementosSector', 'dist': 'rutaDistribución', 'sha': 'calcularResumenHash', 'license_': 'licencia', 'source': 'datosOriginal', 'name': 'nombre', 'value': 'valor', 'manifest': 'manifiestoPaquete', 'dest': 'posiciónValorDestino', 'work': 'rutaTrabajoEnCurso'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
