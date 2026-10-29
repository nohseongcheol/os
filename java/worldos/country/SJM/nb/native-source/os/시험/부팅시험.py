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
        KR = 검사()
        if KR:
            return KR
        time.sleep(0.05)
    raise AssertionError('TID_VERDI 초과: ' + 설명)


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
        Prosess_VERDI = subprocess.Popen(Kommando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        skjerm_VERDI = socket.socket(socket.AF_UNIX)
        LOG_POST = bytearray()
        try:
            def Forbered_socket():
                if Prosess_VERDI.poll() is not None:
                    raise AssertionError(Prosess_VERDI.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and skjerm_bane.exists()
            기다리기(Forbered_socket, 'QEMU socket_VERDI')
            직렬.connect(str(직렬경로))
            skjerm_VERDI.connect(str(skjerm_bane))
            직렬.setblocking(False)
            skjerm_VERDI.sendall(b'cont\n')

            def 포함(streng_VERDI, Kjør_2=0):
                Les, _, _ = select.select([직렬], [], [], 0.1)
                if Les:
                    data = 직렬.recv(65536)
                    if not data:
                        raise AssertionError('직렬 Koble_til Utgang_app')
                    LOG_POST.extend(data)
                if Prosess_VERDI.poll() is not None:
                    raise AssertionError('QEMU 비정상 Utgang_app: ' + str(Prosess_VERDI.returncode))
                return streng_VERDI.encode('utf-8') in LOG_POST[Kjør_2:]

            def 명령시험(inndata_VERDI, 기대):
                Kjør_2 = len(LOG_POST)
                직렬.sendall(inndata_VERDI.encode('ascii'))
                기다리기(lambda: 포함(기대, Kjør_2), 기대)
                기다리기(lambda: 포함('jkoros> ', Kjør_2), 'Kommando 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in LOG_POST
            assert '자바 기계어 kjerne_VERDI Kjør_2'.encode() in LOG_POST
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for INDEKS in range(8):
                명령시험('alloc\n', 'inndeling_VERDI INDEKS: ' + str(INDEKS))
            명령시험('alloc\n', 'inndeling_VERDI INDEKS: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 inndeling_VERDI')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'inndeling_VERDI INDEKS: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 nummer 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Kjør_2 = len(LOG_POST)
            for tast_VERDI in ('i', 'n', 'f', 'o', 'ret'):
                skjerm_VERDI.sendall(('sendkey ' + tast_VERDI + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', Kjør_2), 'PS/2 info inndata_VERDI')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 Kommando')
            assert b'PANIC' not in LOG_POST and b'SELFTEST FAIL' not in LOG_POST
            print('PASS: {} 부팅, Java eget 시험, 직렬 Kommando, PS/2 inndata_VERDI, tildele_lager/return_KR, 정지'.format(종류))
            return LOG_POST.decode('utf-8', 'replace')
        finally:
            직렬.close()
            skjerm_VERDI.close()
            Prosess_VERDI.terminate()
            try:
                Prosess_VERDI.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Prosess_VERDI.kill()
                Prosess_VERDI.wait()


if __name__ == '__main__':
    KR = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (Posisjon / 'build/부팅시험.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
