#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. óstach 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from Rith_ordú import Ordú


def Rith_2():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 Ainm(예: bailíochtaigh.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class Comhad 또는 class 디렉터리(패키지 Ainm 유지)')
    argóint_ARRAY = 인수해석기.parse_args()
    sonraí = argóint_ARRAY.file.read_bytes()
    if argóint_ARRAY.class_name and argóint_ARRAY.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    Ainm = argóint_ARRAY.class_name + '.class' if argóint_ARRAY.class_name else argóint_ARRAY.file.name
    if len(sonraí) > 16384 or not 1 <= len(Ainm.encode('utf-8')) <= 63 or '\n' in Ainm or '\r' in Ainm:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    catagóir_VALUE = '.elf' if sonraí[:4] == b'\x7fELF' else argóint_ARRAY.file.suffix
    if argóint_ARRAY.linux and catagóir_VALUE != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if catagóir_VALUE not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argóint_ARRAY.arguments) > 7 or any(len(teaghrán_sonraí.encode('utf-8')) > 255 or '\n' in teaghrán_sonraí or '\r' in teaghrán_sonraí for teaghrán_sonraí in argóint_ARRAY.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Roghanna = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argóint_ARRAY.vnc: Roghanna += ['-vnc', argóint_ARRAY.vnc]
    Próiseas = subprocess.Popen(Ordú() + Roghanna, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    roghnóir = selectors.DefaultSelector(); roghnóir.register(Próiseas.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); cuir_deireadh_le_OFFSET = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > cuir_deireadh_le_OFFSET: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in roghnóir.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Próiseas.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def seol(Líne, 확인표시=b'jkoros-native> '):
        Próiseas.stdin.write(Líne.encode('utf-8') + b'\n'); Próiseas.stdin.flush()
        return 수신하기(확인표시)
    def Rith_ordú(Líne):
        출력결과 = seol(Líne); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        comhad_Liosta = []
        for 포함항목 in argóint_ARRAY.include:
            if 포함항목.is_dir():
                comhad_Liosta += [(str(sonraí_suíomh.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', sonraí_suíomh.read_bytes()) for sonraí_suíomh in sorted(포함항목.rglob('*.class'))]
            else:
                comhad_Liosta.append((포함항목.name, 포함항목.read_bytes()))
        comhad_Liosta = [(mír_COUNT, sprioc_sonraí) for mír_COUNT, sprioc_sonraí in comhad_Liosta if mír_COUNT != Ainm] + [(Ainm, sonraí)]
        for uaslódáil_ainm, uaslódáil_sonraí in comhad_Liosta:
            if len(uaslódáil_sonraí) > 16384 or len(uaslódáil_ainm.encode('utf-8')) > 63 or '\n' in uaslódáil_ainm or '\r' in uaslódáil_ainm:
                raise ValueError('추가 파일의 Ainm/Méid 제한 초과: ' + uaslódáil_ainm)
            seol('load ' + shlex.quote(uaslódáil_ainm), b'hex> ')
            for 순번 in range(0, len(uaslódáil_sonraí), 64): seol(uaslódáil_sonraí[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in seol('.'): raise RuntimeError('upload failed: ' + uaslódáil_ainm)
            갈무리자료 = seol('hex ' + shlex.quote(uaslódáil_ainm))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != uaslódáil_sonraí: raise RuntimeError('upload verification failed')
        if catagóir_VALUE == '.java' and Rith_ordú('javac ' + shlex.quote(Ainm)) != 0: return 1
        실행가능파일 = argóint_ARRAY.file.stem + '.elf'
        if catagóir_VALUE == '.c' and Rith_ordú('cc ' + shlex.quote(Ainm) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        clár_f67c8751 = 'java ' + shlex.quote(argóint_ARRAY.class_name or argóint_ARRAY.file.stem) if catagóir_VALUE in ('.java', '.class') else ('python ' if catagóir_VALUE == '.py' else 'run ') + shlex.quote(Ainm)
        if catagóir_VALUE == '.jar': clár_f67c8751 = 'java -jar ' + shlex.quote(Ainm)
        if catagóir_VALUE == '.c': clár_f67c8751 = 'run ' + shlex.quote(실행가능파일)
        if argóint_ARRAY.linux: clár_f67c8751 = 'run --linux ' + shlex.quote(Ainm)
        if argóint_ARRAY.arguments: clár_f67c8751 += ' ' + ' '.join(shlex.quote(teaghrán_sonraí) for teaghrán_sonraí in argóint_ARRAY.arguments)
        return 0 if Rith_ordú(clár_f67c8751) == 0 else 1
    finally:
        if Próiseas.poll() is None:
            Próiseas.terminate()
            try: Próiseas.wait(timeout=5)
            except subprocess.TimeoutExpired: Próiseas.kill(); Próiseas.wait(timeout=5)
        roghnóir.close(); Próiseas.stdin.close(); Próiseas.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Rith_2())
