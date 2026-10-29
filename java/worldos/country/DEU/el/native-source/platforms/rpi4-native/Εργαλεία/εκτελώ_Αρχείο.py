#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. φιλοξενώ 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from εκτελώ_εντολή import Εντολή


def Εκτέλεση_2():
    ανάλυση = argparse.ArgumentParser(description=__doc__)
    ανάλυση.add_argument('file', type=Path)
    ανάλυση.add_argument('arguments', nargs='*')
    ανάλυση.add_argument('--class-name', help='패키지가 있는 .class의 전체 Όνομα(예: επικυρώνω.δοκιμή_πακέτο)')
    ανάλυση.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI χρήση_τιμή')
    ανάλυση.add_argument('--vnc', help='예: 127.0.0.1:2')
    ανάλυση.add_argument('--include', action='append', type=Path, default=[], help='προσαρτώ_καταχώρηση class Αρχείο 또는 class 디렉터리(패키지 Όνομα 유지)')
    όρισμα_πίνακας = ανάλυση.parse_args()
    δεδομένα = όρισμα_πίνακας.file.read_bytes()
    if όρισμα_πίνακας.class_name and όρισμα_πίνακας.file.suffix != '.class': ανάλυση.error('--class-name은 .class 입력에서 사용합니다.')
    Όνομα = όρισμα_πίνακας.class_name + '.class' if όρισμα_πίνακας.class_name else όρισμα_πίνακας.file.name
    if len(δεδομένα) > 16384 or not 1 <= len(Όνομα.encode('utf-8')) <= 63 or '\n' in Όνομα or '\r' in Όνομα:
        ανάλυση.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    περιοχή_τιμή = '.elf' if δεδομένα[:4] == b'\x7fELF' else όρισμα_πίνακας.file.suffix
    if όρισμα_πίνακας.linux and περιοχή_τιμή != '.elf': ανάλυση.error('--linux는 ELF 바이너리에만 사용합니다.')
    if περιοχή_τιμή not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        ανάλυση.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(όρισμα_πίνακας.arguments) > 7 or any(len(συμβολοσειρά_δεδομένα.encode('utf-8')) > 255 or '\n' in συμβολοσειρά_δεδομένα or '\r' in συμβολοσειρά_δεδομένα for συμβολοσειρά_δεδομένα in όρισμα_πίνακας.arguments):
        ανάλυση.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Επιλογές = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if όρισμα_πίνακας.vnc: Επιλογές += ['-vnc', όρισμα_πίνακας.vnc]
    Διεργασία = subprocess.Popen(Εντολή() + Επιλογές, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    επιλογέας = selectors.DefaultSelector(); επιλογέας.register(Διεργασία.stdout, selectors.EVENT_READ)
    def λαμβάνω_μήνυμα(δείκτης_8b722c5f, εκτέλεση_ΤΕΛΟΣ_ΧΡΟΝΟΥ=45):
        출력결과 = bytearray(); Τελική_οντότητα_Υπέρθεση = time.monotonic() + εκτέλεση_ΤΕΛΟΣ_ΧΡΟΝΟΥ
        while δείκτης_8b722c5f not in 출력결과:
            if time.monotonic() > Τελική_οντότητα_Υπέρθεση: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in επιλογέας.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Διεργασία.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def στέλνω(Γραμμή, δείκτης_8b722c5f=b'jkoros-native> '):
        Διεργασία.stdin.write(Γραμμή.encode('utf-8') + b'\n'); Διεργασία.stdin.flush()
        return λαμβάνω_μήνυμα(δείκτης_8b722c5f)
    def εκτελώ_εντολή(Γραμμή):
        출력결과 = στέλνω(Γραμμή); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        λαμβάνω_μήνυμα(b'jkoros-native> ')
        λίστα_αρχείων = []
        for περιλαμβάνω in όρισμα_πίνακας.include:
            if περιλαμβάνω.is_dir():
                λίστα_αρχείων += [(str(δεδομένα_θέση.relative_to(περιλαμβάνω).with_suffix('')).replace('/', '.') + '.class', δεδομένα_θέση.read_bytes()) for δεδομένα_θέση in sorted(περιλαμβάνω.rglob('*.class'))]
            else:
                λίστα_αρχείων.append((περιλαμβάνω.name, περιλαμβάνω.read_bytes()))
        λίστα_αρχείων = [(개수, προορισμός_δεδομένα) for 개수, προορισμός_δεδομένα in λίστα_αρχείων if 개수 != Όνομα] + [(Όνομα, δεδομένα)]
        for ανεβάζω_όνομα, ανεβάζω_δεδομένα in λίστα_αρχείων:
            if len(ανεβάζω_δεδομένα) > 16384 or len(ανεβάζω_όνομα.encode('utf-8')) > 63 or '\n' in ανεβάζω_όνομα or '\r' in ανεβάζω_όνομα:
                raise ValueError('προσαρτώ_καταχώρηση 파일의 Όνομα/Μέγεθος 제한 초과: ' + ανεβάζω_όνομα)
            στέλνω('load ' + shlex.quote(ανεβάζω_όνομα), b'hex> ')
            for 순번 in range(0, len(ανεβάζω_δεδομένα), 64): στέλνω(ανεβάζω_δεδομένα[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in στέλνω('.'): raise RuntimeError('upload failed: ' + ανεβάζω_όνομα)
            갈무리자료 = στέλνω('hex ' + shlex.quote(ανεβάζω_όνομα))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != ανεβάζω_δεδομένα: raise RuntimeError('upload verification failed')
        if περιοχή_τιμή == '.java' and εκτελώ_εντολή('javac ' + shlex.quote(Όνομα)) != 0: return 1
        εκτελέσιμο_εικόνα = όρισμα_πίνακας.file.stem + '.elf'
        if περιοχή_τιμή == '.c' and εκτελώ_εντολή('cc ' + shlex.quote(Όνομα) + ' -o ' + shlex.quote(εκτελέσιμο_εικόνα)) != 0: return 1
        εφαρμογή = 'java ' + shlex.quote(όρισμα_πίνακας.class_name or όρισμα_πίνακας.file.stem) if περιοχή_τιμή in ('.java', '.class') else ('python ' if περιοχή_τιμή == '.py' else 'run ') + shlex.quote(Όνομα)
        if περιοχή_τιμή == '.jar': εφαρμογή = 'java -jar ' + shlex.quote(Όνομα)
        if περιοχή_τιμή == '.c': εφαρμογή = 'run ' + shlex.quote(εκτελέσιμο_εικόνα)
        if όρισμα_πίνακας.linux: εφαρμογή = 'run --linux ' + shlex.quote(Όνομα)
        if όρισμα_πίνακας.arguments: εφαρμογή += ' ' + ' '.join(shlex.quote(συμβολοσειρά_δεδομένα) for συμβολοσειρά_δεδομένα in όρισμα_πίνακας.arguments)
        return 0 if εκτελώ_εντολή(εφαρμογή) == 0 else 1
    finally:
        if Διεργασία.poll() is None:
            Διεργασία.terminate()
            try: Διεργασία.wait(timeout=5)
            except subprocess.TimeoutExpired: Διεργασία.kill(); Διεργασία.wait(timeout=5)
        επιλογέας.close(); Διεργασία.stdin.close(); Διεργασία.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Εκτέλεση_2())
