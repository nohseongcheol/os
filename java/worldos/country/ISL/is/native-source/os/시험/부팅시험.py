#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

Staðsetning = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        NIÐURSTAÐA = 검사()
        if NIÐURSTAÐA:
            return NIÐURSTAÐA
        time.sleep(0.05)
    raise AssertionError('TIME_VALUE 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        skjár_slóð = 임시 / 'monitor.sock'
        Skipun = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(skjár_slóð) + ',server,nowait']
        Skipun += ['-kernel', str(Staðsetning / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(Staðsetning / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        Skipun += ['-S']
        Ferli_VALUE = subprocess.Popen(Skipun, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        skjár_VALUE = socket.socket(socket.AF_UNIX)
        LOG_lína = bytearray()
        try:
            def 소켓준비():
                if Ferli_VALUE.poll() is not None:
                    raise AssertionError(Ferli_VALUE.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and skjár_slóð.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            skjár_VALUE.connect(str(skjár_slóð))
            직렬.setblocking(False)
            skjár_VALUE.sendall(b'cont\n')

            def 포함(strengur_VALUE, Keyra_2=0):
                Lestur, _, _ = select.select([직렬], [], [], 0.1)
                if Lestur:
                    gögn = 직렬.recv(65536)
                    if not gögn:
                        raise AssertionError('직렬 Tengjast loka_forrit')
                    LOG_lína.extend(gögn)
                if Ferli_VALUE.poll() is not None:
                    raise AssertionError('QEMU 비정상 loka_forrit: ' + str(Ferli_VALUE.returncode))
                return strengur_VALUE.encode('utf-8') in LOG_lína[Keyra_2:]

            def 명령시험(입력, 기대):
                Keyra_2 = len(LOG_lína)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, Keyra_2), 기대)
                기다리기(lambda: 포함('jkoros> ', Keyra_2), 'Skipun 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in LOG_lína
            assert '자바 기계어 kjarni_VALUE Keyra_2'.encode() in LOG_lína
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for INDEX in range(8):
                명령시험('alloc\n', 'hluti_VALUE INDEX: ' + str(INDEX))
            명령시험('alloc\n', 'hluti_VALUE INDEX: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 hluti_VALUE')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'hluti_VALUE INDEX: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 númer 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Keyra_2 = len(LOG_lína)
            for Lykill_VALUE in ('i', 'n', 'f', 'o', 'ret'):
                skjár_VALUE.sendall(('sendkey ' + Lykill_VALUE + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', Keyra_2), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 Skipun')
            assert b'PANIC' not in LOG_lína and b'SELFTEST FAIL' not in LOG_lína
            print('PASS: {} 부팅, Java eigin 시험, 직렬 Skipun, PS/2 입력, úthluta_geymsla/skila_mæld_stærð, 정지'.format(종류))
            return LOG_lína.decode('utf-8', 'replace')
        finally:
            직렬.close()
            skjár_VALUE.close()
            Ferli_VALUE.terminate()
            try:
                Ferli_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Ferli_VALUE.kill()
                Ferli_VALUE.wait()


if __name__ == '__main__':
    NIÐURSTAÐA = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (Staðsetning / 'build/부팅시험.json').write_text(json.dumps(NIÐURSTAÐA, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
