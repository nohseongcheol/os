#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

Pozicija = Path(__file__).resolve().parents[1]


def 기다리기(검사, aprašas, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        REZULTATAS = 검사()
        if REZULTATAS:
            return REZULTATAS
        time.sleep(0.05)
    raise AssertionError('TIME_VALUE 초과: ' + aprašas)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        stebėti_kelias = 임시 / 'monitor.sock'
        Komanda = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(stebėti_kelias) + ',server,nowait']
        Komanda += ['-kernel', str(Pozicija / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(Pozicija / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        Komanda += ['-S']
        Procesas_VALUE = subprocess.Popen(Komanda, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        stebėti_VALUE = socket.socket(socket.AF_UNIX)
        LOG_RECORD = bytearray()
        try:
            def 소켓준비():
                if Procesas_VALUE.poll() is not None:
                    raise AssertionError(Procesas_VALUE.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and stebėti_kelias.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            stebėti_VALUE.connect(str(stebėti_kelias))
            직렬.setblocking(False)
            stebėti_VALUE.sendall(b'cont\n')

            def 포함(eilutė_VALUE, Paleisti=0):
                Skaitymas, _, _ = select.select([직렬], [], [], 0.1)
                if Skaitymas:
                    duomenys = 직렬.recv(65536)
                    if not duomenys:
                        raise AssertionError('직렬 Prisijungti Baigti_programa_086bb533')
                    LOG_RECORD.extend(duomenys)
                if Procesas_VALUE.poll() is not None:
                    raise AssertionError('QEMU 비정상 Baigti_programa_086bb533: ' + str(Procesas_VALUE.returncode))
                return eilutė_VALUE.encode('utf-8') in LOG_RECORD[Paleisti:]

            def 명령시험(입력, 기대):
                Paleisti = len(LOG_RECORD)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, Paleisti), 기대)
                기다리기(lambda: 포함('jkoros> ', Paleisti), 'Komanda 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in LOG_RECORD
            assert '자바 기계어 branduolys_VALUE Paleisti'.encode() in LOG_RECORD
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for INDEX in range(8):
                명령시험('alloc\n', 'sekcija_VALUE INDEX: ' + str(INDEX))
            명령시험('alloc\n', 'sekcija_VALUE INDEX: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 sekcija_VALUE')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'sekcija_VALUE INDEX: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 numeris 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Paleisti = len(LOG_RECORD)
            for Raktas_VALUE in ('i', 'n', 'f', 'o', 'ret'):
                stebėti_VALUE.sendall(('sendkey ' + Raktas_VALUE + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', Paleisti), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 Komanda')
            assert b'PANIC' not in LOG_RECORD and b'SELFTEST FAIL' not in LOG_RECORD
            print('PASS: {} 부팅, Java savas 시험, 직렬 Komanda, PS/2 입력, priskirti_Saugykla/grąžinti_KR, 정지'.format(종류))
            return LOG_RECORD.decode('utf-8', 'replace')
        finally:
            직렬.close()
            stebėti_VALUE.close()
            Procesas_VALUE.terminate()
            try:
                Procesas_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Procesas_VALUE.kill()
                Procesas_VALUE.wait()


if __name__ == '__main__':
    REZULTATAS = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (Pozicija / 'build/부팅시험.json').write_text(json.dumps(REZULTATAS, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
