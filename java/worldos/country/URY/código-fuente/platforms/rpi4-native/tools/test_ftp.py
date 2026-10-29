#!/usr/bin/env python3
"""기존 ruta 호환 puntoEntradaElemento. datosEfectivo implementación: ../Herramientas/pruebaFTP.py"""
import importlib as valorTomar
import sys as valorSistemaOperación
from pathlib import Path as ruta
valorSistemaOperación.path.insert(0, str(ruta(__file__).resolve().parents[1] / 'Herramientas'))
if __name__ == '__main__':
    import runpy as LanzadorPrograma
    LanzadorPrograma.run_module('pruebaFTP', run_name='__main__', alter_sys=True)
else:
    implementación = valorTomar.import_module('pruebaFTP')
    valorAsociación = {'timeout': 'tiempoEsperaEjecución', 'payload': 'datosCargaÚtil', 'broken': 'dañado', 'linux_example': 'ejemploLinux', 'chunk': 'valorFragmento', 'data': 'Datos', 'proc': 'proceso', 'code': 'secuenciaInstrucciónMáquina', 'linux': 'archivoLinux', 'archive': 'archivoComprimido', 'main': 'ponerEnMarcha', 'net_source': 'fuenteRedCorta', 'temporary': 'temporal', 'static_source': 'fuenteEstático', 'java_source': 'fuenteJava', 'echo': 'entradaElementoServidorRepetirEntrada', 'ROOT': 'raízProyecto', 'text': 'texto', 'marker': 'marcador', 'EchoFixture': 'DispositivoPruebaRepetirEntrada', 'command': 'comando', 'out': 'datosResultado', 'expected': 'esperado', 'server_source': 'fuenteServidor', 'shell': 'intérpreteComandos', 'upload': 'archivosSubir', 'transcript': 'transcripción', 'port': 'númeroPuerto', 'native': 'nativo', 'elf': 'archivoCódigoEjecutable', 'server_udp_port': 'puertoDatagramaServidor', 'packed': 'empaquetado', 'bridge': 'puente', 'selector': 'selector', 'end': 'desfaseFin', 'e': 'entradaElementoAuxiliar', 'ftp': 'conexiónTransferenciaArchivo', 'key': 'valorPulsado', 'bytecode': 'códigoBytes', 'peer': 'valorParRed', 'result': 'resultado', 'unchanged': 'datosPreservado', 'line': 'línea', 'server_tcp_port': 'puertoFlujoServidor', 'source': 'datosOriginal', 'NetworkBridge': 'puenteRed', 'jar': 'paqueteJava', 'receive': 'recibirMensaje', 'report': 'informeValidación'}
    for elementoListaElementoPrevio, elementoListaActual in valorAsociación.items():
        if hasattr(implementación, elementoListaActual): globals()[elementoListaElementoPrevio] = getattr(implementación, elementoListaActual)
