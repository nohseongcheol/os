#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. gazda 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from végrehajt_parancs import Parancs


def Futtatás():
    elemző = argparse.ArgumentParser(description=__doc__)
    elemző.add_argument('file', type=Path)
    elemző.add_argument('arguments', nargs='*')
    elemző.add_argument('--class-name', help='패키지가 있는 .class의 전체 Név(예: ellenőriz.teszt_köteg)')
    elemző.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI használ_ÉRTÉK')
    elemző.add_argument('--vnc', help='예: 127.0.0.1:2')
    elemző.add_argument('--include', action='append', type=Path, default=[], help='hozzáfűz_bejegyzés class Fájl 또는 class 디렉터리(패키지 Név 유지)')
    argumentum_TÖMB = elemző.parse_args()
    adat = argumentum_TÖMB.file.read_bytes()
    if argumentum_TÖMB.class_name and argumentum_TÖMB.file.suffix != '.class': elemző.error('--class-name은 .class 입력에서 사용합니다.')
    Név = argumentum_TÖMB.class_name + '.class' if argumentum_TÖMB.class_name else argumentum_TÖMB.file.name
    if len(adat) > 16384 or not 1 <= len(Név.encode('utf-8')) <= 63 or '\n' in Név or '\r' in Név:
        elemző.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    terület_ÉRTÉK = '.elf' if adat[:4] == b'\x7fELF' else argumentum_TÖMB.file.suffix
    if argumentum_TÖMB.linux and terület_ÉRTÉK != '.elf': elemző.error('--linux는 ELF 바이너리에만 사용합니다.')
    if terület_ÉRTÉK not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        elemző.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argumentum_TÖMB.arguments) > 7 or any(len(sztring_adat.encode('utf-8')) > 255 or '\n' in sztring_adat or '\r' in sztring_adat for sztring_adat in argumentum_TÖMB.arguments):
        elemző.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Beállítások_7f769d16 = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argumentum_TÖMB.vnc: Beállítások_7f769d16 += ['-vnc', argumentum_TÖMB.vnc]
    Folyamat = subprocess.Popen(Parancs() + Beállítások_7f769d16, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    szelektor = selectors.DefaultSelector(); szelektor.register(Folyamat.stdout, selectors.EVENT_READ)
    def fogad_e_mail(jelölő, végrehajtás_IDŐTÚLLÉPÉS=45):
        kimenet = bytearray(); megszüntet_Ofszet = time.monotonic() + végrehajtás_IDŐTÚLLÉPÉS
        while jelölő not in kimenet:
            if time.monotonic() > megszüntet_Ofszet: raise RuntimeError('UART timeout: ' + kimenet.decode('utf-8', 'replace'))
            for 누름값, _ in szelektor.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: kimenet.extend(조각)
            if b'PANIC:' in kimenet or b'FAIL ' in kimenet: raise RuntimeError(kimenet.decode('utf-8', 'replace'))
            if Folyamat.poll() is not None: raise RuntimeError('QEMU exited: ' + kimenet.decode('utf-8', 'replace'))
        return bytes(kimenet)
    def küld(Vonal, jelölő=b'jkoros-native> '):
        Folyamat.stdin.write(Vonal.encode('utf-8') + b'\n'); Folyamat.stdin.flush()
        return fogad_e_mail(jelölő)
    def végrehajt_parancs(Vonal):
        kimenet = küld(Vonal); sys.stdout.buffer.write(kimenet); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', kimenet)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        fogad_e_mail(b'jkoros-native> ')
        fájllista = []
        for tartalmaz in argumentum_TÖMB.include:
            if tartalmaz.is_dir():
                fájllista += [(str(adat_pozíció.relative_to(tartalmaz).with_suffix('')).replace('/', '.') + '.class', adat_pozíció.read_bytes()) for adat_pozíció in sorted(tartalmaz.rglob('*.class'))]
            else:
                fájllista.append((tartalmaz.name, tartalmaz.read_bytes()))
        fájllista = [(cikk_DARAB, cél_adat) for cikk_DARAB, cél_adat in fájllista if cikk_DARAB != Név] + [(Név, adat)]
        for feltölt_név, feltölt_adat in fájllista:
            if len(feltölt_adat) > 16384 or len(feltölt_név.encode('utf-8')) > 63 or '\n' in feltölt_név or '\r' in feltölt_név:
                raise ValueError('hozzáfűz_bejegyzés 파일의 Név/Méret 제한 초과: ' + feltölt_név)
            küld('load ' + shlex.quote(feltölt_név), b'hex> ')
            for 순번 in range(0, len(feltölt_adat), 64): küld(feltölt_adat[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in küld('.'): raise RuntimeError('upload failed: ' + feltölt_név)
            갈무리자료 = küld('hex ' + shlex.quote(feltölt_név))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != feltölt_adat: raise RuntimeError('upload verification failed')
        if terület_ÉRTÉK == '.java' and végrehajt_parancs('javac ' + shlex.quote(Név)) != 0: return 1
        végrehajtható_KÉP = argumentum_TÖMB.file.stem + '.elf'
        if terület_ÉRTÉK == '.c' and végrehajt_parancs('cc ' + shlex.quote(Név) + ' -o ' + shlex.quote(végrehajtható_KÉP)) != 0: return 1
        app = 'java ' + shlex.quote(argumentum_TÖMB.class_name or argumentum_TÖMB.file.stem) if terület_ÉRTÉK in ('.java', '.class') else ('python ' if terület_ÉRTÉK == '.py' else 'run ') + shlex.quote(Név)
        if terület_ÉRTÉK == '.jar': app = 'java -jar ' + shlex.quote(Név)
        if terület_ÉRTÉK == '.c': app = 'run ' + shlex.quote(végrehajtható_KÉP)
        if argumentum_TÖMB.linux: app = 'run --linux ' + shlex.quote(Név)
        if argumentum_TÖMB.arguments: app += ' ' + ' '.join(shlex.quote(sztring_adat) for sztring_adat in argumentum_TÖMB.arguments)
        return 0 if végrehajt_parancs(app) == 0 else 1
    finally:
        if Folyamat.poll() is None:
            Folyamat.terminate()
            try: Folyamat.wait(timeout=5)
            except subprocess.TimeoutExpired: Folyamat.kill(); Folyamat.wait(timeout=5)
        szelektor.close(); Folyamat.stdin.close(); Folyamat.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Futtatás())
