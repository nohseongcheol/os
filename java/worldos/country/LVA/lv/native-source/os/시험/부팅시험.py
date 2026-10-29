#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

Novietojums = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        mērs = 검사()
        if mērs:
            return mērs
        time.sleep(0.05)
    raise AssertionError('TIME_VALUE 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        monitors_ceļš = 임시 / 'monitor.sock'
        Komanda = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitors_ceļš) + ',server,nowait']
        Komanda += ['-kernel', str(Novietojums / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(Novietojums / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        Komanda += ['-S']
        Process_VALUE = subprocess.Popen(Komanda, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        monitors_VALUE = socket.socket(socket.AF_UNIX)
        LOG_RECORD = bytearray()
        try:
            def 소켓준비():
                if Process_VALUE.poll() is not None:
                    raise AssertionError(Process_VALUE.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and monitors_ceļš.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            monitors_VALUE.connect(str(monitors_ceļš))
            직렬.setblocking(False)
            monitors_VALUE.sendall(b'cont\n')

            def 포함(virkne_VALUE, Palaist=0):
                Lasīt, _, _ = select.select([직렬], [], [], 0.1)
                if Lasīt:
                    dati = 직렬.recv(65536)
                    if not dati:
                        raise AssertionError('직렬 Savienoties Iziet_programma')
                    LOG_RECORD.extend(dati)
                if Process_VALUE.poll() is not None:
                    raise AssertionError('QEMU 비정상 Iziet_programma: ' + str(Process_VALUE.returncode))
                return virkne_VALUE.encode('utf-8') in LOG_RECORD[Palaist:]

            def 명령시험(입력, 기대):
                Palaist = len(LOG_RECORD)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, Palaist), 기대)
                기다리기(lambda: 포함('jkoros> ', Palaist), 'Komanda 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in LOG_RECORD
            assert '자바 기계어 kodols_VALUE Palaist'.encode() in LOG_RECORD
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for INDEX in range(8):
                명령시험('alloc\n', 'sadaļa_VALUE INDEX: ' + str(INDEX))
            명령시험('alloc\n', 'sadaļa_VALUE INDEX: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 sadaļa_VALUE')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'sadaļa_VALUE INDEX: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 numurs 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Palaist = len(LOG_RECORD)
            for Atslēga_VALUE in ('i', 'n', 'f', 'o', 'ret'):
                monitors_VALUE.sendall(('sendkey ' + Atslēga_VALUE + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', Palaist), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 Komanda')
            assert b'PANIC' not in LOG_RECORD and b'SELFTEST FAIL' not in LOG_RECORD
            print('PASS: {} 부팅, Java savs 시험, 직렬 Komanda, PS/2 입력, piešķirt_Krātuve/atdot_mērs, 정지'.format(종류))
            return LOG_RECORD.decode('utf-8', 'replace')
        finally:
            직렬.close()
            monitors_VALUE.close()
            Process_VALUE.terminate()
            try:
                Process_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Process_VALUE.kill()
                Process_VALUE.wait()


if __name__ == '__main__':
    mērs = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (Novietojums / 'build/부팅시험.json').write_text(json.dumps(mērs, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
