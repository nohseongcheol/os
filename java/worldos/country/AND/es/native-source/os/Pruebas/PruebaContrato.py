#!/usr/bin/env python3
"""Anfitrión libc 없이 연결한 español C 프로그램을 datosEfectivo ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from pruebaRedUsuario import MáquinaVirtual

posición = Path(__file__).resolve().parents[1]

def ejecutarComando():
    resultado = {}
    valorServidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    valorServidor.bind(('127.0.0.1', 0))
    valorServidor.settimeout(0.1)
    númeroPuerto = valorServidor.getsockname()[1]
    datosRecibido = []
    estadoValorEstadoTerminación = threading.Event()
    def respuestaRepetirEntrada():
        while not estadoValorEstadoTerminación.is_set():
            try:
                Datos, dirección = valorServidor.recvfrom(4096)
            except socket.timeout:
                continue
            datosRecibido.append(Datos)
            valorServidor.sendto(Datos, dirección)
    valorTareaFondo = threading.Thread(target=respuestaRepetirEntrada, daemon=True)
    valorTareaFondo.start()
    try:
        for valorClaseTipo in ('elf', 'iso'):
            máquina = MáquinaVirtual(posición / ('build/kernel.' + valorClaseTipo), valorClaseTipo)
            try:
                for valorIteración in range(2):
                    máquina.comando('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    máquina.comando('run posixudp ' + str(númeroPuerto), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                ponerEnMarcha = len(máquina.registroEntradaDiario)
                máquina.valorSerie.sendall(b'run posixinput\n')
                máquina.esperarEstadoValor('POSIX INPUT READY', ponerEnMarcha)
                máquina.valorSerie.sendall(b'abcdef')
                Salida = máquina.esperarEstadoValor('jkoros> ', ponerEnMarcha)
                assert 'POSIX INPUT PASS' in Salida and 'Exit: 0' in Salida, Salida
                máquina.comando('javac Hello.java', ['Exit: 0'])
                máquina.comando('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                máquina.comando('run hello recovered', ['arg: recovered', 'Exit: 0'])
                resultado[valorClaseTipo] = máquina.registroEntradaDiario.decode('utf-8', 'replace')
                print('PASS:', valorClaseTipo, 'POSIX Archivo/공유 posición/삭제 수명/dirección protegerValor/UDP/표준 valorEntrada/기존 Java', flush=True)
            finally:
                máquina.cerrar()
        assert b'posix-udp' in datosRecibido and b'truncate' in datosRecibido and b'' in datosRecibido
    finally:
        estadoValorEstadoTerminación.set(); valorTareaFondo.join(timeout=2); valorServidor.close()
    resultado['host_datagrams'] = [Datos.decode() for Datos in datosRecibido]
    (posición / 'build/PruebaContrato.json').write_text(json.dumps(resultado, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ejecutarComando()
