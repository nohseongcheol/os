#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/pruebaColecciónEjemplos.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('pruebaColecciónEjemplos', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('pruebaColecciónEjemplos')
    valorAsociación = {'count': 'númeroElementosEntradaElemento', 'exact': 'valorExacto', 'expected_file': 'archivoEsperado', 'ftp_port': 'númeroPuertoTransferenciaArchivo', 'data': 'Datos', 'graphics_command': 'comandoGráficos', 'main': 'ponerEnMarcha', 'row': 'posiciónFila', 'init': 'valorInicialValor', 'target': 'valorObjetivo', 'ROOT': 'raízProyecto', 'text': 'texto', 'binary': 'binario', 'out': 'datosResultado', 'entry': 'puntoEntradaElemento', 'got': 'númeroElementosRecibido', 'port': 'númeroPuerto', 'graphics_start': 'iniciarDibujo', 'col': 'posiciónColumna', 'begin': 'iniciarDesfase', 'kind': 'valorCategoría', 'selector': 'selector', 'n': 'númeroElementosElementoLista', 'key': 'valorPulsado', 'y': 'coordenadaCoordenadaVertical', 'client': 'cliente', 'line': 'línea', 'report': 'informeValidación', 'language': 'Lengua', 'x': 'coordenadaCoordenadaHorizontal', 'start': 'ponerEnMarcha', 'rgb': 'colorRGB', 'down': 'esPulsaciónEnCurso', 'listing': 'enviarLista', 'payload': 'datosCargaÚtil', 'proc': 'proceso', 'w': 'valorAnchuraSolicitado', 'temporary': 'temporal', 'echo': 'entradaElementoServidorRepetirEntrada', 'label': 'tablaNombre', 'content': 'valorContenidoValor', 'argument': 'valorReenviado', 'EchoServers': 'ServidoresRepetirEntrada', 'marker': 'marcador', 'expected': 'esperado', 'test_language': 'pruebaLengua', 'filename': 'nombreEntradaElementoArchivo', 'shell': 'intérpreteComandos', 'color': 'colorPíxel', 'transcript': 'transcripción', 'offset': 'valorDesfase', 'h': 'valorAlturaSolicitado', 'run': 'ejecutarComando', 'c': 'códigoCarácter', 'path': 'ruta', 'encoding': 'juegoCaracteres', 'end': 'desfaseFin', 'ftp': 'conexiónTransferenciaArchivo', 'pixels': 'listaPíxeles', 'symbol': 'valorSímbolo', 'source': 'datosOriginal', 'name': 'nombre', 'receive': 'recibirMensaje', 'manifest': 'manifiestoPaquete'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
