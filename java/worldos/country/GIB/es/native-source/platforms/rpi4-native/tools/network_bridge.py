#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/puenteRed.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('puenteRed', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('puenteRed')
    valorAsociación = {'response': 'respuestaRetorno', 'parts': 'componenteRuta', 's': 'datosCadena', 'i': 'índiceOrdinal', 'close': 'cerrar', 'forward': 'reglaReenvíoEnCurso', 'slip_input': 'entradaSLIP', 'self': 'valorPropio', 'item': 'valorEntradaElemento', 'flags': 'bitsConfiguración', 'ftp_port': 'númeroPuertoTransferenciaArchivo', 'args': 'arregloArgumento', 'server': 'valorServidor', 'data': 'Datos', 'ethernet_input': 'entradaEthernet', 'trace_packet': 'paqueteDatosTraza', 'GATEWAY': 'direcciónEquipoFísicoPasarela', 'rule': 'valorRegla', 'protocol': 'ABIRed', 'forwards': 'reglasReenvíoEnCurso', 'occupied': 'ocupado', 'host': 'Anfitrión', 'ack': 'númeroConfirmación', 'serial_port': 'númeroPuertoSerie', 'readers': 'lectores', 'guest': 'invitado', 'destination': 'direcciónDatosDestino', 'ethernet_port': 'puertoEthernet', 'b': 'valorSegundo', 'MAC': 'direcciónMáquina', 'arp': 'paqueteDatosResoluciónDirección', 'writable': 'escribible', 'direction': 'direcciónSentido', 'seq': 'númeroOrden', 'frame': 'marcoEjecución', 'loop': 'valorCiclo', 'port': 'númeroPuerto', 'offset': 'valorDesfase', 'readable': 'puedeLeer', 'c': 'códigoCarácter', 'p': 'posiciónDatos', 'writers': 'escritores', 'IP': 'valorDirecciónInternet', 'e': 'entradaElementoAuxiliar', 'n': 'númeroElementosElementoLista', 'packet': 'datosPaqueteDatos', 'arguments': 'argumentoReenviado', 'source': 'datosOriginal', 'NetworkBridge': 'puenteRed', 'window': 'ventana', 'capture': 'capturarDatos'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
