#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

ئورۇن = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        ئۆلچەم = 검사()
        if ئۆلچەم:
            return ئۆلچەم
        time.sleep(0.05)
    raise AssertionError('시간 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        كۆرسەتكۈچ_يول = 임시 / 'monitor.sock'
        بۇيرۇق = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(كۆرسەتكۈچ_يول) + ',server,nowait']
        بۇيرۇق += ['-kernel', str(ئورۇن / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(ئورۇن / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        بۇيرۇق += ['-S']
        جەريان_قىممىتى = subprocess.Popen(بۇيرۇق, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        كۆرسەتكۈچ_قىممىتى = socket.socket(socket.AF_UNIX)
        خاتىرە_قۇر = bytearray()
        try:
            def 소켓준비():
                if جەريان_قىممىتى.poll() is not None:
                    raise AssertionError(جەريان_قىممىتى.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and كۆرسەتكۈچ_يول.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            كۆرسەتكۈچ_قىممىتى.connect(str(كۆرسەتكۈچ_يول))
            직렬.setblocking(False)
            كۆرسەتكۈچ_قىممىتى.sendall(b'cont\n')

            def 포함(ھەرپ_تىزمىسى_قىممىتى, ئىجرا_قىل_2=0):
                ئوقۇ, _, _ = select.select([직렬], [], [], 0.1)
                if ئوقۇ:
                    مەلۇمات = 직렬.recv(65536)
                    if not مەلۇمات:
                        raise AssertionError('직렬 ئۇلا چىقىش_ئەپ')
                    خاتىرە_قۇر.extend(مەلۇمات)
                if جەريان_قىممىتى.poll() is not None:
                    raise AssertionError('QEMU 비정상 چىقىش_ئەپ: ' + str(جەريان_قىممىتى.returncode))
                return ھەرپ_تىزمىسى_قىممىتى.encode('utf-8') in خاتىرە_قۇر[ئىجرا_قىل_2:]

            def 명령시험(입력, 기대):
                ئىجرا_قىل_2 = len(خاتىرە_قۇر)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, ئىجرا_قىل_2), 기대)
                기다리기(lambda: 포함('jkoros> ', ئىجرا_قىل_2), 'بۇيرۇق 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in خاتىرە_قۇر
            assert '자바 기계어 يادرو_قىممىتى ئىجرا_قىل_2'.encode() in خاتىرە_قۇر
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for ئىندېكس in range(8):
                명령시험('alloc\n', 'بۆلۈم_قىممىتى ئىندېكس: ' + str(ئىندېكس))
            명령시험('alloc\n', 'بۆلۈم_قىممىتى ئىندېكس: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 بۆلۈم_قىممىتى')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'بۆلۈم_قىممىتى ئىندېكس: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            ئىجرا_قىل_2 = len(خاتىرە_قۇر)
            for ئاچقۇچ_قىممىتى in ('i', 'n', 'f', 'o', 'ret'):
                كۆرسەتكۈچ_قىممىتى.sendall(('sendkey ' + ئاچقۇچ_قىممىتى + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', ئىجرا_قىل_2), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 بۇيرۇق')
            assert b'PANIC' not in خاتىرە_قۇر and b'SELFTEST FAIL' not in خاتىرە_قۇر
            print('PASS: {} 부팅, Java 자체 시험, 직렬 بۇيرۇق, PS/2 입력, تەقسىملەش_بوشلۇق/قايتۇرۇپ_بېرىش_ئۆلچەم, 정지'.format(종류))
            return خاتىرە_قۇر.decode('utf-8', 'replace')
        finally:
            직렬.close()
            كۆرسەتكۈچ_قىممىتى.close()
            جەريان_قىممىتى.terminate()
            try:
                جەريان_قىممىتى.wait(timeout=3)
            except subprocess.TimeoutExpired:
                جەريان_قىممىتى.kill()
                جەريان_قىممىتى.wait()


if __name__ == '__main__':
    ئۆلچەم = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (ئورۇن / 'build/부팅시험.json').write_text(json.dumps(ئۆلچەم, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
