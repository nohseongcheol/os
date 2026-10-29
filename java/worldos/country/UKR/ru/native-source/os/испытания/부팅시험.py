#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

позиция = Path(__file__).resolve().parents[1]


def 기다리기(검사, описание, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        результат = 검사()
        if результат:
            return результат
        time.sleep(0.05)
    raise AssertionError('значение_времени 초과: ' + описание)


def испытания(Вид_ЗНАЧЕН):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        монитор_путь = 임시 / 'monitor.sock'
        команда = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(монитор_путь) + ',server,nowait']
        команда += ['-kernel', str(позиция / 'build/kernel.elf')] if Вид_ЗНАЧЕН == 'elf' else [
            '-cdrom', str(позиция / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        команда += ['-S']
        Процесс_ЗНАЧЕН = subprocess.Popen(команда, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        монитор_ЗНАЧЕН = socket.socket(socket.AF_UNIX)
        LOG_ЗАПИСЬ = bytearray()
        try:
            def Подготовить_сокет():
                if Процесс_ЗНАЧЕН.poll() is not None:
                    raise AssertionError(Процесс_ЗНАЧЕН.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and монитор_путь.exists()
            기다리기(Подготовить_сокет, 'QEMU сокет_ЗНАЧЕН')
            직렬.connect(str(직렬경로))
            монитор_ЗНАЧЕН.connect(str(монитор_путь))
            직렬.setblocking(False)
            монитор_ЗНАЧЕН.sendall(b'cont\n')

            def объявления(строка_ЗНАЧЕН, запустить=0):
                Чтение, _, _ = select.select([직렬], [], [], 0.1)
                if Чтение:
                    данные = 직렬.recv(65536)
                    if not данные:
                        raise AssertionError('직렬 Подключить Выход_программа')
                    LOG_ЗАПИСЬ.extend(данные)
                if Процесс_ЗНАЧЕН.poll() is not None:
                    raise AssertionError('QEMU 비정상 Выход_программа: ' + str(Процесс_ЗНАЧЕН.returncode))
                return строка_ЗНАЧЕН.encode('utf-8') in LOG_ЗАПИСЬ[запустить:]

            def 명령시험(входные_данные_ЗНАЧЕН, 기대):
                запустить = len(LOG_ЗАПИСЬ)
                직렬.sendall(входные_данные_ЗНАЧЕН.encode('ascii'))
                기다리기(lambda: объявления(기대, запустить), 기대)
                기다리기(lambda: объявления('jkoros> ', запустить), 'команда 후 프롬프트')

            기다리기(lambda: объявления('READY'), Вид_ЗНАЧЕН + ' запуск_машины')
            assert b'JAVA SELFTEST PASS' in LOG_ЗАПИСЬ
            assert '자바 기계어 ядро_ЗНАЧЕН запустить'.encode() in LOG_ЗАПИСЬ
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for ИНДЕКС in range(8):
                명령시험('alloc\n', 'раздел_ЗНАЧЕН_366e0bfa ИНДЕКС: ' + str(ИНДЕКС))
            명령시험('alloc\n', 'раздел_ЗНАЧЕН_366e0bfa ИНДЕКС: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 раздел_ЗНАЧЕН_366e0bfa')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'раздел_ЗНАЧЕН_366e0bfa ИНДЕКС: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            запустить = len(LOG_ЗАПИСЬ)
            for Ключ_ЗНАЧЕН in ('i', 'n', 'f', 'o', 'ret'):
                монитор_ЗНАЧЕН.sendall(('sendkey ' + Ключ_ЗНАЧЕН + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: объявления('embedded subset JVM / polling kernel', запустить), 'PS/2 info входные_данные_ЗНАЧЕН')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: объявления('HALTED'), '정지 команда')
            assert b'PANIC' not in LOG_ЗАПИСЬ and b'SELFTEST FAIL' not in LOG_ЗАПИСЬ
            print('PASS: {} запуск_машины, Java свой испытания, 직렬 команда, PS/2 входные_данные_ЗНАЧЕН, выделить_Память/Возврат_KR, 정지'.format(Вид_ЗНАЧЕН))
            return LOG_ЗАПИСЬ.decode('utf-8', 'replace')
        finally:
            직렬.close()
            монитор_ЗНАЧЕН.close()
            Процесс_ЗНАЧЕН.terminate()
            try:
                Процесс_ЗНАЧЕН.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Процесс_ЗНАЧЕН.kill()
                Процесс_ЗНАЧЕН.wait()


if __name__ == '__main__':
    результат = {Вид_ЗНАЧЕН: испытания(Вид_ЗНАЧЕН) for Вид_ЗНАЧЕН in ('elf', 'iso')}
    (позиция / 'build/부팅시험.json').write_text(json.dumps(результат, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
