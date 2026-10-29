#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

Позиция = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        РЕЗУЛТАТ = 검사()
        if РЕЗУЛТАТ:
            return РЕЗУЛТАТ
        time.sleep(0.05)
    raise AssertionError('час_стойност 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        монитор_път = 임시 / 'monitor.sock'
        Команда = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(монитор_път) + ',server,nowait']
        Команда += ['-kernel', str(Позиция / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(Позиция / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        Команда += ['-S']
        Процес_стойност = subprocess.Popen(Команда, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        монитор_стойност = socket.socket(socket.AF_UNIX)
        регистрирам_запис = bytearray()
        try:
            def 소켓준비():
                if Процес_стойност.poll() is not None:
                    raise AssertionError(Процес_стойност.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and монитор_път.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            монитор_стойност.connect(str(монитор_път))
            직렬.setblocking(False)
            монитор_стойност.sendall(b'cont\n')

            def 포함(низ_стойност, Стартиране=0):
                Четене, _, _ = select.select([직렬], [], [], 0.1)
                if Четене:
                    данни = 직렬.recv(65536)
                    if not данни:
                        raise AssertionError('직렬 Свързване Изход_програма')
                    регистрирам_запис.extend(данни)
                if Процес_стойност.poll() is not None:
                    raise AssertionError('QEMU 비정상 Изход_програма: ' + str(Процес_стойност.returncode))
                return низ_стойност.encode('utf-8') in регистрирам_запис[Стартиране:]

            def 명령시험(입력, 기대):
                Стартиране = len(регистрирам_запис)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, Стартиране), 기대)
                기다리기(lambda: 포함('jkoros> ', Стартиране), 'Команда 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in регистрирам_запис
            assert '자바 기계어 ядро_стойност Стартиране'.encode() in регистрирам_запис
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for индекс in range(8):
                명령시험('alloc\n', 'раздел_стойност индекс: ' + str(индекс))
            명령시험('alloc\n', 'раздел_стойност индекс: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 раздел_стойност')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'раздел_стойност индекс: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Стартиране = len(регистрирам_запис)
            for Ключ_стойност in ('i', 'n', 'f', 'o', 'ret'):
                монитор_стойност.sendall(('sendkey ' + Ключ_стойност + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', Стартиране), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 Команда')
            assert b'PANIC' not in регистрирам_запис and b'SELFTEST FAIL' not in регистрирам_запис
            print('PASS: {} 부팅, Java 자체 시험, 직렬 Команда, PS/2 입력, заделям_Памет/връщам_мярка, 정지'.format(종류))
            return регистрирам_запис.decode('utf-8', 'replace')
        finally:
            직렬.close()
            монитор_стойност.close()
            Процес_стойност.terminate()
            try:
                Процес_стойност.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Процес_стойност.kill()
                Процес_стойност.wait()


if __name__ == '__main__':
    РЕЗУЛТАТ = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (Позиция / 'build/부팅시험.json').write_text(json.dumps(РЕЗУЛТАТ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
