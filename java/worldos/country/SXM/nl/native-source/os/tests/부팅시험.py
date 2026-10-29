#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

positie = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        resultaat = 검사()
        if resultaat:
            return resultaat
        time.sleep(0.05)
    raise AssertionError('TIJD_WAARDE 초과: ' + 설명)


def tests(soort_WAARDE):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        monitor_pad = 임시 / 'monitor.sock'
        opdracht = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_pad) + ',server,nowait']
        opdracht += ['-kernel', str(positie / 'build/kernel.elf')] if soort_WAARDE == 'elf' else [
            '-cdrom', str(positie / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        opdracht += ['-S']
        Proces_WAARDE = subprocess.Popen(opdracht, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        monitor_WAARDE = socket.socket(socket.AF_UNIX)
        LOG_RECORD = bytearray()
        try:
            def Bereid_voor_socket():
                if Proces_WAARDE.poll() is not None:
                    raise AssertionError(Proces_WAARDE.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and monitor_pad.exists()
            기다리기(Bereid_voor_socket, 'QEMU socket_WAARDE')
            직렬.connect(str(직렬경로))
            monitor_WAARDE.connect(str(monitor_pad))
            직렬.setblocking(False)
            monitor_WAARDE.sendall(b'cont\n')

            def declaraties(tekenreeks_WAARDE, starten=0):
                Lezen, _, _ = select.select([직렬], [], [], 0.1)
                if Lezen:
                    gegevens = 직렬.recv(65536)
                    if not gegevens:
                        raise AssertionError('직렬 Verbinden Einde_app')
                    LOG_RECORD.extend(gegevens)
                if Proces_WAARDE.poll() is not None:
                    raise AssertionError('QEMU 비정상 Einde_app: ' + str(Proces_WAARDE.returncode))
                return tekenreeks_WAARDE.encode('utf-8') in LOG_RECORD[starten:]

            def 명령시험(invoer_WAARDE, 기대):
                starten = len(LOG_RECORD)
                직렬.sendall(invoer_WAARDE.encode('ascii'))
                기다리기(lambda: declaraties(기대, starten), 기대)
                기다리기(lambda: declaraties('jkoros> ', starten), 'opdracht 후 프롬프트')

            기다리기(lambda: declaraties('READY'), soort_WAARDE + ' machineopstart')
            assert b'JAVA SELFTEST PASS' in LOG_RECORD
            assert '자바 기계어 kernel_WAARDE starten'.encode() in LOG_RECORD
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for INDEX in range(8):
                명령시험('alloc\n', 'sectie_WAARDE INDEX: ' + str(INDEX))
            명령시험('alloc\n', 'sectie_WAARDE INDEX: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 sectie_WAARDE')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'sectie_WAARDE INDEX: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 nummer 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            starten = len(LOG_RECORD)
            for toets_WAARDE in ('i', 'n', 'f', 'o', 'ret'):
                monitor_WAARDE.sendall(('sendkey ' + toets_WAARDE + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: declaraties('embedded subset JVM / polling kernel', starten), 'PS/2 info invoer_WAARDE')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: declaraties('HALTED'), '정지 opdracht')
            assert b'PANIC' not in LOG_RECORD and b'SELFTEST FAIL' not in LOG_RECORD
            print('PASS: {} machineopstart, Java Eigen tests, 직렬 opdracht, PS/2 invoer_WAARDE, toewijzen_Opslag/Retour_HR, 정지'.format(soort_WAARDE))
            return LOG_RECORD.decode('utf-8', 'replace')
        finally:
            직렬.close()
            monitor_WAARDE.close()
            Proces_WAARDE.terminate()
            try:
                Proces_WAARDE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Proces_WAARDE.kill()
                Proces_WAARDE.wait()


if __name__ == '__main__':
    resultaat = {soort_WAARDE: tests(soort_WAARDE) for soort_WAARDE in ('elf', 'iso')}
    (positie / 'build/부팅시험.json').write_text(json.dumps(resultaat, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
