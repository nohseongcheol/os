#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

Posisjon = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        forretningsmål = 검사()
        if forretningsmål:
            return forretningsmål
        time.sleep(0.05)
    raise AssertionError('TIME_VALUE 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        skjerm_bane = 임시 / 'monitor.sock'
        Kommando = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(skjerm_bane) + ',server,nowait']
        Kommando += ['-kernel', str(Posisjon / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(Posisjon / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        Kommando += ['-S']
        Prosess_VALUE = subprocess.Popen(Kommando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        skjerm_VALUE = socket.socket(socket.AF_UNIX)
        LOG_rad = bytearray()
        try:
            def 소켓준비():
                if Prosess_VALUE.poll() is not None:
                    raise AssertionError(Prosess_VALUE.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and skjerm_bane.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            skjerm_VALUE.connect(str(skjerm_bane))
            직렬.setblocking(False)
            skjerm_VALUE.sendall(b'cont\n')

            def 포함(streng_VALUE, Køyr_2=0):
                Les, _, _ = select.select([직렬], [], [], 0.1)
                if Les:
                    data = 직렬.recv(65536)
                    if not data:
                        raise AssertionError('직렬 Kopla_til Utgang_app')
                    LOG_rad.extend(data)
                if Prosess_VALUE.poll() is not None:
                    raise AssertionError('QEMU 비정상 Utgang_app: ' + str(Prosess_VALUE.returncode))
                return streng_VALUE.encode('utf-8') in LOG_rad[Køyr_2:]

            def 명령시험(입력, 기대):
                Køyr_2 = len(LOG_rad)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, Køyr_2), 기대)
                기다리기(lambda: 포함('jkoros> ', Køyr_2), 'Kommando 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in LOG_rad
            assert '자바 기계어 kjerne_VALUE Køyr_2'.encode() in LOG_rad
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for INDEX in range(8):
                명령시험('alloc\n', 'del_VALUE INDEX: ' + str(INDEX))
            명령시험('alloc\n', 'del_VALUE INDEX: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 del_VALUE')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'del_VALUE INDEX: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Køyr_2 = len(LOG_rad)
            for tast_VALUE in ('i', 'n', 'f', 'o', 'ret'):
                skjerm_VALUE.sendall(('sendkey ' + tast_VALUE + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', Køyr_2), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 Kommando')
            assert b'PANIC' not in LOG_rad and b'SELFTEST FAIL' not in LOG_rad
            print('PASS: {} 부팅, Java 자체 시험, 직렬 Kommando, PS/2 입력, tildele_Lagring/levere_tilbake_forretningsmål, 정지'.format(종류))
            return LOG_rad.decode('utf-8', 'replace')
        finally:
            직렬.close()
            skjerm_VALUE.close()
            Prosess_VALUE.terminate()
            try:
                Prosess_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Prosess_VALUE.kill()
                Prosess_VALUE.wait()


if __name__ == '__main__':
    forretningsmål = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (Posisjon / 'build/부팅시험.json').write_text(json.dumps(forretningsmål, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
