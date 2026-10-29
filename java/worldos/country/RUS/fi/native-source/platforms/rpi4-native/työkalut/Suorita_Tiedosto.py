#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. isäntä 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from Suorita_komento import komento


def Suorita_2():
    jäsennin = argparse.ArgumentParser(description=__doc__)
    jäsennin.add_argument('file', type=Path)
    jäsennin.add_argument('arguments', nargs='*')
    jäsennin.add_argument('--class-name', help='패키지가 있는 .class의 전체 Nimi(예: vahvista.testi_nippu)')
    jäsennin.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI käyttö_ARVO')
    jäsennin.add_argument('--vnc', help='예: 127.0.0.1:2')
    jäsennin.add_argument('--include', action='append', type=Path, default=[], help='liitä_merkintä class tiedoston_nimi 또는 class 디렉터리(패키지 Nimi 유지)')
    argumentti_MATRIISI = jäsennin.parse_args()
    data = argumentti_MATRIISI.file.read_bytes()
    if argumentti_MATRIISI.class_name and argumentti_MATRIISI.file.suffix != '.class': jäsennin.error('--class-name은 .class 입력에서 사용합니다.')
    Nimi = argumentti_MATRIISI.class_name + '.class' if argumentti_MATRIISI.class_name else argumentti_MATRIISI.file.name
    if len(data) > 16384 or not 1 <= len(Nimi.encode('utf-8')) <= 63 or '\n' in Nimi or '\r' in Nimi:
        jäsennin.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    alue_ARVO = '.elf' if data[:4] == b'\x7fELF' else argumentti_MATRIISI.file.suffix
    if argumentti_MATRIISI.linux and alue_ARVO != '.elf': jäsennin.error('--linux는 ELF 바이너리에만 사용합니다.')
    if alue_ARVO not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        jäsennin.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argumentti_MATRIISI.arguments) > 7 or any(len(merkkijono_data.encode('utf-8')) > 255 or '\n' in merkkijono_data or '\r' in merkkijono_data for merkkijono_data in argumentti_MATRIISI.arguments):
        jäsennin.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Asetukset_7f769d16 = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argumentti_MATRIISI.vnc: Asetukset_7f769d16 += ['-vnc', argumentti_MATRIISI.vnc]
    Prosessi = subprocess.Popen(komento() + Asetukset_7f769d16, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    valitsin = selectors.DefaultSelector(); valitsin.register(Prosessi.stdout, selectors.EVENT_READ)
    def saada_sanoma(merkintä, suoritus_AIKAKATKAISU=45):
        tulos = bytearray(); lopettaa_puhelu_SIIRTYMÄ = time.monotonic() + suoritus_AIKAKATKAISU
        while merkintä not in tulos:
            if time.monotonic() > lopettaa_puhelu_SIIRTYMÄ: raise RuntimeError('UART timeout: ' + tulos.decode('utf-8', 'replace'))
            for 누름값, _ in valitsin.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: tulos.extend(조각)
            if b'PANIC:' in tulos or b'FAIL ' in tulos: raise RuntimeError(tulos.decode('utf-8', 'replace'))
            if Prosessi.poll() is not None: raise RuntimeError('QEMU exited: ' + tulos.decode('utf-8', 'replace'))
        return bytes(tulos)
    def lähettää(syöterivi, merkintä=b'jkoros-native> '):
        Prosessi.stdin.write(syöterivi.encode('utf-8') + b'\n'); Prosessi.stdin.flush()
        return saada_sanoma(merkintä)
    def Suorita_komento(syöterivi):
        tulos = lähettää(syöterivi); sys.stdout.buffer.write(tulos); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', tulos)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        saada_sanoma(b'jkoros-native> ')
        tiedostoluettelo = []
        for sisältää in argumentti_MATRIISI.include:
            if sisältää.is_dir():
                tiedostoluettelo += [(str(data_toimi.relative_to(sisältää).with_suffix('')).replace('/', '.') + '.class', data_toimi.read_bytes()) for data_toimi in sorted(sisältää.rglob('*.class'))]
            else:
                tiedostoluettelo.append((sisältää.name, sisältää.read_bytes()))
        tiedostoluettelo = [(kohde_LASKE, kohde_data) for kohde_LASKE, kohde_data in tiedostoluettelo if kohde_LASKE != Nimi] + [(Nimi, data)]
        for Upload_nimi, Upload_data in tiedostoluettelo:
            if len(Upload_data) > 16384 or len(Upload_nimi.encode('utf-8')) > 63 or '\n' in Upload_nimi or '\r' in Upload_nimi:
                raise ValueError('liitä_merkintä 파일의 Nimi/Koko 제한 초과: ' + Upload_nimi)
            lähettää('load ' + shlex.quote(Upload_nimi), b'hex> ')
            for 순번 in range(0, len(Upload_data), 64): lähettää(Upload_data[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in lähettää('.'): raise RuntimeError('upload failed: ' + Upload_nimi)
            갈무리자료 = lähettää('hex ' + shlex.quote(Upload_nimi))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Upload_data: raise RuntimeError('upload verification failed')
        if alue_ARVO == '.java' and Suorita_komento('javac ' + shlex.quote(Nimi)) != 0: return 1
        suoritettava_tiedosto_KUVA = argumentti_MATRIISI.file.stem + '.elf'
        if alue_ARVO == '.c' and Suorita_komento('cc ' + shlex.quote(Nimi) + ' -o ' + shlex.quote(suoritettava_tiedosto_KUVA)) != 0: return 1
        ohjelma = 'java ' + shlex.quote(argumentti_MATRIISI.class_name or argumentti_MATRIISI.file.stem) if alue_ARVO in ('.java', '.class') else ('python ' if alue_ARVO == '.py' else 'run ') + shlex.quote(Nimi)
        if alue_ARVO == '.jar': ohjelma = 'java -jar ' + shlex.quote(Nimi)
        if alue_ARVO == '.c': ohjelma = 'run ' + shlex.quote(suoritettava_tiedosto_KUVA)
        if argumentti_MATRIISI.linux: ohjelma = 'run --linux ' + shlex.quote(Nimi)
        if argumentti_MATRIISI.arguments: ohjelma += ' ' + ' '.join(shlex.quote(merkkijono_data) for merkkijono_data in argumentti_MATRIISI.arguments)
        return 0 if Suorita_komento(ohjelma) == 0 else 1
    finally:
        if Prosessi.poll() is None:
            Prosessi.terminate()
            try: Prosessi.wait(timeout=5)
            except subprocess.TimeoutExpired: Prosessi.kill(); Prosessi.wait(timeout=5)
        valitsin.close(); Prosessi.stdin.close(); Prosessi.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Suorita_2())
