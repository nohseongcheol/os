#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

இடம் = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        அளவிடக்கூடியது = 검사()
        if அளவிடக்கூடியது:
            return அளவிடக்கூடியது
        time.sleep(0.05)
    raise AssertionError('நேர_மதிப்பு 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        திரையகம்_பாதை = 임시 / 'monitor.sock'
        கட்டளை = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(திரையகம்_பாதை) + ',server,nowait']
        கட்டளை += ['-kernel', str(இடம் / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(இடம் / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        கட்டளை += ['-S']
        செயலகம்_மதிப்பு = subprocess.Popen(கட்டளை, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        திரையகம்_மதிப்பு = socket.socket(socket.AF_UNIX)
        பதிவு_பதிவு = bytearray()
        try:
            def 소켓준비():
                if செயலகம்_மதிப்பு.poll() is not None:
                    raise AssertionError(செயலகம்_மதிப்பு.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and திரையகம்_பாதை.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            திரையகம்_மதிப்பு.connect(str(திரையகம்_பாதை))
            직렬.setblocking(False)
            திரையகம்_மதிப்பு.sendall(b'cont\n')

            def 포함(சரம்_மதிப்பு, செயல்படுத்துக=0):
                படி, _, _ = select.select([직렬], [], [], 0.1)
                if படி:
                    தரவு = 직렬.recv(65536)
                    if not தரவு:
                        raise AssertionError('직렬 இணைக்க முடிவு_நிரல்')
                    பதிவு_பதிவு.extend(தரவு)
                if செயலகம்_மதிப்பு.poll() is not None:
                    raise AssertionError('QEMU 비정상 முடிவு_நிரல்: ' + str(செயலகம்_மதிப்பு.returncode))
                return சரம்_மதிப்பு.encode('utf-8') in பதிவு_பதிவு[செயல்படுத்துக:]

            def 명령시험(입력, 기대):
                செயல்படுத்துக = len(பதிவு_பதிவு)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, செயல்படுத்துக), 기대)
                기다리기(lambda: 포함('jkoros> ', செயல்படுத்துக), 'கட்டளை 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in பதிவு_பதிவு
            assert '자바 기계어 கரு_மதிப்பு செயல்படுத்துக'.encode() in பதிவு_பதிவு
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for அடைவு in range(8):
                명령시험('alloc\n', 'பிரிவு_மதிப்பு அடைவு: ' + str(அடைவு))
            명령시험('alloc\n', 'பிரிவு_மதிப்பு அடைவு: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 பிரிவு_மதிப்பு')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'பிரிவு_மதிப்பு அடைவு: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            செயல்படுத்துக = len(பதிவு_பதிவு)
            for சாவி_மதிப்பு in ('i', 'n', 'f', 'o', 'ret'):
                திரையகம்_மதிப்பு.sendall(('sendkey ' + சாவி_மதிப்பு + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', செயல்படுத்துக), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 கட்டளை')
            assert b'PANIC' not in பதிவு_பதிவு and b'SELFTEST FAIL' not in பதிவு_பதிவு
            print('PASS: {} 부팅, Java 자체 시험, 직렬 கட்டளை, PS/2 입력, ஒதுக்கிடு_சேமிப்பகம்/반환, 정지'.format(종류))
            return பதிவு_பதிவு.decode('utf-8', 'replace')
        finally:
            직렬.close()
            திரையகம்_மதிப்பு.close()
            செயலகம்_மதிப்பு.terminate()
            try:
                செயலகம்_மதிப்பு.wait(timeout=3)
            except subprocess.TimeoutExpired:
                செயலகம்_மதிப்பு.kill()
                செயலகம்_மதிப்பு.wait()


if __name__ == '__main__':
    அளவிடக்கூடியது = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (இடம் / 'build/부팅시험.json').write_text(json.dumps(அளவிடக்கூடியது, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
