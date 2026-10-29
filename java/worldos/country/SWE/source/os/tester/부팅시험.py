#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

position = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        RESULTAT = 검사()
        if RESULTAT:
            return RESULTAT
        time.sleep(0.05)
    raise AssertionError('tid_värde 초과: ' + 설명)


def tester(variant_värde):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        övervaka_väg = 임시 / 'monitor.sock'
        kommando = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(övervaka_väg) + ',server,nowait']
        kommando += ['-kernel', str(position / 'build/kernel.elf')] if variant_värde == 'elf' else [
            '-cdrom', str(position / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        kommando += ['-S']
        Process_värde = subprocess.Popen(kommando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        övervaka_värde = socket.socket(socket.AF_UNIX)
        LOG_POST = bytearray()
        try:
            def Förbereda_socket():
                if Process_värde.poll() is not None:
                    raise AssertionError(Process_värde.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and övervaka_väg.exists()
            기다리기(Förbereda_socket, 'QEMU socket_värde')
            직렬.connect(str(직렬경로))
            övervaka_värde.connect(str(övervaka_väg))
            직렬.setblocking(False)
            övervaka_värde.sendall(b'cont\n')

            def deklarationer(sträng_värde, Kör=0):
                Läs, _, _ = select.select([직렬], [], [], 0.1)
                if Läs:
                    data = 직렬.recv(65536)
                    if not data:
                        raise AssertionError('직렬 Anslut Utgång_app')
                    LOG_POST.extend(data)
                if Process_värde.poll() is not None:
                    raise AssertionError('QEMU 비정상 Utgång_app: ' + str(Process_värde.returncode))
                return sträng_värde.encode('utf-8') in LOG_POST[Kör:]

            def 명령시험(indata_värde, 기대):
                Kör = len(LOG_POST)
                직렬.sendall(indata_värde.encode('ascii'))
                기다리기(lambda: deklarationer(기대, Kör), 기대)
                기다리기(lambda: deklarationer('jkoros> ', Kör), 'kommando 후 프롬프트')

            기다리기(lambda: deklarationer('READY'), variant_värde + ' maskinstart')
            assert b'JAVA SELFTEST PASS' in LOG_POST
            assert '자바 기계어 kärna_värde Kör'.encode() in LOG_POST
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for INDEX in range(8):
                명령시험('alloc\n', 'avsnitt_värde INDEX: ' + str(INDEX))
            명령시험('alloc\n', 'avsnitt_värde INDEX: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 avsnitt_värde')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'avsnitt_värde INDEX: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 nummer 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Kör = len(LOG_POST)
            for Nyckel_värde in ('i', 'n', 'f', 'o', 'ret'):
                övervaka_värde.sendall(('sendkey ' + Nyckel_värde + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: deklarationer('embedded subset JVM / polling kernel', Kör), 'PS/2 info indata_värde')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: deklarationer('HALTED'), '정지 kommando')
            assert b'PANIC' not in LOG_POST and b'SELFTEST FAIL' not in LOG_POST
            print('PASS: {} maskinstart, Java eget tester, 직렬 kommando, PS/2 indata_värde, allokera_minne/Retur_KR, 정지'.format(variant_värde))
            return LOG_POST.decode('utf-8', 'replace')
        finally:
            직렬.close()
            övervaka_värde.close()
            Process_värde.terminate()
            try:
                Process_värde.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Process_värde.kill()
                Process_värde.wait()


if __name__ == '__main__':
    RESULTAT = {variant_värde: tester(variant_värde) for variant_värde in ('elf', 'iso')}
    (position / 'build/부팅시험.json').write_text(json.dumps(RESULTAT, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
