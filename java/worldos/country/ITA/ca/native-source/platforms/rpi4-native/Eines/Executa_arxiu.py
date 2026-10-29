#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. allotjar 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from Executa_ordre import Ordre


def Executa_2():
    analitzador = argparse.ArgumentParser(description=__doc__)
    analitzador.add_argument('file', type=Path)
    analitzador.add_argument('arguments', nargs='*')
    analitzador.add_argument('--class-name', help='패키지가 있는 .class의 전체 Nom(예: validar.꾸러미시험)')
    analitzador.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI ús_VALOR')
    analitzador.add_argument('--vnc', help='예: 127.0.0.1:2')
    analitzador.add_argument('--include', action='append', type=Path, default=[], help='Annexa_introducció class Fitxer 또는 class 디렉터리(패키지 Nom 유지)')
    arg_MATRIU = analitzador.parse_args()
    dades = arg_MATRIU.file.read_bytes()
    if arg_MATRIU.class_name and arg_MATRIU.file.suffix != '.class': analitzador.error('--class-name은 .class 입력에서 사용합니다.')
    Nom = arg_MATRIU.class_name + '.class' if arg_MATRIU.class_name else arg_MATRIU.file.name
    if len(dades) > 16384 or not 1 <= len(Nom.encode('utf-8')) <= 63 or '\n' in Nom or '\r' in Nom:
        analitzador.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    Categoria_VALOR = '.elf' if dades[:4] == b'\x7fELF' else arg_MATRIU.file.suffix
    if arg_MATRIU.linux and Categoria_VALOR != '.elf': analitzador.error('--linux는 ELF 바이너리에만 사용합니다.')
    if Categoria_VALOR not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        analitzador.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(arg_MATRIU.arguments) > 7 or any(len(cadena_dades.encode('utf-8')) > 255 or '\n' in cadena_dades or '\r' in cadena_dades for cadena_dades in arg_MATRIU.arguments):
        analitzador.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Opcions = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if arg_MATRIU.vnc: Opcions += ['-vnc', arg_MATRIU.vnc]
    Procés = subprocess.Popen(Ordre() + Opcions, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    준비선택기 = selectors.DefaultSelector(); 준비선택기.register(Procés.stdout, selectors.EVENT_READ)
    def rebre_correu(확인표시, 시간제한=45):
        출력결과 = bytearray(); finalitzar_DESPLAÇAMENT = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > finalitzar_DESPLAÇAMENT: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in 준비선택기.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Procés.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def enviar(línia, 확인표시=b'jkoros-native> '):
        Procés.stdin.write(línia.encode('utf-8') + b'\n'); Procés.stdin.flush()
        return rebre_correu(확인표시)
    def Executa_ordre(línia):
        출력결과 = enviar(línia); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        rebre_correu(b'jkoros-native> ')
        arxiu_Llista = []
        for incloure in arg_MATRIU.include:
            if incloure.is_dir():
                arxiu_Llista += [(str(dades_càrrec.relative_to(incloure).with_suffix('')).replace('/', '.') + '.class', dades_càrrec.read_bytes()) for dades_càrrec in sorted(incloure.rglob('*.class'))]
            else:
                arxiu_Llista.append((incloure.name, incloure.read_bytes()))
        arxiu_Llista = [(element_COMPT, destinació_dades) for element_COMPT, destinació_dades in arxiu_Llista if element_COMPT != Nom] + [(Nom, dades)]
        for pujar_nom, pujar_dades in arxiu_Llista:
            if len(pujar_dades) > 16384 or len(pujar_nom.encode('utf-8')) > 63 or '\n' in pujar_nom or '\r' in pujar_nom:
                raise ValueError('Annexa_introducció 파일의 Nom/Mida 제한 초과: ' + pujar_nom)
            enviar('load ' + shlex.quote(pujar_nom), b'hex> ')
            for 순번 in range(0, len(pujar_dades), 64): enviar(pujar_dades[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in enviar('.'): raise RuntimeError('upload failed: ' + pujar_nom)
            갈무리자료 = enviar('hex ' + shlex.quote(pujar_nom))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != pujar_dades: raise RuntimeError('upload verification failed')
        if Categoria_VALOR == '.java' and Executa_ordre('javac ' + shlex.quote(Nom)) != 0: return 1
        실행가능파일 = arg_MATRIU.file.stem + '.elf'
        if Categoria_VALOR == '.c' and Executa_ordre('cc ' + shlex.quote(Nom) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        programa = 'java ' + shlex.quote(arg_MATRIU.class_name or arg_MATRIU.file.stem) if Categoria_VALOR in ('.java', '.class') else ('python ' if Categoria_VALOR == '.py' else 'run ') + shlex.quote(Nom)
        if Categoria_VALOR == '.jar': programa = 'java -jar ' + shlex.quote(Nom)
        if Categoria_VALOR == '.c': programa = 'run ' + shlex.quote(실행가능파일)
        if arg_MATRIU.linux: programa = 'run --linux ' + shlex.quote(Nom)
        if arg_MATRIU.arguments: programa += ' ' + ' '.join(shlex.quote(cadena_dades) for cadena_dades in arg_MATRIU.arguments)
        return 0 if Executa_ordre(programa) == 0 else 1
    finally:
        if Procés.poll() is None:
            Procés.terminate()
            try: Procés.wait(timeout=5)
            except subprocess.TimeoutExpired: Procés.kill(); Procés.wait(timeout=5)
        준비선택기.close(); Procés.stdin.close(); Procés.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Executa_2())
