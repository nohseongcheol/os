#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/pruebaRemmina.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('pruebaRemmina', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('pruebaRemmina')
    valorAsociación = {'wait': 'esperarFin', 'typing': 'carácterIngresado', 'start': 'ponerEnMarcha', 'profile': 'perfil', 'focused': 'enfocado', 'serial': 'entradaSalidaSerie', 'keys': 'teclasPulsado', 'server': 'valorServidor', 'log': 'registroEntradaDiario', 'args': 'arregloArgumento', 'deadline': 'tiempoPlazo', 'data': 'Datos', 'candidate': 'candidato', 'logs': 'registrosDiario', 'kw': 'argumentoNombrado', 'number': 'valorNumérico', 'main': 'ponerEnMarcha', 'ready': 'terminadoPreparación', 'found': 'buscarCoincidenciaResultado', 'guest': 'invitado', 'ROOT': 'raízProyecto', 'marker': 'marcador', 'text': 'texto', 'out': 'datosResultado', 'env': 'entorno', 'f': 'entradaElementoArchivo', 'port': 'númeroPuerto', 'offset': 'valorDesfase', 'version': 'númeroVersión', 'p': 'posiciónDatos', 'selector': 'selector', 'xvfb': 'presentarVirtual', 'display': 'dispositivoPresentar', 'n': 'númeroElementosElementoLista', 'key': 'valorPulsado', 'processes': 'procesosEnEjecución', 'rootfs': 'sistemaArchivosRaíz', 'xdo': 'herramientaEntradaVirtual', 'name': 'nombre', 'window': 'ventana', 'report': 'informeValidación', 'work': 'rutaTrabajoEnCurso'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
