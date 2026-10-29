#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/vistaEscritorio.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('vistaEscritorio', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('vistaEscritorio')
    valorAsociación = {'count': 'númeroElementosEntradaElemento', 'special': 'teclaEspecial', 'error': 'error', 'exact': 'valorExacto', 'network': 'red', 'closed': 'esCerrado', 'length': 'longitud', 'opened': 'abierto', 'ftp_port': 'númeroPuertoTransferenciaArchivo', 'server': 'valorServidor', 'resources': 'recursos', 'data': 'Datos', 'shift': 'teclaDesplazar', 'send': 'enviar', 'run_desktop': 'ponerEnMarchaEscritorio', 'protocol': 'ABIRed', 'forwards': 'reglasReenvíoEnCurso', 'host': 'Anfitrión', 'text': 'texto', 'korean': 'coreano', 'port': 'númeroPuerto', 'signum': 'númeroSeñal', 'version': 'númeroVersión', 'parser': 'analizador', 'bridge': 'puente', 'kind': 'valorCategoría', 'tail': 'parteTerminación', 'size': 'tamaño', 'previous_buttons': 'botonesElementoPrevio', 'key': 'valorPulsado', 'y': 'coordenadaCoordenadaVertical', 'prefix': 'partePrevio', 'client': 'cliente', 'char': 'datosCarácter', 'work': 'rutaTrabajoEnCurso', 'Keyboard': 'Teclado', 'x': 'coordenadaCoordenadaHorizontal', 'down': 'esPulsaciónEnCurso', 'net': 'entradaElementoPuenteRed', 'self': 'valorPropio', 'mode_changed': 'cambiadoModo', 'serial': 'entradaSalidaSerie', 'args': 'arregloArgumento', 'Hangul': 'componerHangul', 'chunk': 'valorFragmento', 'proc': 'proceso', 'Desktop': 'conectarEscritorio', 'buttons': 'botones', 'thread': 'tareaFondo', 'pressed': 'esPulsado', 'previous': 'elementoPrevio', 'toggle': 'modoConmutar', 'command': 'comando', 'sock': 'valorConectorRed', 'frame': 'marcoEjecución', 'ctrl': 'teclaControl', 'path': 'ruta', 'cp': 'codificaciónEstadoCarácter', 'terminate': 'terminarProceso', 'security': 'seguridad', 'vnc_port': 'puertoVNC', 'body': 'textoCuerpo', 'index': 'índiceBuscar', 'exited': 'tieneSalido', 'keysym': 'símboloTecla', 'output': 'salida', 'keyboard': 'entradaElementoTeclado', 'interrupted': 'interrumpido', 'listener': 'recibirPuerto', 'reader': 'lector', 'NetworkBridge': 'puenteRed', 'gui': 'pantallaDibujo', 'worker': 'tareaProcesamiento'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
