#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 seriale_VALORE/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

posizione = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        risultato = 검사()
        if risultato:
            return risultato
        time.sleep(0.05)
    raise AssertionError('valore 초과: ' + 설명)


def prove(Kind_VALORE):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        seriale_percorso = 임시 / 'serial.sock'
        monitor_percorso = 임시 / 'monitor.sock'
        comando = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(seriale_percorso) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_percorso) + ',server,nowait']
        comando += ['-kernel', str(posizione / 'build/kernel.elf')] if Kind_VALORE == 'elf' else [
            '-cdrom', str(posizione / 'build/kernel.iso'), '-boot', 'd']
        # seriale_VALORE 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        comando += ['-S']
        Processi_VALORE = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        seriale_VALORE = socket.socket(socket.AF_UNIX)
        monitor_VALORE = socket.socket(socket.AF_UNIX)
        LOG_riga = bytearray()
        try:
            def Prepara_socket():
                if Processi_VALORE.poll() is not None:
                    raise AssertionError(Processi_VALORE.stderr.read().decode('utf-8', 'replace'))
                return seriale_percorso.exists() and monitor_percorso.exists()
            기다리기(Prepara_socket, 'QEMU socket_VALORE')
            seriale_VALORE.connect(str(seriale_percorso))
            monitor_VALORE.connect(str(monitor_percorso))
            seriale_VALORE.setblocking(False)
            monitor_VALORE.sendall(b'cont\n')

            def dichiarazioni(stringa_VALORE, avvia=0):
                Lettura, _, _ = select.select([seriale_VALORE], [], [], 0.1)
                if Lettura:
                    dati = seriale_VALORE.recv(65536)
                    if not dati:
                        raise AssertionError('seriale_VALORE Connetti Esci_app')
                    LOG_riga.extend(dati)
                if Processi_VALORE.poll() is not None:
                    raise AssertionError('QEMU 비정상 Esci_app: ' + str(Processi_VALORE.returncode))
                return stringa_VALORE.encode('utf-8') in LOG_riga[avvia:]

            def 명령시험(input_VALORE, 기대):
                avvia = len(LOG_riga)
                seriale_VALORE.sendall(input_VALORE.encode('ascii'))
                기다리기(lambda: dichiarazioni(기대, avvia), 기대)
                기다리기(lambda: dichiarazioni('jkoros> ', avvia), 'comando 후 프롬프트')

            기다리기(lambda: dichiarazioni('READY'), Kind_VALORE + ' avvio_macchina')
            assert b'JAVA SELFTEST PASS' in LOG_riga
            assert '자바 기계어 kernel_VALORE avvia'.encode() in LOG_riga
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for INDICE in range(8):
                명령시험('alloc\n', 'sezione_VALORE INDICE: ' + str(INDICE))
            명령시험('alloc\n', 'sezione_VALORE INDICE: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 sezione_VALORE')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'sezione_VALORE INDICE: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 numero 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            avvia = len(LOG_riga)
            for tasto_VALORE in ('i', 'n', 'f', 'o', 'ret'):
                monitor_VALORE.sendall(('sendkey ' + tasto_VALORE + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: dichiarazioni('embedded subset JVM / polling kernel', avvia), 'PS/2 info input_VALORE')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            seriale_VALORE.sendall(b'halt\n')
            기다리기(lambda: dichiarazioni('HALTED'), '정지 comando')
            assert b'PANIC' not in LOG_riga and b'SELFTEST FAIL' not in LOG_riga
            print('PASS: {} avvio_macchina, Java nativo prove, seriale_VALORE comando, PS/2 input_VALORE, allocare_Memoria/Reso_KR, 정지'.format(Kind_VALORE))
            return LOG_riga.decode('utf-8', 'replace')
        finally:
            seriale_VALORE.close()
            monitor_VALORE.close()
            Processi_VALORE.terminate()
            try:
                Processi_VALORE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Processi_VALORE.kill()
                Processi_VALORE.wait()


if __name__ == '__main__':
    risultato = {Kind_VALORE: prove(Kind_VALORE) for Kind_VALORE in ('elf', 'iso')}
    (posizione / 'build/부팅시험.json').write_text(json.dumps(risultato, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
