#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

Pozíció = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        KR = 검사()
        if KR:
            return KR
        time.sleep(0.05)
    raise AssertionError('IDŐ_ÉRTÉK 초과: ' + 설명)


def 시험(Altípus_ÉRTÉK):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        figyelő_útvonal = 임시 / 'monitor.sock'
        Parancs = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(figyelő_útvonal) + ',server,nowait']
        Parancs += ['-kernel', str(Pozíció / 'build/kernel.elf')] if Altípus_ÉRTÉK == 'elf' else [
            '-cdrom', str(Pozíció / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        Parancs += ['-S']
        folyamat_ÉRTÉK = subprocess.Popen(Parancs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        figyelő_ÉRTÉK = socket.socket(socket.AF_UNIX)
        LOG_REKORD = bytearray()
        try:
            def Előkészítés_szoftvercsatorna():
                if folyamat_ÉRTÉK.poll() is not None:
                    raise AssertionError(folyamat_ÉRTÉK.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and figyelő_útvonal.exists()
            기다리기(Előkészítés_szoftvercsatorna, 'QEMU szoftvercsatorna_ÉRTÉK')
            직렬.connect(str(직렬경로))
            figyelő_ÉRTÉK.connect(str(figyelő_útvonal))
            직렬.setblocking(False)
            figyelő_ÉRTÉK.sendall(b'cont\n')

            def 포함(sztring_ÉRTÉK, Futtatás=0):
                Olvasás, _, _ = select.select([직렬], [], [], 0.1)
                if Olvasás:
                    adat = 직렬.recv(65536)
                    if not adat:
                        raise AssertionError('직렬 Kapcsolódás kilép_app')
                    LOG_REKORD.extend(adat)
                if folyamat_ÉRTÉK.poll() is not None:
                    raise AssertionError('QEMU 비정상 kilép_app: ' + str(folyamat_ÉRTÉK.returncode))
                return sztring_ÉRTÉK.encode('utf-8') in LOG_REKORD[Futtatás:]

            def 명령시험(bevitel_ÉRTÉK, 기대):
                Futtatás = len(LOG_REKORD)
                직렬.sendall(bevitel_ÉRTÉK.encode('ascii'))
                기다리기(lambda: 포함(기대, Futtatás), 기대)
                기다리기(lambda: 포함('jkoros> ', Futtatás), 'Parancs 후 프롬프트')

            기다리기(lambda: 포함('READY'), Altípus_ÉRTÉK + ' 부팅')
            assert b'JAVA SELFTEST PASS' in LOG_REKORD
            assert '자바 기계어 kernel_ÉRTÉK Futtatás'.encode() in LOG_REKORD
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for INDEX in range(8):
                명령시험('alloc\n', 'szakasz_ÉRTÉK INDEX: ' + str(INDEX))
            명령시험('alloc\n', 'szakasz_ÉRTÉK INDEX: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 szakasz_ÉRTÉK')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'szakasz_ÉRTÉK INDEX: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 szám 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Futtatás = len(LOG_REKORD)
            for Kulcs_ÉRTÉK in ('i', 'n', 'f', 'o', 'ret'):
                figyelő_ÉRTÉK.sendall(('sendkey ' + Kulcs_ÉRTÉK + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', Futtatás), 'PS/2 info bevitel_ÉRTÉK')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 Parancs')
            assert b'PANIC' not in LOG_REKORD and b'SELFTEST FAIL' not in LOG_REKORD
            print('PASS: {} 부팅, Java saját 시험, 직렬 Parancs, PS/2 bevitel_ÉRTÉK, kioszt_tár/visszaküld_KR, 정지'.format(Altípus_ÉRTÉK))
            return LOG_REKORD.decode('utf-8', 'replace')
        finally:
            직렬.close()
            figyelő_ÉRTÉK.close()
            folyamat_ÉRTÉK.terminate()
            try:
                folyamat_ÉRTÉK.wait(timeout=3)
            except subprocess.TimeoutExpired:
                folyamat_ÉRTÉK.kill()
                folyamat_ÉRTÉK.wait()


if __name__ == '__main__':
    KR = {Altípus_ÉRTÉK: 시험(Altípus_ÉRTÉK) for Altípus_ÉRTÉK in ('elf', 'iso')}
    (Pozíció / 'build/부팅시험.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
