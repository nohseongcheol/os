#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

Posizioa = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        EMAITZA = 검사()
        if EMAITZA:
            return EMAITZA
        time.sleep(0.05)
    raise AssertionError('ordua_balio 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        monitore_bide_izen = 임시 / 'monitor.sock'
        Komandoa = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitore_bide_izen) + ',server,nowait']
        Komandoa += ['-kernel', str(Posizioa / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(Posizioa / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        Komandoa += ['-S']
        prozesu_balio = subprocess.Popen(Komandoa, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        monitore_balio = socket.socket(socket.AF_UNIX)
        LOG_marka = bytearray()
        try:
            def 소켓준비():
                if prozesu_balio.poll() is not None:
                    raise AssertionError(prozesu_balio.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and monitore_bide_izen.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            monitore_balio.connect(str(monitore_bide_izen))
            직렬.setblocking(False)
            monitore_balio.sendall(b'cont\n')

            def 포함(kate_balio, Exekutatu_2=0):
                Irakurri, _, _ = select.select([직렬], [], [], 0.1)
                if Irakurri:
                    datuak = 직렬.recv(65536)
                    if not datuak:
                        raise AssertionError('직렬 Konektatu irten_aplik')
                    LOG_marka.extend(datuak)
                if prozesu_balio.poll() is not None:
                    raise AssertionError('QEMU 비정상 irten_aplik: ' + str(prozesu_balio.returncode))
                return kate_balio.encode('utf-8') in LOG_marka[Exekutatu_2:]

            def 명령시험(입력, 기대):
                Exekutatu_2 = len(LOG_marka)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, Exekutatu_2), 기대)
                기다리기(lambda: 포함('jkoros> ', Exekutatu_2), 'Komandoa 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in LOG_marka
            assert '자바 기계어 nukleo_balio Exekutatu_2'.encode() in LOG_marka
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for INDIZE in range(8):
                명령시험('alloc\n', 'sekzio_balio INDIZE: ' + str(INDIZE))
            명령시험('alloc\n', 'sekzio_balio INDIZE: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 sekzio_balio')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'sekzio_balio INDIZE: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Exekutatu_2 = len(LOG_marka)
            for gako_balio in ('i', 'n', 'f', 'o', 'ret'):
                monitore_balio.sendall(('sendkey ' + gako_balio + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', Exekutatu_2), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 Komandoa')
            assert b'PANIC' not in LOG_marka and b'SELFTEST FAIL' not in LOG_marka
            print('PASS: {} 부팅, Java 자체 시험, 직렬 Komandoa, PS/2 입력, esleitu_biltegi/itzuli_neurria, 정지'.format(종류))
            return LOG_marka.decode('utf-8', 'replace')
        finally:
            직렬.close()
            monitore_balio.close()
            prozesu_balio.terminate()
            try:
                prozesu_balio.wait(timeout=3)
            except subprocess.TimeoutExpired:
                prozesu_balio.kill()
                prozesu_balio.wait()


if __name__ == '__main__':
    EMAITZA = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (Posizioa / 'build/부팅시험.json').write_text(json.dumps(EMAITZA, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
