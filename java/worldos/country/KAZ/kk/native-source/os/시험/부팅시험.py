#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

Орны = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        НӘТИЖЕ = 검사()
        if НӘТИЖЕ:
            return НӘТИЖЕ
        time.sleep(0.05)
    raise AssertionError('уақыт_мән 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        бақылау_жол = 임시 / 'monitor.sock'
        Команда = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(бақылау_жол) + ',server,nowait']
        Команда += ['-kernel', str(Орны / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(Орны / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        Команда += ['-S']
        Процесс_мән = subprocess.Popen(Команда, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        бақылау_мән = socket.socket(socket.AF_UNIX)
        журнал_жол = bytearray()
        try:
            def 소켓준비():
                if Процесс_мән.poll() is not None:
                    raise AssertionError(Процесс_мән.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and бақылау_жол.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            бақылау_мән.connect(str(бақылау_жол))
            직렬.setblocking(False)
            бақылау_мән.sendall(b'cont\n')

            def 포함(жол_мән_6ca8363c, Орындау_2=0):
                Оқу, _, _ = select.select([직렬], [], [], 0.1)
                if Оқу:
                    деректер = 직렬.recv(65536)
                    if not деректер:
                        raise AssertionError('직렬 Байланысу Шығу_бағдарлама')
                    журнал_жол.extend(деректер)
                if Процесс_мән.poll() is not None:
                    raise AssertionError('QEMU 비정상 Шығу_бағдарлама: ' + str(Процесс_мән.returncode))
                return жол_мән_6ca8363c.encode('utf-8') in журнал_жол[Орындау_2:]

            def 명령시험(입력, 기대):
                Орындау_2 = len(журнал_жол)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, Орындау_2), 기대)
                기다리기(lambda: 포함('jkoros> ', Орындау_2), 'Команда 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in журнал_жол
            assert '자바 기계어 ядро_мән Орындау_2'.encode() in журнал_жол
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for индекс in range(8):
                명령시험('alloc\n', 'бөлім_мән_366e0bfa индекс: ' + str(индекс))
            명령시험('alloc\n', 'бөлім_мән_366e0bfa индекс: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 бөлім_мән_366e0bfa')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'бөлім_мән_366e0bfa индекс: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Орындау_2 = len(журнал_жол)
            for Кілт_мән in ('i', 'n', 'f', 'o', 'ret'):
                бақылау_мән.sendall(('sendkey ' + Кілт_мән + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', Орындау_2), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 Команда')
            assert b'PANIC' not in журнал_жол and b'SELFTEST FAIL' not in журнал_жол
            print('PASS: {} 부팅, Java 자체 시험, 직렬 Команда, PS/2 입력, бекіту_Жад/қайтару_өлшем, 정지'.format(종류))
            return журнал_жол.decode('utf-8', 'replace')
        finally:
            직렬.close()
            бақылау_мән.close()
            Процесс_мән.terminate()
            try:
                Процесс_мән.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Процесс_мән.kill()
                Процесс_мән.wait()


if __name__ == '__main__':
    НӘТИЖЕ = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (Орны / 'build/부팅시험.json').write_text(json.dumps(НӘТИЖЕ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
