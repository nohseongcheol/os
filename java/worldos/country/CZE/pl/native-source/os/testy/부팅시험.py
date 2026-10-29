#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

pozycja = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        WYNIK = 검사()
        if WYNIK:
            return WYNIK
        time.sleep(0.05)
    raise AssertionError('wartość_czasu 초과: ' + 설명)


def testy(Rodzaj_WARTOŚĆ):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        monitor_ścieżka = 임시 / 'monitor.sock'
        polecenie = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_ścieżka) + ',server,nowait']
        polecenie += ['-kernel', str(pozycja / 'build/kernel.elf')] if Rodzaj_WARTOŚĆ == 'elf' else [
            '-cdrom', str(pozycja / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        polecenie += ['-S']
        Proces_WARTOŚĆ = subprocess.Popen(polecenie, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        monitor_WARTOŚĆ = socket.socket(socket.AF_UNIX)
        LOG_zapis = bytearray()
        try:
            def Przygotuj_gniazdo():
                if Proces_WARTOŚĆ.poll() is not None:
                    raise AssertionError(Proces_WARTOŚĆ.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and monitor_ścieżka.exists()
            기다리기(Przygotuj_gniazdo, 'QEMU gniazdo_WARTOŚĆ')
            직렬.connect(str(직렬경로))
            monitor_WARTOŚĆ.connect(str(monitor_ścieżka))
            직렬.setblocking(False)
            monitor_WARTOŚĆ.sendall(b'cont\n')

            def deklaracje(ciąg_WARTOŚĆ, Uruchom_2=0):
                Odczyt, _, _ = select.select([직렬], [], [], 0.1)
                if Odczyt:
                    dane = 직렬.recv(65536)
                    if not dane:
                        raise AssertionError('직렬 Połącz wyjść_program')
                    LOG_zapis.extend(dane)
                if Proces_WARTOŚĆ.poll() is not None:
                    raise AssertionError('QEMU 비정상 wyjść_program: ' + str(Proces_WARTOŚĆ.returncode))
                return ciąg_WARTOŚĆ.encode('utf-8') in LOG_zapis[Uruchom_2:]

            def 명령시험(wejście_WARTOŚĆ, 기대):
                Uruchom_2 = len(LOG_zapis)
                직렬.sendall(wejście_WARTOŚĆ.encode('ascii'))
                기다리기(lambda: deklaracje(기대, Uruchom_2), 기대)
                기다리기(lambda: deklaracje('jkoros> ', Uruchom_2), 'polecenie 후 프롬프트')

            기다리기(lambda: deklaracje('READY'), Rodzaj_WARTOŚĆ + ' rozruch_maszyny')
            assert b'JAVA SELFTEST PASS' in LOG_zapis
            assert '자바 기계어 jądro_WARTOŚĆ Uruchom_2'.encode() in LOG_zapis
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for INDEKS in range(8):
                명령시험('alloc\n', 'obszar_WARTOŚĆ_366e0bfa INDEKS: ' + str(INDEKS))
            명령시험('alloc\n', 'obszar_WARTOŚĆ_366e0bfa INDEKS: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 obszar_WARTOŚĆ_366e0bfa')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'obszar_WARTOŚĆ_366e0bfa INDEKS: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 identyfikator 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Uruchom_2 = len(LOG_zapis)
            for Klucz_WARTOŚĆ in ('i', 'n', 'f', 'o', 'ret'):
                monitor_WARTOŚĆ.sendall(('sendkey ' + Klucz_WARTOŚĆ + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: deklaracje('embedded subset JVM / polling kernel', Uruchom_2), 'PS/2 info wejście_WARTOŚĆ')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: deklaracje('HALTED'), '정지 polecenie')
            assert b'PANIC' not in LOG_zapis and b'SELFTEST FAIL' not in LOG_zapis
            print('PASS: {} rozruch_maszyny, Java własny testy, 직렬 polecenie, PS/2 wejście_WARTOŚĆ, przydzielić_Pamięć/Zwrot_KR, 정지'.format(Rodzaj_WARTOŚĆ))
            return LOG_zapis.decode('utf-8', 'replace')
        finally:
            직렬.close()
            monitor_WARTOŚĆ.close()
            Proces_WARTOŚĆ.terminate()
            try:
                Proces_WARTOŚĆ.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Proces_WARTOŚĆ.kill()
                Proces_WARTOŚĆ.wait()


if __name__ == '__main__':
    WYNIK = {Rodzaj_WARTOŚĆ: testy(Rodzaj_WARTOŚĆ) for Rodzaj_WARTOŚĆ in ('elf', 'iso')}
    (pozycja / 'build/부팅시험.json').write_text(json.dumps(WYNIK, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
