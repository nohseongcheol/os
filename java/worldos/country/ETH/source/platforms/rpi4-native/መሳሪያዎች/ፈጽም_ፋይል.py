#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. አዘጋጅ_b78e430d 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from ፈጽም_ትእዛዝ import ትእዛዝ


def ማስኬጃ():
    አግልሎ_ማስቀመጥ = argparse.ArgumentParser(description=__doc__)
    አግልሎ_ማስቀመጥ.add_argument('file', type=Path)
    አግልሎ_ማስቀመጥ.add_argument('arguments', nargs='*')
    አግልሎ_ማስቀመጥ.add_argument('--class-name', help='패키지가 있는 .class의 전체 ስም(예: ትክክለኛነት_አረጋግጥ.꾸러미시험)')
    አግልሎ_ማስቀመጥ.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    አግልሎ_ማስቀመጥ.add_argument('--vnc', help='예: 127.0.0.1:2')
    አግልሎ_ማስቀመጥ.add_argument('--include', action='append', type=Path, default=[], help='추가 class ፋይል 또는 class 디렉터리(패키지 ስም 유지)')
    ነጋሪ_እሴት_ድርድር = አግልሎ_ማስቀመጥ.parse_args()
    ውሂብ = ነጋሪ_እሴት_ድርድር.file.read_bytes()
    if ነጋሪ_እሴት_ድርድር.class_name and ነጋሪ_እሴት_ድርድር.file.suffix != '.class': አግልሎ_ማስቀመጥ.error('--class-name은 .class 입력에서 사용합니다.')
    ስም = ነጋሪ_እሴት_ድርድር.class_name + '.class' if ነጋሪ_እሴት_ድርድር.class_name else ነጋሪ_እሴት_ድርድር.file.name
    if len(ውሂብ) > 16384 or not 1 <= len(ስም.encode('utf-8')) <= 63 or '\n' in ስም or '\r' in ስም:
        አግልሎ_ማስቀመጥ.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    ምድብ_እሴት = '.elf' if ውሂብ[:4] == b'\x7fELF' else ነጋሪ_እሴት_ድርድር.file.suffix
    if ነጋሪ_እሴት_ድርድር.linux and ምድብ_እሴት != '.elf': አግልሎ_ማስቀመጥ.error('--linux는 ELF 바이너리에만 사용합니다.')
    if ምድብ_እሴት not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        አግልሎ_ማስቀመጥ.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(ነጋሪ_እሴት_ድርድር.arguments) > 7 or any(len(ኅብረቁምፊ_ውሂብ.encode('utf-8')) > 255 or '\n' in ኅብረቁምፊ_ውሂብ or '\r' in ኅብረቁምፊ_ውሂብ for ኅብረቁምፊ_ውሂብ in ነጋሪ_እሴት_ድርድር.arguments):
        አግልሎ_ማስቀመጥ.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    አማራጮች = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if ነጋሪ_እሴት_ድርድር.vnc: አማራጮች += ['-vnc', ነጋሪ_እሴት_ድርድር.vnc]
    ሂደቶች = subprocess.Popen(ትእዛዝ() + አማራጮች, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    መራጭ = selectors.DefaultSelector(); መራጭ.register(ሂደቶች.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); ጨርስ_ዝንፍ = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > ጨርስ_ዝንፍ: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in መራጭ.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if ሂደቶች.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def ላክ(መስመር, 확인표시=b'jkoros-native> '):
        ሂደቶች.stdin.write(መስመር.encode('utf-8') + b'\n'); ሂደቶች.stdin.flush()
        return 수신하기(확인표시)
    def ፈጽም_ትእዛዝ(መስመር):
        출력결과 = ላክ(መስመር); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        ፋይል_ዝርዝር = []
        for 포함항목 in ነጋሪ_እሴት_ድርድር.include:
            if 포함항목.is_dir():
                ፋይል_ዝርዝር += [(str(ውሂብ_በቦታ_አስቀመጠ.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', ውሂብ_በቦታ_አስቀመጠ.read_bytes()) for ውሂብ_በቦታ_አስቀመጠ in sorted(포함항목.rglob('*.class'))]
            else:
                ፋይል_ዝርዝር.append((포함항목.name, 포함항목.read_bytes()))
        ፋይል_ዝርዝር = [(개수, መድረሻ_ውሂብ) for 개수, መድረሻ_ውሂብ in ፋይል_ዝርዝር if 개수 != ስም] + [(ስም, ውሂብ)]
        for መጫን_ስም, መጫን_ውሂብ in ፋይል_ዝርዝር:
            if len(መጫን_ውሂብ) > 16384 or len(መጫን_ስም.encode('utf-8')) > 63 or '\n' in መጫን_ስም or '\r' in መጫን_ስም:
                raise ValueError('추가 파일의 ስም/መጠን 제한 초과: ' + መጫን_ስም)
            ላክ('load ' + shlex.quote(መጫን_ስም), b'hex> ')
            for 순번 in range(0, len(መጫን_ውሂብ), 64): ላክ(መጫን_ውሂብ[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in ላክ('.'): raise RuntimeError('upload failed: ' + መጫን_ስም)
            갈무리자료 = ላክ('hex ' + shlex.quote(መጫን_ስም))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != መጫን_ውሂብ: raise RuntimeError('upload verification failed')
        if ምድብ_እሴት == '.java' and ፈጽም_ትእዛዝ('javac ' + shlex.quote(ስም)) != 0: return 1
        실행가능파일 = ነጋሪ_እሴት_ድርድር.file.stem + '.elf'
        if ምድብ_እሴት == '.c' and ፈጽም_ትእዛዝ('cc ' + shlex.quote(ስም) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        ፕሮግራም = 'java ' + shlex.quote(ነጋሪ_እሴት_ድርድር.class_name or ነጋሪ_እሴት_ድርድር.file.stem) if ምድብ_እሴት in ('.java', '.class') else ('python ' if ምድብ_እሴት == '.py' else 'run ') + shlex.quote(ስም)
        if ምድብ_እሴት == '.jar': ፕሮግራም = 'java -jar ' + shlex.quote(ስም)
        if ምድብ_እሴት == '.c': ፕሮግራም = 'run ' + shlex.quote(실행가능파일)
        if ነጋሪ_እሴት_ድርድር.linux: ፕሮግራም = 'run --linux ' + shlex.quote(ስም)
        if ነጋሪ_እሴት_ድርድር.arguments: ፕሮግራም += ' ' + ' '.join(shlex.quote(ኅብረቁምፊ_ውሂብ) for ኅብረቁምፊ_ውሂብ in ነጋሪ_እሴት_ድርድር.arguments)
        return 0 if ፈጽም_ትእዛዝ(ፕሮግራም) == 0 else 1
    finally:
        if ሂደቶች.poll() is None:
            ሂደቶች.terminate()
            try: ሂደቶች.wait(timeout=5)
            except subprocess.TimeoutExpired: ሂደቶች.kill(); ሂደቶች.wait(timeout=5)
        መራጭ.close(); ሂደቶች.stdin.close(); ሂደቶች.stdout.close()


if __name__ == '__main__':
    raise SystemExit(ማስኬጃ())
