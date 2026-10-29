#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

Позиција = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        мерка = 검사()
        if мерка:
            return мерка
        time.sleep(0.05)
    raise AssertionError('TIME_VALUE 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        монитор_патека = 임시 / 'monitor.sock'
        Команда = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(монитор_патека) + ',server,nowait']
        Команда += ['-kernel', str(Позиција / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(Позиција / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        Команда += ['-S']
        Процес_VALUE = subprocess.Popen(Команда, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        монитор_VALUE = socket.socket(socket.AF_UNIX)
        LOG_ред = bytearray()
        try:
            def 소켓준비():
                if Процес_VALUE.poll() is not None:
                    raise AssertionError(Процес_VALUE.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and монитор_патека.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            монитор_VALUE.connect(str(монитор_патека))
            직렬.setblocking(False)
            монитор_VALUE.sendall(b'cont\n')

            def 포함(низа_VALUE_6ca8363c, Изврши_2=0):
                Читај, _, _ = select.select([직렬], [], [], 0.1)
                if Читај:
                    податоци = 직렬.recv(65536)
                    if not податоци:
                        raise AssertionError('직렬 Врзи_се Излез_програма')
                    LOG_ред.extend(податоци)
                if Процес_VALUE.poll() is not None:
                    raise AssertionError('QEMU 비정상 Излез_програма: ' + str(Процес_VALUE.returncode))
                return низа_VALUE_6ca8363c.encode('utf-8') in LOG_ред[Изврши_2:]

            def 명령시험(입력, 기대):
                Изврши_2 = len(LOG_ред)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, Изврши_2), 기대)
                기다리기(lambda: 포함('jkoros> ', Изврши_2), 'Команда 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in LOG_ред
            assert '자바 기계어 јадро_VALUE Изврши_2'.encode() in LOG_ред
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for INDEX in range(8):
                명령시험('alloc\n', 'секција_VALUE INDEX: ' + str(INDEX))
            명령시험('alloc\n', 'секција_VALUE INDEX: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 секција_VALUE')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'секција_VALUE INDEX: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Изврши_2 = len(LOG_ред)
            for Клуч_VALUE in ('i', 'n', 'f', 'o', 'ret'):
                монитор_VALUE.sendall(('sendkey ' + Клуч_VALUE + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', Изврши_2), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 Команда')
            assert b'PANIC' not in LOG_ред and b'SELFTEST FAIL' not in LOG_ред
            print('PASS: {} 부팅, Java 자체 시험, 직렬 Команда, PS/2 입력, додели_Склад/반환, 정지'.format(종류))
            return LOG_ред.decode('utf-8', 'replace')
        finally:
            직렬.close()
            монитор_VALUE.close()
            Процес_VALUE.terminate()
            try:
                Процес_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Процес_VALUE.kill()
                Процес_VALUE.wait()


if __name__ == '__main__':
    мерка = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (Позиција / 'build/부팅시험.json').write_text(json.dumps(мерка, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
