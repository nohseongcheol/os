#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

positionéieren = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        Mooss = 검사()
        if Mooss:
            return Mooss
        time.sleep(0.05)
    raise AssertionError('TIME_VALUE 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        Schierm_Wee = 임시 / 'monitor.sock'
        Befeel = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(Schierm_Wee) + ',server,nowait']
        Befeel += ['-kernel', str(positionéieren / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(positionéieren / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        Befeel += ['-S']
        Prozess_VALUE = subprocess.Popen(Befeel, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        Schierm_VALUE = socket.socket(socket.AF_UNIX)
        LOG_Rei = bytearray()
        try:
            def 소켓준비():
                if Prozess_VALUE.poll() is not None:
                    raise AssertionError(Prozess_VALUE.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and Schierm_Wee.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            Schierm_VALUE.connect(str(Schierm_Wee))
            직렬.setblocking(False)
            Schierm_VALUE.sendall(b'cont\n')

            def 포함(Zeechefolleg_VALUE, Laf=0):
                읽기, _, _ = select.select([직렬], [], [], 0.1)
                if 읽기:
                    Daten = 직렬.recv(65536)
                    if not Daten:
                        raise AssertionError('직렬 Verbannen Schluss_App')
                    LOG_Rei.extend(Daten)
                if Prozess_VALUE.poll() is not None:
                    raise AssertionError('QEMU 비정상 Schluss_App: ' + str(Prozess_VALUE.returncode))
                return Zeechefolleg_VALUE.encode('utf-8') in LOG_Rei[Laf:]

            def 명령시험(입력, 기대):
                Laf = len(LOG_Rei)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, Laf), 기대)
                기다리기(lambda: 포함('jkoros> ', Laf), 'Befeel 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in LOG_Rei
            assert '자바 기계어 Kernel_VALUE Laf'.encode() in LOG_Rei
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for INDEX in range(8):
                명령시험('alloc\n', 'Beräich_VALUE INDEX: ' + str(INDEX))
            명령시험('alloc\n', 'Beräich_VALUE INDEX: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 Beräich_VALUE')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'Beräich_VALUE INDEX: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Laf = len(LOG_Rei)
            for Tast_VALUE in ('i', 'n', 'f', 'o', 'ret'):
                Schierm_VALUE.sendall(('sendkey ' + Tast_VALUE + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', Laf), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 Befeel')
            assert b'PANIC' not in LOG_Rei and b'SELFTEST FAIL' not in LOG_Rei
            print('PASS: {} 부팅, Java 자체 시험, 직렬 Befeel, PS/2 입력, zouweisen_Späicher/반환, 정지'.format(종류))
            return LOG_Rei.decode('utf-8', 'replace')
        finally:
            직렬.close()
            Schierm_VALUE.close()
            Prozess_VALUE.terminate()
            try:
                Prozess_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Prozess_VALUE.kill()
                Prozess_VALUE.wait()


if __name__ == '__main__':
    Mooss = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (positionéieren / 'build/부팅시험.json').write_text(json.dumps(Mooss, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
