#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. Wirtssystem 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from befehlAusführen import befehl


def ausführenVorgang():
    strukturanalysierer = argparse.ArgumentParser(description=__doc__)
    strukturanalysierer.add_argument('file', type=Path)
    strukturanalysierer.add_argument('arguments', nargs='*')
    strukturanalysierer.add_argument('--class-name', help='패키지가 있는 .class의 전체 Name(예: validieren.bündelPrüfung)')
    strukturanalysierer.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 aufrufen ABI benutzenWert')
    strukturanalysierer.add_argument('--vnc', help='예: 127.0.0.1:2')
    strukturanalysierer.add_argument('--include', action='append', type=Path, default=[], help='eintragAnhängen class Datei 또는 class 디렉터리(패키지 Name wertBeibehalten)')
    argumentDatenfeld = strukturanalysierer.parse_args()
    Daten = argumentDatenfeld.file.read_bytes()
    if argumentDatenfeld.class_name and argumentDatenfeld.file.suffix != '.class': strukturanalysierer.error('--class-name은 .class 입력에서 사용합니다.')
    Name = argumentDatenfeld.class_name + '.class' if argumentDatenfeld.class_name else argumentDatenfeld.file.name
    if len(Daten) > 16384 or not 1 <= len(Name.encode('utf-8')) <= 63 or '\n' in Name or '\r' in Name:
        strukturanalysierer.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    kategorieWert = '.elf' if Daten[:4] == b'\x7fELF' else argumentDatenfeld.file.suffix
    if argumentDatenfeld.linux and kategorieWert != '.elf': strukturanalysierer.error('--linux는 ELF 바이너리에만 사용합니다.')
    if kategorieWert not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        strukturanalysierer.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argumentDatenfeld.arguments) > 7 or any(len(zeichenketteDaten.encode('utf-8')) > 255 or '\n' in zeichenketteDaten or '\r' in zeichenketteDaten for zeichenketteDaten in argumentDatenfeld.arguments):
        strukturanalysierer.error('인수는 höchstwertWert 7개, 각각 UTF-8 255바이트 이하입니다.')
    wahlmöglichkeiten = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argumentDatenfeld.vnc: wahlmöglichkeiten += ['-vnc', argumentDatenfeld.vnc]
    prozess = subprocess.Popen(befehl() + wahlmöglichkeiten, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    auswähler = selectors.DefaultSelector(); auswähler.register(prozess.stdout, selectors.EVENT_READ)
    def nachrichtEmpfangen(markierung, ausführungZeitüberschreitung=45):
        ausgabe = bytearray(); endeVersatzwert = time.monotonic() + ausführungZeitüberschreitung
        while markierung not in ausgabe:
            if time.monotonic() > endeVersatzwert: raise RuntimeError('UART timeout: ' + ausgabe.decode('utf-8', 'replace'))
            for gedrücktWert, _ in auswähler.select(0.1):
                fragmentWert = gedrücktWert.fileobj.read(4096)
                if fragmentWert: ausgabe.extend(fragmentWert)
            if b'PANIC:' in ausgabe or b'FAIL ' in ausgabe: raise RuntimeError(ausgabe.decode('utf-8', 'replace'))
            if prozess.poll() is not None: raise RuntimeError('QEMU exited: ' + ausgabe.decode('utf-8', 'replace'))
        return bytes(ausgabe)
    def senden(zeile, markierung=b'jkoros-native> '):
        prozess.stdin.write(zeile.encode('utf-8') + b'\n'); prozess.stdin.flush()
        return nachrichtEmpfangen(markierung)
    def befehlAusführen(zeile):
        ausgabe = senden(zeile); sys.stdout.buffer.write(ausgabe); sys.stdout.buffer.flush()
        istGleich = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', ausgabe)
        if not istGleich: raise RuntimeError('guest did not report exit status')
        return int(istGleich.group(1))
    try:
        nachrichtEmpfangen(b'jkoros-native> ')
        dateiListe = []
        for einbinden in argumentDatenfeld.include:
            if einbinden.is_dir():
                dateiListe += [(str(datenPosition.relative_to(einbinden).with_suffix('')).replace('/', '.') + '.class', datenPosition.read_bytes()) for datenPosition in sorted(einbinden.rglob('*.class'))]
            else:
                dateiListe.append((einbinden.name, einbinden.read_bytes()))
        dateiListe = [(elementeintragAnzahl, zielDaten) for elementeintragAnzahl, zielDaten in dateiListe if elementeintragAnzahl != Name] + [(Name, Daten)]
        for hochladenName, hochladenDaten in dateiListe:
            if len(hochladenDaten) > 16384 or len(hochladenName.encode('utf-8')) > 63 or '\n' in hochladenName or '\r' in hochladenName:
                raise ValueError('eintragAnhängen 파일의 Name/größe grenzwertWert 초과: ' + hochladenName)
            senden('load ' + shlex.quote(hochladenName), b'hex> ')
            for ordnungszahlIndex in range(0, len(hochladenDaten), 64): senden(hochladenDaten[ordnungszahlIndex:ordnungszahlIndex+64].hex(), b'hex> ')
            if b'LOADED' not in senden('.'): raise RuntimeError('upload failed: ' + hochladenName)
            ausgelesen = senden('hex ' + shlex.quote(hochladenName))
            istGleich = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', ausgelesen, re.S)
            if not istGleich or bytes.fromhex(''.join(istGleich.group(2).decode().split())) != hochladenDaten: raise RuntimeError('upload verification failed')
        if kategorieWert == '.java' and befehlAusführen('javac ' + shlex.quote(Name)) != 0: return 1
        ausführdateiAbbild = argumentDatenfeld.file.stem + '.elf'
        if kategorieWert == '.c' and befehlAusführen('cc ' + shlex.quote(Name) + ' -o ' + shlex.quote(ausführdateiAbbild)) != 0: return 1
        programm = 'java ' + shlex.quote(argumentDatenfeld.class_name or argumentDatenfeld.file.stem) if kategorieWert in ('.java', '.class') else ('python ' if kategorieWert == '.py' else 'run ') + shlex.quote(Name)
        if kategorieWert == '.jar': programm = 'java -jar ' + shlex.quote(Name)
        if kategorieWert == '.c': programm = 'run ' + shlex.quote(ausführdateiAbbild)
        if argumentDatenfeld.linux: programm = 'run --linux ' + shlex.quote(Name)
        if argumentDatenfeld.arguments: programm += ' ' + ' '.join(shlex.quote(zeichenketteDaten) for zeichenketteDaten in argumentDatenfeld.arguments)
        return 0 if befehlAusführen(programm) == 0 else 1
    finally:
        if prozess.poll() is None:
            prozess.terminate()
            try: prozess.wait(timeout=5)
            except subprocess.TimeoutExpired: prozess.kill(); prozess.wait(timeout=5)
        auswähler.close(); prozess.stdin.close(); prozess.stdout.close()


if __name__ == '__main__':
    raise SystemExit(ausführenVorgang())
