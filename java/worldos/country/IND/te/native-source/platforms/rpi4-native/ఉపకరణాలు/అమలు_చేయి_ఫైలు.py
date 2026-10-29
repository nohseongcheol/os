#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. హోస్ట్ 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from అమలు_చేయి_ఆదేశం import ఆదేశము


def నడుపుము():
    పార్సర్ = argparse.ArgumentParser(description=__doc__)
    పార్సర్.add_argument('file', type=Path)
    పార్సర్.add_argument('arguments', nargs='*')
    పార్సర్.add_argument('--class-name', help='패키지가 있는 .class의 전체 పేరు(예: నిర్థారీకరించు.꾸러미시험)')
    పార్సర్.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    పార్సర్.add_argument('--vnc', help='예: 127.0.0.1:2')
    పార్సర్.add_argument('--include', action='append', type=Path, default=[], help='추가 class దస్త్రం 또는 class 디렉터리(패키지 పేరు 유지)')
    కారకం_శ్రేణి = పార్సర్.parse_args()
    డేటా = కారకం_శ్రేణి.file.read_bytes()
    if కారకం_శ్రేణి.class_name and కారకం_శ్రేణి.file.suffix != '.class': పార్సర్.error('--class-name은 .class 입력에서 사용합니다.')
    పేరు = కారకం_శ్రేణి.class_name + '.class' if కారకం_శ్రేణి.class_name else కారకం_శ్రేణి.file.name
    if len(డేటా) > 16384 or not 1 <= len(పేరు.encode('utf-8')) <= 63 or '\n' in పేరు or '\r' in పేరు:
        పార్సర్.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    వర్గం_మూల్యం = '.elf' if డేటా[:4] == b'\x7fELF' else కారకం_శ్రేణి.file.suffix
    if కారకం_శ్రేణి.linux and వర్గం_మూల్యం != '.elf': పార్సర్.error('--linux는 ELF 바이너리에만 사용합니다.')
    if వర్గం_మూల్యం not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        పార్సర్.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(కారకం_శ్రేణి.arguments) > 7 or any(len(అక్షరసరం_డేటా.encode('utf-8')) > 255 or '\n' in అక్షరసరం_డేటా or '\r' in అక్షరసరం_డేటా for అక్షరసరం_డేటా in కారకం_శ్రేణి.arguments):
        పార్సర్.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    ఐచ్ఛికాలు = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if కారకం_శ్రేణి.vnc: ఐచ్ఛికాలు += ['-vnc', కారకం_శ్రేణి.vnc]
    క్రమణం = subprocess.Popen(ఆదేశము() + ఐచ్ఛికాలు, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    సెలక్టర్ = selectors.DefaultSelector(); సెలక్టర్.register(క్రమణం.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); ముగించు_ఆఫ్_సెట్ = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > ముగించు_ఆఫ్_సెట్: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in సెలక్టర్.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if క్రమణం.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def పంపు(పంక్తి, 확인표시=b'jkoros-native> '):
        క్రమణం.stdin.write(పంక్తి.encode('utf-8') + b'\n'); క్రమణం.stdin.flush()
        return 수신하기(확인표시)
    def అమలు_చేయి_ఆదేశం(పంక్తి):
        출력결과 = పంపు(పంక్తి); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        ఫైలు_జాబితా = []
        for 포함항목 in కారకం_శ్రేణి.include:
            if 포함항목.is_dir():
                ఫైలు_జాబితా += [(str(డేటా_స్థాయి.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', డేటా_స్థాయి.read_bytes()) for డేటా_స్థాయి in sorted(포함항목.rglob('*.class'))]
            else:
                ఫైలు_జాబితా.append((포함항목.name, 포함항목.read_bytes()))
        ఫైలు_జాబితా = [(개수, గమ్యం_డేటా) for 개수, గమ్యం_డేటా in ఫైలు_జాబితా if 개수 != పేరు] + [(పేరు, డేటా)]
        for అప్_లోడ్_పేరు, అప్_లోడ్_డేటా in ఫైలు_జాబితా:
            if len(అప్_లోడ్_డేటా) > 16384 or len(అప్_లోడ్_పేరు.encode('utf-8')) > 63 or '\n' in అప్_లోడ్_పేరు or '\r' in అప్_లోడ్_పేరు:
                raise ValueError('추가 파일의 పేరు/పరిమాణం 제한 초과: ' + అప్_లోడ్_పేరు)
            పంపు('load ' + shlex.quote(అప్_లోడ్_పేరు), b'hex> ')
            for 순번 in range(0, len(అప్_లోడ్_డేటా), 64): పంపు(అప్_లోడ్_డేటా[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in పంపు('.'): raise RuntimeError('upload failed: ' + అప్_లోడ్_పేరు)
            갈무리자료 = పంపు('hex ' + shlex.quote(అప్_లోడ్_పేరు))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != అప్_లోడ్_డేటా: raise RuntimeError('upload verification failed')
        if వర్గం_మూల్యం == '.java' and అమలు_చేయి_ఆదేశం('javac ' + shlex.quote(పేరు)) != 0: return 1
        실행가능파일 = కారకం_శ్రేణి.file.stem + '.elf'
        if వర్గం_మూల్యం == '.c' and అమలు_చేయి_ఆదేశం('cc ' + shlex.quote(పేరు) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        అనువర్తనం = 'java ' + shlex.quote(కారకం_శ్రేణి.class_name or కారకం_శ్రేణి.file.stem) if వర్గం_మూల్యం in ('.java', '.class') else ('python ' if వర్గం_మూల్యం == '.py' else 'run ') + shlex.quote(పేరు)
        if వర్గం_మూల్యం == '.jar': అనువర్తనం = 'java -jar ' + shlex.quote(పేరు)
        if వర్గం_మూల్యం == '.c': అనువర్తనం = 'run ' + shlex.quote(실행가능파일)
        if కారకం_శ్రేణి.linux: అనువర్తనం = 'run --linux ' + shlex.quote(పేరు)
        if కారకం_శ్రేణి.arguments: అనువర్తనం += ' ' + ' '.join(shlex.quote(అక్షరసరం_డేటా) for అక్షరసరం_డేటా in కారకం_శ్రేణి.arguments)
        return 0 if అమలు_చేయి_ఆదేశం(అనువర్తనం) == 0 else 1
    finally:
        if క్రమణం.poll() is None:
            క్రమణం.terminate()
            try: క్రమణం.wait(timeout=5)
            except subprocess.TimeoutExpired: క్రమణం.kill(); క్రమణం.wait(timeout=5)
        సెలక్టర్.close(); క్రమణం.stdin.close(); క్రమణం.stdout.close()


if __name__ == '__main__':
    raise SystemExit(నడుపుము())
