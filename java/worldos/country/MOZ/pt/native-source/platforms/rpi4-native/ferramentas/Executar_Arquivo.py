#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. host 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from Executar_comando import comando


def iniciar():
    analisador = argparse.ArgumentParser(description=__doc__)
    analisador.add_argument('file', type=Path)
    analisador.add_argument('arguments', nargs='*')
    analisador.add_argument('--class-name', help='패키지가 있는 .class의 전체 Nome(예: validar.teste_grupo)')
    analisador.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI uso_VALOR')
    analisador.add_argument('--vnc', help='예: 127.0.0.1:2')
    analisador.add_argument('--include', action='append', type=Path, default=[], help='Acrescentar_entrada class ficheiro 또는 class 디렉터리(패키지 Nome reter_VALOR)')
    argumento_MATRIZ = analisador.parse_args()
    dados = argumento_MATRIZ.file.read_bytes()
    if argumento_MATRIZ.class_name and argumento_MATRIZ.file.suffix != '.class': analisador.error('--class-name은 .class 입력에서 사용합니다.')
    Nome = argumento_MATRIZ.class_name + '.class' if argumento_MATRIZ.class_name else argumento_MATRIZ.file.name
    if len(dados) > 16384 or not 1 <= len(Nome.encode('utf-8')) <= 63 or '\n' in Nome or '\r' in Nome:
        analisador.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    área_VALOR = '.elf' if dados[:4] == b'\x7fELF' else argumento_MATRIZ.file.suffix
    if argumento_MATRIZ.linux and área_VALOR != '.elf': analisador.error('--linux는 ELF 바이너리에만 사용합니다.')
    if área_VALOR not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        analisador.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argumento_MATRIZ.arguments) > 7 or any(len(cadeia_dados.encode('utf-8')) > 255 or '\n' in cadeia_dados or '\r' in cadeia_dados for cadeia_dados in argumento_MATRIZ.arguments):
        analisador.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Opções = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argumento_MATRIZ.vnc: Opções += ['-vnc', argumento_MATRIZ.vnc]
    Processo = subprocess.Popen(comando() + Opções, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    seletor = selectors.DefaultSelector(); seletor.register(Processo.stdout, selectors.EVENT_READ)
    def receber_email(favorito, execução_TEMPOLIMITE=45):
        saída = bytearray(); encerrar_DESLOC = time.monotonic() + execução_TEMPOLIMITE
        while favorito not in saída:
            if time.monotonic() > encerrar_DESLOC: raise RuntimeError('UART timeout: ' + saída.decode('utf-8', 'replace'))
            for 누름값, _ in seletor.select(0.1):
                fragmento_VALOR = 누름값.fileobj.read(4096)
                if fragmento_VALOR: saída.extend(fragmento_VALOR)
            if b'PANIC:' in saída or b'FAIL ' in saída: raise RuntimeError(saída.decode('utf-8', 'replace'))
            if Processo.poll() is not None: raise RuntimeError('QEMU exited: ' + saída.decode('utf-8', 'replace'))
        return bytes(saída)
    def enviar(linha_de_entrada, favorito=b'jkoros-native> '):
        Processo.stdin.write(linha_de_entrada.encode('utf-8') + b'\n'); Processo.stdin.flush()
        return receber_email(favorito)
    def Executar_comando(linha_de_entrada):
        saída = enviar(linha_de_entrada); sys.stdout.buffer.write(saída); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', saída)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        receber_email(b'jkoros-native> ')
        lista_de_arquivos = []
        for incluir in argumento_MATRIZ.include:
            if incluir.is_dir():
                lista_de_arquivos += [(str(dados_cargo.relative_to(incluir).with_suffix('')).replace('/', '.') + '.class', dados_cargo.read_bytes()) for dados_cargo in sorted(incluir.rglob('*.class'))]
            else:
                lista_de_arquivos.append((incluir.name, incluir.read_bytes()))
        lista_de_arquivos = [(item_CONT_NÚM, destino_dados) for item_CONT_NÚM, destino_dados in lista_de_arquivos if item_CONT_NÚM != Nome] + [(Nome, dados)]
        for Upload_nome, Upload_dados in lista_de_arquivos:
            if len(Upload_dados) > 16384 or len(Upload_nome.encode('utf-8')) > 63 or '\n' in Upload_nome or '\r' in Upload_nome:
                raise ValueError('Acrescentar_entrada 파일의 Nome/Tamanho 제한 초과: ' + Upload_nome)
            enviar('load ' + shlex.quote(Upload_nome), b'hex> ')
            for 순번 in range(0, len(Upload_dados), 64): enviar(Upload_dados[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in enviar('.'): raise RuntimeError('upload failed: ' + Upload_nome)
            갈무리자료 = enviar('hex ' + shlex.quote(Upload_nome))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Upload_dados: raise RuntimeError('upload verification failed')
        if área_VALOR == '.java' and Executar_comando('javac ' + shlex.quote(Nome)) != 0: return 1
        executável_foto = argumento_MATRIZ.file.stem + '.elf'
        if área_VALOR == '.c' and Executar_comando('cc ' + shlex.quote(Nome) + ' -o ' + shlex.quote(executável_foto)) != 0: return 1
        app = 'java ' + shlex.quote(argumento_MATRIZ.class_name or argumento_MATRIZ.file.stem) if área_VALOR in ('.java', '.class') else ('python ' if área_VALOR == '.py' else 'run ') + shlex.quote(Nome)
        if área_VALOR == '.jar': app = 'java -jar ' + shlex.quote(Nome)
        if área_VALOR == '.c': app = 'run ' + shlex.quote(executável_foto)
        if argumento_MATRIZ.linux: app = 'run --linux ' + shlex.quote(Nome)
        if argumento_MATRIZ.arguments: app += ' ' + ' '.join(shlex.quote(cadeia_dados) for cadeia_dados in argumento_MATRIZ.arguments)
        return 0 if Executar_comando(app) == 0 else 1
    finally:
        if Processo.poll() is None:
            Processo.terminate()
            try: Processo.wait(timeout=5)
            except subprocess.TimeoutExpired: Processo.kill(); Processo.wait(timeout=5)
        seletor.close(); Processo.stdin.close(); Processo.stdout.close()


if __name__ == '__main__':
    raise SystemExit(iniciar())
