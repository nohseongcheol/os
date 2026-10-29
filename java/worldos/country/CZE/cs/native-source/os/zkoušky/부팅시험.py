#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

pozice = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        VÝSLEDEK = 검사()
        if VÝSLEDEK:
            return VÝSLEDEK
        time.sleep(0.05)
    raise AssertionError('časová_hodnota 초과: ' + 설명)


def zkoušky(Druh_HODNOTA):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        monitor_cesta = 임시 / 'monitor.sock'
        příkaz = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_cesta) + ',server,nowait']
        příkaz += ['-kernel', str(pozice / 'build/kernel.elf')] if Druh_HODNOTA == 'elf' else [
            '-cdrom', str(pozice / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        příkaz += ['-S']
        Proces_HODNOTA = subprocess.Popen(příkaz, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        monitor_HODNOTA = socket.socket(socket.AF_UNIX)
        LOGZ_ZÁZNAM = bytearray()
        try:
            def Připravit_soket():
                if Proces_HODNOTA.poll() is not None:
                    raise AssertionError(Proces_HODNOTA.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and monitor_cesta.exists()
            기다리기(Připravit_soket, 'QEMU soket_HODNOTA')
            직렬.connect(str(직렬경로))
            monitor_HODNOTA.connect(str(monitor_cesta))
            직렬.setblocking(False)
            monitor_HODNOTA.sendall(b'cont\n')

            def deklarace(řetězec_HODNOTA, Spustit_2=0):
                Čtení, _, _ = select.select([직렬], [], [], 0.1)
                if Čtení:
                    data = 직렬.recv(65536)
                    if not data:
                        raise AssertionError('직렬 Připojit Konec_program')
                    LOGZ_ZÁZNAM.extend(data)
                if Proces_HODNOTA.poll() is not None:
                    raise AssertionError('QEMU 비정상 Konec_program: ' + str(Proces_HODNOTA.returncode))
                return řetězec_HODNOTA.encode('utf-8') in LOGZ_ZÁZNAM[Spustit_2:]

            def 명령시험(vstup_HODNOTA, 기대):
                Spustit_2 = len(LOGZ_ZÁZNAM)
                직렬.sendall(vstup_HODNOTA.encode('ascii'))
                기다리기(lambda: deklarace(기대, Spustit_2), 기대)
                기다리기(lambda: deklarace('jkoros> ', Spustit_2), 'příkaz 후 프롬프트')

            기다리기(lambda: deklarace('READY'), Druh_HODNOTA + ' spuštění_stroje')
            assert b'JAVA SELFTEST PASS' in LOGZ_ZÁZNAM
            assert '자바 기계어 jádro_HODNOTA Spustit_2'.encode() in LOGZ_ZÁZNAM
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for INDEX in range(8):
                명령시험('alloc\n', 'oddíl_HODNOTA_366e0bfa INDEX: ' + str(INDEX))
            명령시험('alloc\n', 'oddíl_HODNOTA_366e0bfa INDEX: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 oddíl_HODNOTA_366e0bfa')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'oddíl_HODNOTA_366e0bfa INDEX: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 číslo 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Spustit_2 = len(LOGZ_ZÁZNAM)
            for Klíč_HODNOTA in ('i', 'n', 'f', 'o', 'ret'):
                monitor_HODNOTA.sendall(('sendkey ' + Klíč_HODNOTA + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: deklarace('embedded subset JVM / polling kernel', Spustit_2), 'PS/2 info vstup_HODNOTA')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: deklarace('HALTED'), '정지 příkaz')
            assert b'PANIC' not in LOGZ_ZÁZNAM and b'SELFTEST FAIL' not in LOGZ_ZÁZNAM
            print('PASS: {} spuštění_stroje, Java vlastní zkoušky, 직렬 příkaz, PS/2 vstup_HODNOTA, přidělit_Storage/Vratka_KV, 정지'.format(Druh_HODNOTA))
            return LOGZ_ZÁZNAM.decode('utf-8', 'replace')
        finally:
            직렬.close()
            monitor_HODNOTA.close()
            Proces_HODNOTA.terminate()
            try:
                Proces_HODNOTA.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Proces_HODNOTA.kill()
                Proces_HODNOTA.wait()


if __name__ == '__main__':
    VÝSLEDEK = {Druh_HODNOTA: zkoušky(Druh_HODNOTA) for Druh_HODNOTA in ('elf', 'iso')}
    (pozice / 'build/부팅시험.json').write_text(json.dumps(VÝSLEDEK, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
