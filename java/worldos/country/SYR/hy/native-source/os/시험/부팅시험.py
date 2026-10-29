#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

Դիրք = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        չափ = 검사()
        if չափ:
            return չափ
        time.sleep(0.05)
    raise AssertionError('시간 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        մոնիտոր_ուղի = 임시 / 'monitor.sock'
        Հրահանգ = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(մոնիտոր_ուղի) + ',server,nowait']
        Հրահանգ += ['-kernel', str(Դիրք / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(Դիրք / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        Հրահանգ += ['-S']
        Ընթացք_արժեք = subprocess.Popen(Հրահանգ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        մոնիտոր_արժեք = socket.socket(socket.AF_UNIX)
        մատյան_տող = bytearray()
        try:
            def 소켓준비():
                if Ընթացք_արժեք.poll() is not None:
                    raise AssertionError(Ընթացք_արժեք.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and մոնիտոր_ուղի.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            մոնիտոր_արժեք.connect(str(մոնիտոր_ուղի))
            직렬.setblocking(False)
            մոնիտոր_արժեք.sendall(b'cont\n')

            def 포함(տող_արժեք_6ca8363c, Գործարկել=0):
                Ընթերցում, _, _ = select.select([직렬], [], [], 0.1)
                if Ընթերցում:
                    տվյալ = 직렬.recv(65536)
                    if not տվյալ:
                        raise AssertionError('직렬 Միացնել Ելք_ծրագիր')
                    մատյան_տող.extend(տվյալ)
                if Ընթացք_արժեք.poll() is not None:
                    raise AssertionError('QEMU 비정상 Ելք_ծրագիր: ' + str(Ընթացք_արժեք.returncode))
                return տող_արժեք_6ca8363c.encode('utf-8') in մատյան_տող[Գործարկել:]

            def 명령시험(입력, 기대):
                Գործարկել = len(մատյան_տող)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, Գործարկել), 기대)
                기다리기(lambda: 포함('jkoros> ', Գործարկել), 'Հրահանգ 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in մատյան_տող
            assert '자바 기계어 միջուկ_արժեք Գործարկել'.encode() in մատյան_տող
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for դասիչ in range(8):
                명령시험('alloc\n', 'խումբ_արժեք_366e0bfa դասիչ: ' + str(դասիչ))
            명령시험('alloc\n', 'խումբ_արժեք_366e0bfa դասիչ: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 խումբ_արժեք_366e0bfa')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'խումբ_արժեք_366e0bfa դասիչ: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Գործարկել = len(մատյան_տող)
            for ստեղն_արժեք in ('i', 'n', 'f', 'o', 'ret'):
                մոնիտոր_արժեք.sendall(('sendkey ' + ստեղն_արժեք + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', Գործարկել), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 Հրահանգ')
            assert b'PANIC' not in մատյան_տող and b'SELFTEST FAIL' not in մատյան_տող
            print('PASS: {} 부팅, Java 자체 시험, 직렬 Հրահանգ, PS/2 입력, հատկացնել_Պահեստ/վերադարձնել_չափ, 정지'.format(종류))
            return մատյան_տող.decode('utf-8', 'replace')
        finally:
            직렬.close()
            մոնիտոր_արժեք.close()
            Ընթացք_արժեք.terminate()
            try:
                Ընթացք_արժեք.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Ընթացք_արժեք.kill()
                Ընթացք_արժեք.wait()


if __name__ == '__main__':
    չափ = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (Դիրք / 'build/부팅시험.json').write_text(json.dumps(չափ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
