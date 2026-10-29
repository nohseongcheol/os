#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

позиція = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        результат = 검사()
        if результат:
            return результат
        time.sleep(0.05)
    raise AssertionError('час_значення 초과: ' + 설명)


def випробування(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        монітор_шлях = 임시 / 'monitor.sock'
        команда = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(монітор_шлях) + ',server,nowait']
        команда += ['-kernel', str(позиція / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(позиція / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        команда += ['-S']
        процес_значення = subprocess.Popen(команда, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        монітор_значення = socket.socket(socket.AF_UNIX)
        журнал_запис = bytearray()
        try:
            def Готувати_сокет():
                if процес_значення.poll() is not None:
                    raise AssertionError(процес_значення.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and монітор_шлях.exists()
            기다리기(Готувати_сокет, 'QEMU сокет_значення')
            직렬.connect(str(직렬경로))
            монітор_значення.connect(str(монітор_шлях))
            직렬.setblocking(False)
            монітор_значення.sendall(b'cont\n')

            def оголошення(рядок_значення, запустити=0):
                Читання, _, _ = select.select([직렬], [], [], 0.1)
                if Читання:
                    дані = 직렬.recv(65536)
                    if not дані:
                        raise AssertionError('직렬 З_єднання Вийти_програма')
                    журнал_запис.extend(дані)
                if процес_значення.poll() is not None:
                    raise AssertionError('QEMU 비정상 Вийти_програма: ' + str(процес_значення.returncode))
                return рядок_значення.encode('utf-8') in журнал_запис[запустити:]

            def 명령시험(입력, 기대):
                запустити = len(журнал_запис)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: оголошення(기대, запустити), 기대)
                기다리기(lambda: оголошення('jkoros> ', запустити), 'команда 후 프롬프트')

            기다리기(lambda: оголошення('READY'), 종류 + ' запуск_машини')
            assert b'JAVA SELFTEST PASS' in журнал_запис
            assert '자바 기계어 ядро_значення запустити'.encode() in журнал_запис
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for індекс in range(8):
                명령시험('alloc\n', 'розділ_значення_366e0bfa індекс: ' + str(індекс))
            명령시험('alloc\n', 'розділ_значення_366e0bfa індекс: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 розділ_значення_366e0bfa')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'розділ_значення_366e0bfa індекс: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            запустити = len(журнал_запис)
            for Ключ_значення in ('i', 'n', 'f', 'o', 'ret'):
                монітор_значення.sendall(('sendkey ' + Ключ_значення + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: оголошення('embedded subset JVM / polling kernel', запустити), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: оголошення('HALTED'), '정지 команда')
            assert b'PANIC' not in журнал_запис and b'SELFTEST FAIL' not in журнал_запис
            print('PASS: {} запуск_машини, Java своє випробування, 직렬 команда, PS/2 입력, виділяти_місце/повернути_КР, 정지'.format(종류))
            return журнал_запис.decode('utf-8', 'replace')
        finally:
            직렬.close()
            монітор_значення.close()
            процес_значення.terminate()
            try:
                процес_значення.wait(timeout=3)
            except subprocess.TimeoutExpired:
                процес_значення.kill()
                процес_значення.wait()


if __name__ == '__main__':
    результат = {종류: випробування(종류) for 종류 in ('elf', 'iso')}
    (позиція / 'build/부팅시험.json').write_text(json.dumps(результат, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
