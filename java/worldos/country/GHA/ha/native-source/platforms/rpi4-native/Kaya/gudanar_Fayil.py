#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. sauka 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from gudanar_Umarni import Umarni


def Tafiyar_da():
    tatsar_manhaja = argparse.ArgumentParser(description=__doc__)
    tatsar_manhaja.add_argument('file', type=Path)
    tatsar_manhaja.add_argument('arguments', nargs='*')
    tatsar_manhaja.add_argument('--class-name', help='패키지가 있는 .class의 전체 Suna(예: inganta.꾸러미시험)')
    tatsar_manhaja.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    tatsar_manhaja.add_argument('--vnc', help='예: 127.0.0.1:2')
    tatsar_manhaja.add_argument('--include', action='append', type=Path, default=[], help='추가 class Fayil 또는 class 디렉터리(패키지 Suna 유지)')
    Tubalin_aiki_TSARI = tatsar_manhaja.parse_args()
    Tarin_bayani = Tubalin_aiki_TSARI.file.read_bytes()
    if Tubalin_aiki_TSARI.class_name and Tubalin_aiki_TSARI.file.suffix != '.class': tatsar_manhaja.error('--class-name은 .class 입력에서 사용합니다.')
    Suna = Tubalin_aiki_TSARI.class_name + '.class' if Tubalin_aiki_TSARI.class_name else Tubalin_aiki_TSARI.file.name
    if len(Tarin_bayani) > 16384 or not 1 <= len(Suna.encode('utf-8')) <= 63 or '\n' in Suna or '\r' in Suna:
        tatsar_manhaja.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    ɓangare_Daraja = '.elf' if Tarin_bayani[:4] == b'\x7fELF' else Tubalin_aiki_TSARI.file.suffix
    if Tubalin_aiki_TSARI.linux and ɓangare_Daraja != '.elf': tatsar_manhaja.error('--linux는 ELF 바이너리에만 사용합니다.')
    if ɓangare_Daraja not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        tatsar_manhaja.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(Tubalin_aiki_TSARI.arguments) > 7 or any(len(Zare_Tarin_bayani.encode('utf-8')) > 255 or '\n' in Zare_Tarin_bayani or '\r' in Zare_Tarin_bayani for Zare_Tarin_bayani in Tubalin_aiki_TSARI.arguments):
        tatsar_manhaja.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Zaɓuɓɓuka = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if Tubalin_aiki_TSARI.vnc: Zaɓuɓɓuka += ['-vnc', Tubalin_aiki_TSARI.vnc]
    haryar_aikin_na_ura = subprocess.Popen(Umarni() + Zaɓuɓɓuka, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    mai_zabe = selectors.DefaultSelector(); mai_zabe.register(haryar_aikin_na_ura.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); Ƙarshe_Sassautawa = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > Ƙarshe_Sassautawa: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in mai_zabe.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if haryar_aikin_na_ura.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def Aika(Layi, 확인표시=b'jkoros-native> '):
        haryar_aikin_na_ura.stdin.write(Layi.encode('utf-8') + b'\n'); haryar_aikin_na_ura.stdin.flush()
        return 수신하기(확인표시)
    def gudanar_Umarni(Layi):
        출력결과 = Aika(Layi); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        Fayil_Jeri = []
        for 포함항목 in Tubalin_aiki_TSARI.include:
            if 포함항목.is_dir():
                Fayil_Jeri += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                Fayil_Jeri.append((포함항목.name, 포함항목.read_bytes()))
        Fayil_Jeri = [(개수, Zangon_ƙarshe_Tarin_bayani) for 개수, Zangon_ƙarshe_Tarin_bayani in Fayil_Jeri if 개수 != Suna] + [(Suna, Tarin_bayani)]
        for lodawa_Suna, lodawa_Tarin_bayani in Fayil_Jeri:
            if len(lodawa_Tarin_bayani) > 16384 or len(lodawa_Suna.encode('utf-8')) > 63 or '\n' in lodawa_Suna or '\r' in lodawa_Suna:
                raise ValueError('추가 파일의 Suna/Girma 제한 초과: ' + lodawa_Suna)
            Aika('load ' + shlex.quote(lodawa_Suna), b'hex> ')
            for 순번 in range(0, len(lodawa_Tarin_bayani), 64): Aika(lodawa_Tarin_bayani[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in Aika('.'): raise RuntimeError('upload failed: ' + lodawa_Suna)
            갈무리자료 = Aika('hex ' + shlex.quote(lodawa_Suna))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != lodawa_Tarin_bayani: raise RuntimeError('upload verification failed')
        if ɓangare_Daraja == '.java' and gudanar_Umarni('javac ' + shlex.quote(Suna)) != 0: return 1
        실행가능파일 = Tubalin_aiki_TSARI.file.stem + '.elf'
        if ɓangare_Daraja == '.c' and gudanar_Umarni('cc ' + shlex.quote(Suna) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        Shiri = 'java ' + shlex.quote(Tubalin_aiki_TSARI.class_name or Tubalin_aiki_TSARI.file.stem) if ɓangare_Daraja in ('.java', '.class') else ('python ' if ɓangare_Daraja == '.py' else 'run ') + shlex.quote(Suna)
        if ɓangare_Daraja == '.jar': Shiri = 'java -jar ' + shlex.quote(Suna)
        if ɓangare_Daraja == '.c': Shiri = 'run ' + shlex.quote(실행가능파일)
        if Tubalin_aiki_TSARI.linux: Shiri = 'run --linux ' + shlex.quote(Suna)
        if Tubalin_aiki_TSARI.arguments: Shiri += ' ' + ' '.join(shlex.quote(Zare_Tarin_bayani) for Zare_Tarin_bayani in Tubalin_aiki_TSARI.arguments)
        return 0 if gudanar_Umarni(Shiri) == 0 else 1
    finally:
        if haryar_aikin_na_ura.poll() is None:
            haryar_aikin_na_ura.terminate()
            try: haryar_aikin_na_ura.wait(timeout=5)
            except subprocess.TimeoutExpired: haryar_aikin_na_ura.kill(); haryar_aikin_na_ura.wait(timeout=5)
        mai_zabe.close(); haryar_aikin_na_ura.stdin.close(); haryar_aikin_na_ura.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Tafiyar_da())
