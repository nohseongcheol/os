#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. hospedar 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from executar_comando import Orde


def Executar_2():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('file', type=Path)
    analizador.add_argument('arguments', nargs='*')
    analizador.add_argument('--class-name', help='패키지가 있는 .class의 전체 Nome(예: validar.꾸러미시험)')
    analizador.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    analizador.add_argument('--vnc', help='예: 127.0.0.1:2')
    analizador.add_argument('--include', action='append', type=Path, default=[], help='Anexar_introdución class Ficheiro 또는 class 디렉터리(패키지 Nome 유지)')
    argumento_MATRIZ = analizador.parse_args()
    datos = argumento_MATRIZ.file.read_bytes()
    if argumento_MATRIZ.class_name and argumento_MATRIZ.file.suffix != '.class': analizador.error('--class-name은 .class 입력에서 사용합니다.')
    Nome = argumento_MATRIZ.class_name + '.class' if argumento_MATRIZ.class_name else argumento_MATRIZ.file.name
    if len(datos) > 16384 or not 1 <= len(Nome.encode('utf-8')) <= 63 or '\n' in Nome or '\r' in Nome:
        analizador.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    Categoría_VALOR = '.elf' if datos[:4] == b'\x7fELF' else argumento_MATRIZ.file.suffix
    if argumento_MATRIZ.linux and Categoría_VALOR != '.elf': analizador.error('--linux는 ELF 바이너리에만 사용합니다.')
    if Categoría_VALOR not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        analizador.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argumento_MATRIZ.arguments) > 7 or any(len(cadea_datos.encode('utf-8')) > 255 or '\n' in cadea_datos or '\r' in cadea_datos for cadea_datos in argumento_MATRIZ.arguments):
        analizador.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Opcións = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argumento_MATRIZ.vnc: Opcións += ['-vnc', argumento_MATRIZ.vnc]
    Proceso = subprocess.Popen(Orde() + Opcións, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    준비선택기 = selectors.DefaultSelector(); 준비선택기.register(Proceso.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); finalizar_DESPRAZAMENTO = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > finalizar_DESPRAZAMENTO: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in 준비선택기.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Proceso.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def enviar(Liña, 확인표시=b'jkoros-native> '):
        Proceso.stdin.write(Liña.encode('utf-8') + b'\n'); Proceso.stdin.flush()
        return 수신하기(확인표시)
    def executar_comando(Liña):
        출력결과 = enviar(Liña); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        Ficheiro_Lista = []
        for 포함항목 in argumento_MATRIZ.include:
            if 포함항목.is_dir():
                Ficheiro_Lista += [(str(datos_cargo.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', datos_cargo.read_bytes()) for datos_cargo in sorted(포함항목.rglob('*.class'))]
            else:
                Ficheiro_Lista.append((포함항목.name, 포함항목.read_bytes()))
        Ficheiro_Lista = [(elemento_CONTAR, destino_datos) for elemento_CONTAR, destino_datos in Ficheiro_Lista if elemento_CONTAR != Nome] + [(Nome, datos)]
        for carga_nome, carga_datos in Ficheiro_Lista:
            if len(carga_datos) > 16384 or len(carga_nome.encode('utf-8')) > 63 or '\n' in carga_nome or '\r' in carga_nome:
                raise ValueError('Anexar_introdución 파일의 Nome/Tamaño 제한 초과: ' + carga_nome)
            enviar('load ' + shlex.quote(carga_nome), b'hex> ')
            for 순번 in range(0, len(carga_datos), 64): enviar(carga_datos[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in enviar('.'): raise RuntimeError('upload failed: ' + carga_nome)
            갈무리자료 = enviar('hex ' + shlex.quote(carga_nome))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != carga_datos: raise RuntimeError('upload verification failed')
        if Categoría_VALOR == '.java' and executar_comando('javac ' + shlex.quote(Nome)) != 0: return 1
        실행가능파일 = argumento_MATRIZ.file.stem + '.elf'
        if Categoría_VALOR == '.c' and executar_comando('cc ' + shlex.quote(Nome) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        apl = 'java ' + shlex.quote(argumento_MATRIZ.class_name or argumento_MATRIZ.file.stem) if Categoría_VALOR in ('.java', '.class') else ('python ' if Categoría_VALOR == '.py' else 'run ') + shlex.quote(Nome)
        if Categoría_VALOR == '.jar': apl = 'java -jar ' + shlex.quote(Nome)
        if Categoría_VALOR == '.c': apl = 'run ' + shlex.quote(실행가능파일)
        if argumento_MATRIZ.linux: apl = 'run --linux ' + shlex.quote(Nome)
        if argumento_MATRIZ.arguments: apl += ' ' + ' '.join(shlex.quote(cadea_datos) for cadea_datos in argumento_MATRIZ.arguments)
        return 0 if executar_comando(apl) == 0 else 1
    finally:
        if Proceso.poll() is None:
            Proceso.terminate()
            try: Proceso.wait(timeout=5)
            except subprocess.TimeoutExpired: Proceso.kill(); Proceso.wait(timeout=5)
        준비선택기.close(); Proceso.stdin.close(); Proceso.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Executar_2())
