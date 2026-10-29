#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

מיקום = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        תוצאה = 검사()
        if תוצאה:
            return תוצאה
        time.sleep(0.05)
    raise AssertionError('ערך_זמן 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        צג_נתיב = 임시 / 'monitor.sock'
        פקודה = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(צג_נתיב) + ',server,nowait']
        פקודה += ['-kernel', str(מיקום / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(מיקום / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        פקודה += ['-S']
        תהליך_ערך = subprocess.Popen(פקודה, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        צג_ערך = socket.socket(socket.AF_UNIX)
        לרשום_שיא = bytearray()
        try:
            def 소켓준비():
                if תהליך_ערך.poll() is not None:
                    raise AssertionError(תהליך_ערך.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and צג_נתיב.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            צג_ערך.connect(str(צג_נתיב))
            직렬.setblocking(False)
            צג_ערך.sendall(b'cont\n')

            def 포함(מחרוזת_ערך, הפעלה=0):
                קרא, _, _ = select.select([직렬], [], [], 0.1)
                if קרא:
                    נתונים = 직렬.recv(65536)
                    if not נתונים:
                        raise AssertionError('직렬 חיבור יציאה_תוכנית')
                    לרשום_שיא.extend(נתונים)
                if תהליך_ערך.poll() is not None:
                    raise AssertionError('QEMU 비정상 יציאה_תוכנית: ' + str(תהליך_ערך.returncode))
                return מחרוזת_ערך.encode('utf-8') in לרשום_שיא[הפעלה:]

            def 명령시험(קלט_ערך, 기대):
                הפעלה = len(לרשום_שיא)
                직렬.sendall(קלט_ערך.encode('ascii'))
                기다리기(lambda: 포함(기대, הפעלה), 기대)
                기다리기(lambda: 포함('jkoros> ', הפעלה), 'פקודה 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in לרשום_שיא
            assert '자바 기계어 ליבה_ערך הפעלה'.encode() in לרשום_שיא
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for מדד in range(8):
                명령시험('alloc\n', 'מקטע_ערך מדד: ' + str(מדד))
            명령시험('alloc\n', 'מקטע_ערך מדד: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 מקטע_ערך')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'מקטע_ערך מדד: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            הפעלה = len(לרשום_שיא)
            for מקש_ערך in ('i', 'n', 'f', 'o', 'ret'):
                צג_ערך.sendall(('sendkey ' + מקש_ערך + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', הפעלה), 'PS/2 info קלט_ערך')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 פקודה')
            assert b'PANIC' not in לרשום_שיא and b'SELFTEST FAIL' not in לרשום_שיא
            print('PASS: {} 부팅, Java עצמי 시험, 직렬 פקודה, PS/2 קלט_ערך, הקצה_אחסון/החזר_תוצאה, 정지'.format(종류))
            return לרשום_שיא.decode('utf-8', 'replace')
        finally:
            직렬.close()
            צג_ערך.close()
            תהליך_ערך.terminate()
            try:
                תהליך_ערך.wait(timeout=3)
            except subprocess.TimeoutExpired:
                תהליך_ערך.kill()
                תהליך_ערך.wait()


if __name__ == '__main__':
    תוצאה = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (מיקום / 'build/부팅시험.json').write_text(json.dumps(תוצאה, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
