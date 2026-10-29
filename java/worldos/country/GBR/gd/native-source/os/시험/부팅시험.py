#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

suidhich = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        tomhas = 검사()
        if tomhas:
            return tomhas
        time.sleep(0.05)
    raise AssertionError('TIME_VALUE 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        monatair_slighe = 임시 / 'monitor.sock'
        àithne = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monatair_slighe) + ',server,nowait']
        àithne += ['-kernel', str(suidhich / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(suidhich / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        àithne += ['-S']
        Pròiseas_VALUE = subprocess.Popen(àithne, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        monatair_VALUE = socket.socket(socket.AF_UNIX)
        LOG_ràgh = bytearray()
        try:
            def 소켓준비():
                if Pròiseas_VALUE.poll() is not None:
                    raise AssertionError(Pròiseas_VALUE.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and monatair_slighe.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            monatair_VALUE.connect(str(monatair_slighe))
            직렬.setblocking(False)
            monatair_VALUE.sendall(b'cont\n')

            def 포함(sreang_VALUE, ruith=0):
                읽기, _, _ = select.select([직렬], [], [], 0.1)
                if 읽기:
                    dàta = 직렬.recv(65536)
                    if not dàta:
                        raise AssertionError('직렬 CONNECT fàg_ap')
                    LOG_ràgh.extend(dàta)
                if Pròiseas_VALUE.poll() is not None:
                    raise AssertionError('QEMU 비정상 fàg_ap: ' + str(Pròiseas_VALUE.returncode))
                return sreang_VALUE.encode('utf-8') in LOG_ràgh[ruith:]

            def 명령시험(입력, 기대):
                ruith = len(LOG_ràgh)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, ruith), 기대)
                기다리기(lambda: 포함('jkoros> ', ruith), 'àithne 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in LOG_ràgh
            assert '자바 기계어 eitean_VALUE ruith'.encode() in LOG_ràgh
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for INDEX in range(8):
                명령시험('alloc\n', 'earrann_VALUE INDEX: ' + str(INDEX))
            명령시험('alloc\n', 'earrann_VALUE INDEX: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 earrann_VALUE')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'earrann_VALUE INDEX: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            ruith = len(LOG_ràgh)
            for Iuchair_VALUE in ('i', 'n', 'f', 'o', 'ret'):
                monatair_VALUE.sendall(('sendkey ' + Iuchair_VALUE + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', ruith), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 àithne')
            assert b'PANIC' not in LOG_ràgh and b'SELFTEST FAIL' not in LOG_ràgh
            print('PASS: {} 부팅, Java 자체 시험, 직렬 àithne, PS/2 입력, sònraich_stòras/return_tomhas, 정지'.format(종류))
            return LOG_ràgh.decode('utf-8', 'replace')
        finally:
            직렬.close()
            monatair_VALUE.close()
            Pròiseas_VALUE.terminate()
            try:
                Pròiseas_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Pròiseas_VALUE.kill()
                Pròiseas_VALUE.wait()


if __name__ == '__main__':
    tomhas = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (suidhich / 'build/부팅시험.json').write_text(json.dumps(tomhas, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
