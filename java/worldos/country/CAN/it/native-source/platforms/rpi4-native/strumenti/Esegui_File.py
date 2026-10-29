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
from Esegui_comando import comando


def avvia():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('arguments', nargs='*')
    parser.add_argument('--class-name', help='패키지가 있는 .class의 전체 Nome(예: convalidare.test_aggregare)')
    parser.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI usare_VALORE')
    parser.add_argument('--vnc', help='예: 127.0.0.1:2')
    parser.add_argument('--include', action='append', type=Path, default=[], help='Aggiunta_voce class file 또는 class 디렉터리(패키지 Nome mantenere_VALORE)')
    argomento_array = parser.parse_args()
    dati = argomento_array.file.read_bytes()
    if argomento_array.class_name and argomento_array.file.suffix != '.class': parser.error('--class-name은 .class 입력에서 사용합니다.')
    Nome = argomento_array.class_name + '.class' if argomento_array.class_name else argomento_array.file.name
    if len(dati) > 16384 or not 1 <= len(Nome.encode('utf-8')) <= 63 or '\n' in Nome or '\r' in Nome:
        parser.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    Valore_categoria = '.elf' if dati[:4] == b'\x7fELF' else argomento_array.file.suffix
    if argomento_array.linux and Valore_categoria != '.elf': parser.error('--linux는 ELF 바이너리에만 사용합니다.')
    if Valore_categoria not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        parser.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argomento_array.arguments) > 7 or any(len(stringa_dati.encode('utf-8')) > 255 or '\n' in stringa_dati or '\r' in stringa_dati for stringa_dati in argomento_array.arguments):
        parser.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Opzioni = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argomento_array.vnc: Opzioni += ['-vnc', argomento_array.vnc]
    Processi = subprocess.Popen(comando() + Opzioni, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selettore = selectors.DefaultSelector(); selettore.register(Processi.stdout, selectors.EVENT_READ)
    def ricevere_documento(marcatore, esecuzione_TIMEOUT=45):
        output = bytearray(); chiudere_SCARTO = time.monotonic() + esecuzione_TIMEOUT
        while marcatore not in output:
            if time.monotonic() > chiudere_SCARTO: raise RuntimeError('UART timeout: ' + output.decode('utf-8', 'replace'))
            for 누름값, _ in selettore.select(0.1):
                blocco_VALORE_652d4b53 = 누름값.fileobj.read(4096)
                if blocco_VALORE_652d4b53: output.extend(blocco_VALORE_652d4b53)
            if b'PANIC:' in output or b'FAIL ' in output: raise RuntimeError(output.decode('utf-8', 'replace'))
            if Processi.poll() is not None: raise RuntimeError('QEMU exited: ' + output.decode('utf-8', 'replace'))
        return bytes(output)
    def inviare(riga_di_ingresso, marcatore=b'jkoros-native> '):
        Processi.stdin.write(riga_di_ingresso.encode('utf-8') + b'\n'); Processi.stdin.flush()
        return ricevere_documento(marcatore)
    def Esegui_comando(riga_di_ingresso):
        output = inviare(riga_di_ingresso); sys.stdout.buffer.write(output); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', output)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        ricevere_documento(b'jkoros-native> ')
        elenco_file = []
        for includere in argomento_array.include:
            if includere.is_dir():
                elenco_file += [(str(dati_funzione.relative_to(includere).with_suffix('')).replace('/', '.') + '.class', dati_funzione.read_bytes()) for dati_funzione in sorted(includere.rglob('*.class'))]
            else:
                elenco_file.append((includere.name, includere.read_bytes()))
        elenco_file = [(articolo_CONTA_NUMERI, meta_dati) for articolo_CONTA_NUMERI, meta_dati in elenco_file if articolo_CONTA_NUMERI != Nome] + [(Nome, dati)]
        for Upload_nome, Upload_dati in elenco_file:
            if len(Upload_dati) > 16384 or len(Upload_nome.encode('utf-8')) > 63 or '\n' in Upload_nome or '\r' in Upload_nome:
                raise ValueError('Aggiunta_voce 파일의 Nome/Dimensione 제한 초과: ' + Upload_nome)
            inviare('load ' + shlex.quote(Upload_nome), b'hex> ')
            for 순번 in range(0, len(Upload_dati), 64): inviare(Upload_dati[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in inviare('.'): raise RuntimeError('upload failed: ' + Upload_nome)
            갈무리자료 = inviare('hex ' + shlex.quote(Upload_nome))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Upload_dati: raise RuntimeError('upload verification failed')
        if Valore_categoria == '.java' and Esegui_comando('javac ' + shlex.quote(Nome)) != 0: return 1
        eseguibile_foto = argomento_array.file.stem + '.elf'
        if Valore_categoria == '.c' and Esegui_comando('cc ' + shlex.quote(Nome) + ' -o ' + shlex.quote(eseguibile_foto)) != 0: return 1
        app = 'java ' + shlex.quote(argomento_array.class_name or argomento_array.file.stem) if Valore_categoria in ('.java', '.class') else ('python ' if Valore_categoria == '.py' else 'run ') + shlex.quote(Nome)
        if Valore_categoria == '.jar': app = 'java -jar ' + shlex.quote(Nome)
        if Valore_categoria == '.c': app = 'run ' + shlex.quote(eseguibile_foto)
        if argomento_array.linux: app = 'run --linux ' + shlex.quote(Nome)
        if argomento_array.arguments: app += ' ' + ' '.join(shlex.quote(stringa_dati) for stringa_dati in argomento_array.arguments)
        return 0 if Esegui_comando(app) == 0 else 1
    finally:
        if Processi.poll() is None:
            Processi.terminate()
            try: Processi.wait(timeout=5)
            except subprocess.TimeoutExpired: Processi.kill(); Processi.wait(timeout=5)
        selettore.close(); Processi.stdin.close(); Processi.stdout.close()


if __name__ == '__main__':
    raise SystemExit(avvia())
