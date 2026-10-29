#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/PruebaArranque.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('PruebaArranque', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('PruebaArranque')
    valorAsociación = {'timeout': 'tiempoEsperaEjecución', 'response': 'respuestaRetorno', 'msg': 'mensajeRed', 'exact': 'valorExacto', 'markers': 'marcadores', 'i': 'índiceOrdinal', 'match': 'esIgual', 'execute': 'ejecutarTarea', 'cancel': 'operaciónCancelar', 'cmd_byte': 'byteComando', 'reply': 'respuesta', 'points': 'puntos', 'server': 'valorServidor', 'data': 'Datos', 'prompt': 'indicadorEntrada', 'enter': 'entrar', 'imported': 'importado', 'send': 'enviar', 'main': 'ponerEnMarcha', 'ROOT': 'raízProyecto', 'text': 'texto', 'first_gui': 'gUIPrimero', 'pixel': 'píxel', 'java_class': 'claseJava', 'upload': 'archivosSubir', 'pixels_file': 'archivoPíxel', 'pixels_data': 'datosPíxel', 'edit': 'valorEditar', 'receive_until': 'recibirHasta', 'selector': 'selector', 'size': 'tamaño', 'qmp_path': 'rutaQMP', 'key': 'valorPulsado', 'second_gui': 'gUISegundo', 'y': 'coordenadaCoordenadaVertical', 'result': 'resultado', 'samples': 'entradasEjemplo', 'client': 'cliente', 'line': 'línea', 'report': 'informeValidación', 'work': 'rutaTrabajoEnCurso', 'x': 'coordenadaCoordenadaHorizontal', 'python_checks': 'comprobacionesPython', 'download': 'descargar', 'greeting': 'Saludo', 'dims': 'valorDimensiones', 'chunk': 'valorFragmento', 'deadline': 'tiempoPlazo', 'proc': 'proceso', 'content': 'valorContenidoValor', 'block': 'bloqueDatos', 'marker': 'marcador', 'command': 'comando', 'expected': 'esperado', 'shell': 'intérpreteComandos', 'drawing': 'rutaDibujo', 'f': 'entradaElementoArchivo', 'transcript': 'transcripción', 'offset': 'valorDesfase', 'path': 'ruta', 'screenshot': 'capturaPantalla', 'arguments': 'argumentoReenviado', 'pixels': 'listaPíxeles', 'viewer': 'clientePantalla', 'output': 'salida', 'stream': 'valorFlujo', 'cmd': 'argumentosComando', 'name': 'nombre', 'qmp': 'conexiónControlDoblePrueba'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
