#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

Положај = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        ИСХОД = 검사()
        if ИСХОД:
            return ИСХОД
        time.sleep(0.05)
    raise AssertionError('време_вриједност 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        монитор_пут = 임시 / 'monitor.sock'
        Наредба = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(монитор_пут) + ',server,nowait']
        Наредба += ['-kernel', str(Положај / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(Положај / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        Наредба += ['-S']
        Процес_вриједност = subprocess.Popen(Наредба, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        монитор_вриједност = socket.socket(socket.AF_UNIX)
        евиденција_ред = bytearray()
        try:
            def 소켓준비():
                if Процес_вриједност.poll() is not None:
                    raise AssertionError(Процес_вриједност.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and монитор_пут.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            монитор_вриједност.connect(str(монитор_пут))
            직렬.setblocking(False)
            монитор_вриједност.sendall(b'cont\n')

            def 포함(ниска_вриједност, Покрени=0):
                Чита, _, _ = select.select([직렬], [], [], 0.1)
                if Чита:
                    подаци = 직렬.recv(65536)
                    if not подаци:
                        raise AssertionError('직렬 Повежи_се Излаз_програм')
                    евиденција_ред.extend(подаци)
                if Процес_вриједност.poll() is not None:
                    raise AssertionError('QEMU 비정상 Излаз_програм: ' + str(Процес_вриједност.returncode))
                return ниска_вриједност.encode('utf-8') in евиденција_ред[Покрени:]

            def 명령시험(입력, 기대):
                Покрени = len(евиденција_ред)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, Покрени), 기대)
                기다리기(lambda: 포함('jkoros> ', Покрени), 'Наредба 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in евиденција_ред
            assert '자바 기계어 језгро_вриједност Покрени'.encode() in евиденција_ред
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for индекс in range(8):
                명령시험('alloc\n', 'одељак_вриједност индекс: ' + str(индекс))
            명령시험('alloc\n', 'одељак_вриједност индекс: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 одељак_вриједност')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'одељак_вриједност индекс: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Покрени = len(евиденција_ред)
            for Кључ_вриједност in ('i', 'n', 'f', 'o', 'ret'):
                монитор_вриједност.sendall(('sendkey ' + Кључ_вриједност + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', Покрени), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 Наредба')
            assert b'PANIC' not in евиденција_ред and b'SELFTEST FAIL' not in евиденција_ред
            print('PASS: {} 부팅, Java 자체 시험, 직렬 Наредба, PS/2 입력, доделити_похрана/вратити_мера, 정지'.format(종류))
            return евиденција_ред.decode('utf-8', 'replace')
        finally:
            직렬.close()
            монитор_вриједност.close()
            Процес_вриједност.terminate()
            try:
                Процес_вриједност.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Процес_вриједност.kill()
                Процес_вриједност.wait()


if __name__ == '__main__':
    ИСХОД = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (Положај / 'build/부팅시험.json').write_text(json.dumps(ИСХОД, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
