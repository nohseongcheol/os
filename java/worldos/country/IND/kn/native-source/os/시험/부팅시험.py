#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

ಸ್ಥಾನ = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        ಮಾಪನ = 검사()
        if ಮಾಪನ:
            return ಮಾಪನ
        time.sleep(0.05)
    raise AssertionError('ಸಮಯ_ಮೌಲ್ಯ 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        ಮಾನಿಟರ್_ಹಾದಿ = 임시 / 'monitor.sock'
        ಆಜ್ಞೆ = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(ಮಾನಿಟರ್_ಹಾದಿ) + ',server,nowait']
        ಆಜ್ಞೆ += ['-kernel', str(ಸ್ಥಾನ / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(ಸ್ಥಾನ / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        ಆಜ್ಞೆ += ['-S']
        ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ = subprocess.Popen(ಆಜ್ಞೆ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        ಮಾನಿಟರ್_ಮೌಲ್ಯ = socket.socket(socket.AF_UNIX)
        ಲಾಗ್_ದಾಖಲೆ = bytearray()
        try:
            def 소켓준비():
                if ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.poll() is not None:
                    raise AssertionError(ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and ಮಾನಿಟರ್_ಹಾದಿ.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            ಮಾನಿಟರ್_ಮೌಲ್ಯ.connect(str(ಮಾನಿಟರ್_ಹಾದಿ))
            직렬.setblocking(False)
            ಮಾನಿಟರ್_ಮೌಲ್ಯ.sendall(b'cont\n')

            def 포함(ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ, ಚಲಾಯಿಸು_2=0):
                ಓದು, _, _ = select.select([직렬], [], [], 0.1)
                if ಓದು:
                    ಡೇಟಾ = 직렬.recv(65536)
                    if not ಡೇಟಾ:
                        raise AssertionError('직렬 ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು ನಿರ್ಗಮನ_ಅಪ್ಲಿ')
                    ಲಾಗ್_ದಾಖಲೆ.extend(ಡೇಟಾ)
                if ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.poll() is not None:
                    raise AssertionError('QEMU 비정상 ನಿರ್ಗಮನ_ಅಪ್ಲಿ: ' + str(ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.returncode))
                return ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ.encode('utf-8') in ಲಾಗ್_ದಾಖಲೆ[ಚಲಾಯಿಸು_2:]

            def 명령시험(입력, 기대):
                ಚಲಾಯಿಸು_2 = len(ಲಾಗ್_ದಾಖಲೆ)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, ಚಲಾಯಿಸು_2), 기대)
                기다리기(lambda: 포함('jkoros> ', ಚಲಾಯಿಸು_2), 'ಆಜ್ಞೆ 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in ಲಾಗ್_ದಾಖಲೆ
            assert '자바 기계어 ಕರ್ನಲ್_ಮೌಲ್ಯ ಚಲಾಯಿಸು_2'.encode() in ಲಾಗ್_ದಾಖಲೆ
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for ಪದಸೂಚಿ in range(8):
                명령시험('alloc\n', 'ವಿಭಾಗ_ಮೌಲ್ಯ ಪದಸೂಚಿ: ' + str(ಪದಸೂಚಿ))
            명령시험('alloc\n', 'ವಿಭಾಗ_ಮೌಲ್ಯ ಪದಸೂಚಿ: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 ವಿಭಾಗ_ಮೌಲ್ಯ')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'ವಿಭಾಗ_ಮೌಲ್ಯ ಪದಸೂಚಿ: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            ಚಲಾಯಿಸು_2 = len(ಲಾಗ್_ದಾಖಲೆ)
            for ಕೀ_ಮೌಲ್ಯ in ('i', 'n', 'f', 'o', 'ret'):
                ಮಾನಿಟರ್_ಮೌಲ್ಯ.sendall(('sendkey ' + ಕೀ_ಮೌಲ್ಯ + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', ಚಲಾಯಿಸು_2), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 ಆಜ್ಞೆ')
            assert b'PANIC' not in ಲಾಗ್_ದಾಖಲೆ and b'SELFTEST FAIL' not in ಲಾಗ್_ದಾಖಲೆ
            print('PASS: {} 부팅, Java 자체 시험, 직렬 ಆಜ್ಞೆ, PS/2 입력, ವಿತರಿಸು_ಸಂಗ್ರಹ/반환, 정지'.format(종류))
            return ಲಾಗ್_ದಾಖಲೆ.decode('utf-8', 'replace')
        finally:
            직렬.close()
            ಮಾನಿಟರ್_ಮೌಲ್ಯ.close()
            ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.terminate()
            try:
                ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.wait(timeout=3)
            except subprocess.TimeoutExpired:
                ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.kill()
                ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.wait()


if __name__ == '__main__':
    ಮಾಪನ = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (ಸ್ಥಾನ / 'build/부팅시험.json').write_text(json.dumps(ಮಾಪನ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
