#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

Турган_жери = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        결과 = 검사()
        if 결과:
            return 결과
        time.sleep(0.05)
    raise AssertionError('시간 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        монитор_жол = 임시 / 'monitor.sock'
        Команда = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(монитор_жол) + ',server,nowait']
        Команда += ['-kernel', str(Турган_жери / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(Турган_жери / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        Команда += ['-S']
        Процесс_маани = subprocess.Popen(Команда, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        монитор_маани = socket.socket(socket.AF_UNIX)
        жазуу_катар = bytearray()
        try:
            def 소켓준비():
                if Процесс_маани.poll() is not None:
                    raise AssertionError(Процесс_маани.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and монитор_жол.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            монитор_маани.connect(str(монитор_жол))
            직렬.setblocking(False)
            монитор_маани.sendall(b'cont\n')

            def 포함(сап_маани, Жүргүзүү=0):
                Окуу, _, _ = select.select([직렬], [], [], 0.1)
                if Окуу:
                    берилмелер = 직렬.recv(65536)
                    if not берилмелер:
                        raise AssertionError('직렬 Туташуу Чыгуу_програм')
                    жазуу_катар.extend(берилмелер)
                if Процесс_маани.poll() is not None:
                    raise AssertionError('QEMU 비정상 Чыгуу_програм: ' + str(Процесс_маани.returncode))
                return сап_маани.encode('utf-8') in жазуу_катар[Жүргүзүү:]

            def 명령시험(입력, 기대):
                Жүргүзүү = len(жазуу_катар)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, Жүргүзүү), 기대)
                기다리기(lambda: 포함('jkoros> ', Жүргүзүү), 'Команда 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in жазуу_катар
            assert '자바 기계어 өзөк_маани Жүргүзүү'.encode() in жазуу_катар
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for индекс in range(8):
                명령시험('alloc\n', 'бөлүк_маани_366e0bfa индекс: ' + str(индекс))
            명령시험('alloc\n', 'бөлүк_маани_366e0bfa индекс: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 бөлүк_маани_366e0bfa')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'бөлүк_маани_366e0bfa индекс: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Жүргүзүү = len(жазуу_катар)
            for ачкыч_маани in ('i', 'n', 'f', 'o', 'ret'):
                монитор_маани.sendall(('sendkey ' + ачкыч_маани + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', Жүргүзүү), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 Команда')
            assert b'PANIC' not in жазуу_катар and b'SELFTEST FAIL' not in жазуу_катар
            print('PASS: {} 부팅, Java 자체 시험, 직렬 Команда, PS/2 입력, энчилөө_сактагыч/반환, 정지'.format(종류))
            return жазуу_катар.decode('utf-8', 'replace')
        finally:
            직렬.close()
            монитор_маани.close()
            Процесс_маани.terminate()
            try:
                Процесс_маани.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Процесс_маани.kill()
                Процесс_маани.wait()


if __name__ == '__main__':
    결과 = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (Турган_жери / 'build/부팅시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
