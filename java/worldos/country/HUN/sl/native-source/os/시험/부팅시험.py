#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

Položaj = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        REZULTAT = 검사()
        if REZULTAT:
            return REZULTAT
        time.sleep(0.05)
    raise AssertionError('čas_VALUE 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        monitor_pot = 임시 / 'monitor.sock'
        Ukaz = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_pot) + ',server,nowait']
        Ukaz += ['-kernel', str(Položaj / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(Položaj / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        Ukaz += ['-S']
        Proces_VALUE = subprocess.Popen(Ukaz, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        monitor_VALUE = socket.socket(socket.AF_UNIX)
        LOG_zapis = bytearray()
        try:
            def Pripravi_vtičnica():
                if Proces_VALUE.poll() is not None:
                    raise AssertionError(Proces_VALUE.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and monitor_pot.exists()
            기다리기(Pripravi_vtičnica, 'QEMU vtičnica_VALUE')
            직렬.connect(str(직렬경로))
            monitor_VALUE.connect(str(monitor_pot))
            직렬.setblocking(False)
            monitor_VALUE.sendall(b'cont\n')

            def 포함(niz_VALUE, Zaženi=0):
                Branje, _, _ = select.select([직렬], [], [], 0.1)
                if Branje:
                    podatki = 직렬.recv(65536)
                    if not podatki:
                        raise AssertionError('직렬 Poveži Izhod_aplikacija')
                    LOG_zapis.extend(podatki)
                if Proces_VALUE.poll() is not None:
                    raise AssertionError('QEMU 비정상 Izhod_aplikacija: ' + str(Proces_VALUE.returncode))
                return niz_VALUE.encode('utf-8') in LOG_zapis[Zaženi:]

            def 명령시험(입력, 기대):
                Zaženi = len(LOG_zapis)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, Zaženi), 기대)
                기다리기(lambda: 포함('jkoros> ', Zaženi), 'Ukaz 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in LOG_zapis
            assert '자바 기계어 jedro_VALUE Zaženi'.encode() in LOG_zapis
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for INDEX in range(8):
                명령시험('alloc\n', 'odsek_VALUE INDEX: ' + str(INDEX))
            명령시험('alloc\n', 'odsek_VALUE INDEX: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 odsek_VALUE')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'odsek_VALUE INDEX: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Zaženi = len(LOG_zapis)
            for Ključ_VALUE in ('i', 'n', 'f', 'o', 'ret'):
                monitor_VALUE.sendall(('sendkey ' + Ključ_VALUE + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', Zaženi), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 Ukaz')
            assert b'PANIC' not in LOG_zapis and b'SELFTEST FAIL' not in LOG_zapis
            print('PASS: {} 부팅, Java lastno 시험, 직렬 Ukaz, PS/2 입력, dodeliti_Senzor_prostora/vrni_KR, 정지'.format(종류))
            return LOG_zapis.decode('utf-8', 'replace')
        finally:
            직렬.close()
            monitor_VALUE.close()
            Proces_VALUE.terminate()
            try:
                Proces_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Proces_VALUE.kill()
                Proces_VALUE.wait()


if __name__ == '__main__':
    REZULTAT = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (Položaj / 'build/부팅시험.json').write_text(json.dumps(REZULTAT, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
