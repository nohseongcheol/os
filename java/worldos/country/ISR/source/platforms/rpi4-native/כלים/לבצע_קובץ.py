#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. ארח 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from לבצע_פקודה import פקודה


def הפעלה():
    מנתח = argparse.ArgumentParser(description=__doc__)
    מנתח.add_argument('file', type=Path)
    מנתח.add_argument('arguments', nargs='*')
    מנתח.add_argument('--class-name', help='패키지가 있는 .class의 전체 שם(예: לאמת.נסה_חבילה)')
    מנתח.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI שימוש_ערך')
    מנתח.add_argument('--vnc', help='예: 127.0.0.1:2')
    מנתח.add_argument('--include', action='append', type=Path, default=[], help='צירוף_ערך_b73accca class קובץ 또는 class 디렉터리(패키지 שם 유지)')
    ארגומנט_מערך = מנתח.parse_args()
    נתונים = ארגומנט_מערך.file.read_bytes()
    if ארגומנט_מערך.class_name and ארגומנט_מערך.file.suffix != '.class': מנתח.error('--class-name은 .class 입력에서 사용합니다.')
    שם = ארגומנט_מערך.class_name + '.class' if ארגומנט_מערך.class_name else ארגומנט_מערך.file.name
    if len(נתונים) > 16384 or not 1 <= len(שם.encode('utf-8')) <= 63 or '\n' in שם or '\r' in שם:
        מנתח.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    אזור_ערך = '.elf' if נתונים[:4] == b'\x7fELF' else ארגומנט_מערך.file.suffix
    if ארגומנט_מערך.linux and אזור_ערך != '.elf': מנתח.error('--linux는 ELF 바이너리에만 사용합니다.')
    if אזור_ערך not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        מנתח.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(ארגומנט_מערך.arguments) > 7 or any(len(מחרוזת_נתונים.encode('utf-8')) > 255 or '\n' in מחרוזת_נתונים or '\r' in מחרוזת_נתונים for מחרוזת_נתונים in ארגומנט_מערך.arguments):
        מנתח.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    אפשרויות = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if ארגומנט_מערך.vnc: אפשרויות += ['-vnc', ארגומנט_מערך.vnc]
    תהליך = subprocess.Popen(פקודה() + אפשרויות, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    בורר = selectors.DefaultSelector(); בורר.register(תהליך.stdout, selectors.EVENT_READ)
    def לקבל_דואר(סמן, 시간제한=45):
        פלט = bytearray(); סיים_שיחה_היסט = time.monotonic() + 시간제한
        while סמן not in פלט:
            if time.monotonic() > סיים_שיחה_היסט: raise RuntimeError('UART timeout: ' + פלט.decode('utf-8', 'replace'))
            for 누름값, _ in בורר.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: פלט.extend(조각)
            if b'PANIC:' in פלט or b'FAIL ' in פלט: raise RuntimeError(פלט.decode('utf-8', 'replace'))
            if תהליך.poll() is not None: raise RuntimeError('QEMU exited: ' + פלט.decode('utf-8', 'replace'))
        return bytes(פלט)
    def שלח(שורה, סמן=b'jkoros-native> '):
        תהליך.stdin.write(שורה.encode('utf-8') + b'\n'); תהליך.stdin.flush()
        return לקבל_דואר(סמן)
    def לבצע_פקודה(שורה):
        פלט = שלח(שורה); sys.stdout.buffer.write(פלט); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', פלט)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        לקבל_דואר(b'jkoros-native> ')
        קובץ_רשימה = []
        for לכלול in ארגומנט_מערך.include:
            if לכלול.is_dir():
                קובץ_רשימה += [(str(נתונים_עמדה.relative_to(לכלול).with_suffix('')).replace('/', '.') + '.class', נתונים_עמדה.read_bytes()) for נתונים_עמדה in sorted(לכלול.rglob('*.class'))]
            else:
                קובץ_רשימה.append((לכלול.name, לכלול.read_bytes()))
        קובץ_רשימה = [(개수, יעד_נתונים) for 개수, יעד_נתונים in קובץ_רשימה if 개수 != שם] + [(שם, נתונים)]
        for העלה_שם, העלה_נתונים in קובץ_רשימה:
            if len(העלה_נתונים) > 16384 or len(העלה_שם.encode('utf-8')) > 63 or '\n' in העלה_שם or '\r' in העלה_שם:
                raise ValueError('צירוף_ערך_b73accca 파일의 שם/גודל 제한 초과: ' + העלה_שם)
            שלח('load ' + shlex.quote(העלה_שם), b'hex> ')
            for 순번 in range(0, len(העלה_נתונים), 64): שלח(העלה_נתונים[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in שלח('.'): raise RuntimeError('upload failed: ' + העלה_שם)
            갈무리자료 = שלח('hex ' + shlex.quote(העלה_שם))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != העלה_נתונים: raise RuntimeError('upload verification failed')
        if אזור_ערך == '.java' and לבצע_פקודה('javac ' + shlex.quote(שם)) != 0: return 1
        실행가능파일 = ארגומנט_מערך.file.stem + '.elf'
        if אזור_ערך == '.c' and לבצע_פקודה('cc ' + shlex.quote(שם) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        תוכנית = 'java ' + shlex.quote(ארגומנט_מערך.class_name or ארגומנט_מערך.file.stem) if אזור_ערך in ('.java', '.class') else ('python ' if אזור_ערך == '.py' else 'run ') + shlex.quote(שם)
        if אזור_ערך == '.jar': תוכנית = 'java -jar ' + shlex.quote(שם)
        if אזור_ערך == '.c': תוכנית = 'run ' + shlex.quote(실행가능파일)
        if ארגומנט_מערך.linux: תוכנית = 'run --linux ' + shlex.quote(שם)
        if ארגומנט_מערך.arguments: תוכנית += ' ' + ' '.join(shlex.quote(מחרוזת_נתונים) for מחרוזת_נתונים in ארגומנט_מערך.arguments)
        return 0 if לבצע_פקודה(תוכנית) == 0 else 1
    finally:
        if תהליך.poll() is None:
            תהליך.terminate()
            try: תהליך.wait(timeout=5)
            except subprocess.TimeoutExpired: תהליך.kill(); תהליך.wait(timeout=5)
        בורר.close(); תהליך.stdin.close(); תהליך.stdout.close()


if __name__ == '__main__':
    raise SystemExit(הפעלה())
