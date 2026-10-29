#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

Пазіцыя = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        결과 = 검사()
        if 결과:
            return 결과
        time.sleep(0.05)
    raise AssertionError('час_значэнне 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        манітор_шлях = 임시 / 'monitor.sock'
        Загад = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(манітор_шлях) + ',server,nowait']
        Загад += ['-kernel', str(Пазіцыя / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(Пазіцыя / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        Загад += ['-S']
        Працэс_значэнне = subprocess.Popen(Загад, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        манітор_значэнне = socket.socket(socket.AF_UNIX)
        журнал_запіс = bytearray()
        try:
            def 소켓준비():
                if Працэс_значэнне.poll() is not None:
                    raise AssertionError(Працэс_значэнне.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and манітор_шлях.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            манітор_значэнне.connect(str(манітор_шлях))
            직렬.setblocking(False)
            манітор_значэнне.sendall(b'cont\n')

            def 포함(радок_значэнне, Выканаць=0):
                Чытанне, _, _ = select.select([직렬], [], [], 0.1)
                if Чытанне:
                    дадзеныя = 직렬.recv(65536)
                    if not дадзеныя:
                        raise AssertionError('직렬 Злучыцца Выхад_праграма')
                    журнал_запіс.extend(дадзеныя)
                if Працэс_значэнне.poll() is not None:
                    raise AssertionError('QEMU 비정상 Выхад_праграма: ' + str(Працэс_значэнне.returncode))
                return радок_значэнне.encode('utf-8') in журнал_запіс[Выканаць:]

            def 명령시험(입력, 기대):
                Выканаць = len(журнал_запіс)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, Выканаць), 기대)
                기다리기(lambda: 포함('jkoros> ', Выканаць), 'Загад 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in журнал_запіс
            assert '자바 기계어 ядро_значэнне Выканаць'.encode() in журнал_запіс
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for індэкс in range(8):
                명령시험('alloc\n', 'секцыя_значэнне індэкс: ' + str(індэкс))
            명령시험('alloc\n', 'секцыя_значэнне індэкс: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 секцыя_значэнне')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'секцыя_значэнне індэкс: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Выканаць = len(журнал_запіс)
            for клавіша_значэнне in ('i', 'n', 'f', 'o', 'ret'):
                манітор_значэнне.sendall(('sendkey ' + клавіша_значэнне + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', Выканаць), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 Загад')
            assert b'PANIC' not in журнал_запіс and b'SELFTEST FAIL' not in журнал_запіс
            print('PASS: {} 부팅, Java 자체 시험, 직렬 Загад, PS/2 입력, вылучыць_Сховішча/반환, 정지'.format(종류))
            return журнал_запіс.decode('utf-8', 'replace')
        finally:
            직렬.close()
            манітор_значэнне.close()
            Працэс_значэнне.terminate()
            try:
                Працэс_значэнне.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Працэс_значэнне.kill()
                Працэс_значэнне.wait()


if __name__ == '__main__':
    결과 = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (Пазіцыя / 'build/부팅시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
