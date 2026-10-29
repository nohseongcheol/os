#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. Anfitrión 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from ejecutarComando import comando


def ponerEnMarcha():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('file', type=Path)
    analizador.add_argument('arguments', nargs='*')
    analizador.add_argument('--class-name', help='패키지가 있는 .class의 전체 nombre(예: validar.pruebaPaquete)')
    analizador.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 invocar ABI valorUsar')
    analizador.add_argument('--vnc', help='예: 127.0.0.1:2')
    analizador.add_argument('--include', action='append', type=Path, default=[], help='añadirFinalEntradaElemento class Archivo 또는 class 디렉터리(패키지 nombre retenerValor)')
    arregloArgumento = analizador.parse_args()
    Datos = arregloArgumento.file.read_bytes()
    if arregloArgumento.class_name and arregloArgumento.file.suffix != '.class': analizador.error('--class-name은 .class 입력에서 사용합니다.')
    nombre = arregloArgumento.class_name + '.class' if arregloArgumento.class_name else arregloArgumento.file.name
    if len(Datos) > 16384 or not 1 <= len(nombre.encode('utf-8')) <= 63 or '\n' in nombre or '\r' in nombre:
        analizador.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    valorCategoría = '.elf' if Datos[:4] == b'\x7fELF' else arregloArgumento.file.suffix
    if arregloArgumento.linux and valorCategoría != '.elf': analizador.error('--linux는 ELF 바이너리에만 사용합니다.')
    if valorCategoría not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        analizador.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(arregloArgumento.arguments) > 7 or any(len(datosCadena.encode('utf-8')) > 255 or '\n' in datosCadena or '\r' in datosCadena for datosCadena in arregloArgumento.arguments):
        analizador.error('인수는 valorMáximo 7개, 각각 UTF-8 255바이트 이하입니다.')
    opciones = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if arregloArgumento.vnc: opciones += ['-vnc', arregloArgumento.vnc]
    proceso = subprocess.Popen(comando() + opciones, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selector = selectors.DefaultSelector(); selector.register(proceso.stdout, selectors.EVENT_READ)
    def recibirMensaje(marcador, tiempoEsperaEjecución=45):
        salida = bytearray(); desfaseFin = time.monotonic() + tiempoEsperaEjecución
        while marcador not in salida:
            if time.monotonic() > desfaseFin: raise RuntimeError('UART timeout: ' + salida.decode('utf-8', 'replace'))
            for valorPulsado, _ in selector.select(0.1):
                valorFragmento = valorPulsado.fileobj.read(4096)
                if valorFragmento: salida.extend(valorFragmento)
            if b'PANIC:' in salida or b'FAIL ' in salida: raise RuntimeError(salida.decode('utf-8', 'replace'))
            if proceso.poll() is not None: raise RuntimeError('QEMU exited: ' + salida.decode('utf-8', 'replace'))
        return bytes(salida)
    def enviar(línea, marcador=b'jkoros-native> '):
        proceso.stdin.write(línea.encode('utf-8') + b'\n'); proceso.stdin.flush()
        return recibirMensaje(marcador)
    def ejecutarComando(línea):
        salida = enviar(línea); sys.stdout.buffer.write(salida); sys.stdout.buffer.flush()
        esIgual = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', salida)
        if not esIgual: raise RuntimeError('guest did not report exit status')
        return int(esIgual.group(1))
    try:
        recibirMensaje(b'jkoros-native> ')
        listaArchivo = []
        for incluir in arregloArgumento.include:
            if incluir.is_dir():
                listaArchivo += [(str(posiciónDatos.relative_to(incluir).with_suffix('')).replace('/', '.') + '.class', posiciónDatos.read_bytes()) for posiciónDatos in sorted(incluir.rglob('*.class'))]
            else:
                listaArchivo.append((incluir.name, incluir.read_bytes()))
        listaArchivo = [(númeroElementosElementoLista, datosDestino) for númeroElementosElementoLista, datosDestino in listaArchivo if númeroElementosElementoLista != nombre] + [(nombre, Datos)]
        for nombreSubir, datosSubir in listaArchivo:
            if len(datosSubir) > 16384 or len(nombreSubir.encode('utf-8')) > 63 or '\n' in nombreSubir or '\r' in nombreSubir:
                raise ValueError('añadirFinalEntradaElemento 파일의 nombre/tamaño valorLímite 초과: ' + nombreSubir)
            enviar('load ' + shlex.quote(nombreSubir), b'hex> ')
            for índiceOrdinal in range(0, len(datosSubir), 64): enviar(datosSubir[índiceOrdinal:índiceOrdinal+64].hex(), b'hex> ')
            if b'LOADED' not in enviar('.'): raise RuntimeError('upload failed: ' + nombreSubir)
            volcado = enviar('hex ' + shlex.quote(nombreSubir))
            esIgual = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', volcado, re.S)
            if not esIgual or bytes.fromhex(''.join(esIgual.group(2).decode().split())) != datosSubir: raise RuntimeError('upload verification failed')
        if valorCategoría == '.java' and ejecutarComando('javac ' + shlex.quote(nombre)) != 0: return 1
        imagenCódigoEjecutable = arregloArgumento.file.stem + '.elf'
        if valorCategoría == '.c' and ejecutarComando('cc ' + shlex.quote(nombre) + ' -o ' + shlex.quote(imagenCódigoEjecutable)) != 0: return 1
        programa = 'java ' + shlex.quote(arregloArgumento.class_name or arregloArgumento.file.stem) if valorCategoría in ('.java', '.class') else ('python ' if valorCategoría == '.py' else 'run ') + shlex.quote(nombre)
        if valorCategoría == '.jar': programa = 'java -jar ' + shlex.quote(nombre)
        if valorCategoría == '.c': programa = 'run ' + shlex.quote(imagenCódigoEjecutable)
        if arregloArgumento.linux: programa = 'run --linux ' + shlex.quote(nombre)
        if arregloArgumento.arguments: programa += ' ' + ' '.join(shlex.quote(datosCadena) for datosCadena in arregloArgumento.arguments)
        return 0 if ejecutarComando(programa) == 0 else 1
    finally:
        if proceso.poll() is None:
            proceso.terminate()
            try: proceso.wait(timeout=5)
            except subprocess.TimeoutExpired: proceso.kill(); proceso.wait(timeout=5)
        selector.close(); proceso.stdin.close(); proceso.stdout.close()


if __name__ == '__main__':
    raise SystemExit(ponerEnMarcha())
