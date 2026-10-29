#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

ਸਥਿਤੀ = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        ਮਾਪ = 검사()
        if ਮਾਪ:
            return ਮਾਪ
        time.sleep(0.05)
    raise AssertionError('시간 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        ਮੌਨੀਟਰ_ਰਸਤਾ = 임시 / 'monitor.sock'
        ਕਮਾਂਡ = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(ਮੌਨੀਟਰ_ਰਸਤਾ) + ',server,nowait']
        ਕਮਾਂਡ += ['-kernel', str(ਸਥਿਤੀ / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(ਸਥਿਤੀ / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        ਕਮਾਂਡ += ['-S']
        ਕਾਰਵਾਈ_ਕੀਮਤ = subprocess.Popen(ਕਮਾਂਡ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        ਮੌਨੀਟਰ_ਕੀਮਤ = socket.socket(socket.AF_UNIX)
        ਲੌਗ_ਕਤਾਰ = bytearray()
        try:
            def 소켓준비():
                if ਕਾਰਵਾਈ_ਕੀਮਤ.poll() is not None:
                    raise AssertionError(ਕਾਰਵਾਈ_ਕੀਮਤ.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and ਮੌਨੀਟਰ_ਰਸਤਾ.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            ਮੌਨੀਟਰ_ਕੀਮਤ.connect(str(ਮੌਨੀਟਰ_ਰਸਤਾ))
            직렬.setblocking(False)
            ਮੌਨੀਟਰ_ਕੀਮਤ.sendall(b'cont\n')

            def 포함(ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ, ਚਲਾਓ_2=0):
                ਪੜ੍ਹਨ, _, _ = select.select([직렬], [], [], 0.1)
                if ਪੜ੍ਹਨ:
                    ਸਮੱਗਰੀ = 직렬.recv(65536)
                    if not ਸਮੱਗਰੀ:
                        raise AssertionError('직렬 ਕੁਨੈਕਸ਼ਨ_ਕਰੋ ਨਿਕਾਸ_ਐਪਲੀਕੇਸ਼')
                    ਲੌਗ_ਕਤਾਰ.extend(ਸਮੱਗਰੀ)
                if ਕਾਰਵਾਈ_ਕੀਮਤ.poll() is not None:
                    raise AssertionError('QEMU 비정상 ਨਿਕਾਸ_ਐਪਲੀਕੇਸ਼: ' + str(ਕਾਰਵਾਈ_ਕੀਮਤ.returncode))
                return ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ.encode('utf-8') in ਲੌਗ_ਕਤਾਰ[ਚਲਾਓ_2:]

            def 명령시험(입력, 기대):
                ਚਲਾਓ_2 = len(ਲੌਗ_ਕਤਾਰ)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, ਚਲਾਓ_2), 기대)
                기다리기(lambda: 포함('jkoros> ', ਚਲਾਓ_2), 'ਕਮਾਂਡ 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in ਲੌਗ_ਕਤਾਰ
            assert '자바 기계어 ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ ਚਲਾਓ_2'.encode() in ਲੌਗ_ਕਤਾਰ
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for ਅਨੁਕ੍ਰਮਣਿਕਾ in range(8):
                명령시험('alloc\n', 'ਵਿਭਾਗ_ਕੀਮਤ ਅਨੁਕ੍ਰਮਣਿਕਾ: ' + str(ਅਨੁਕ੍ਰਮਣਿਕਾ))
            명령시험('alloc\n', 'ਵਿਭਾਗ_ਕੀਮਤ ਅਨੁਕ੍ਰਮਣਿਕਾ: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 ਵਿਭਾਗ_ਕੀਮਤ')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'ਵਿਭਾਗ_ਕੀਮਤ ਅਨੁਕ੍ਰਮਣਿਕਾ: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            ਚਲਾਓ_2 = len(ਲੌਗ_ਕਤਾਰ)
            for ਕੀ_ਕੀਮਤ in ('i', 'n', 'f', 'o', 'ret'):
                ਮੌਨੀਟਰ_ਕੀਮਤ.sendall(('sendkey ' + ਕੀ_ਕੀਮਤ + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', ਚਲਾਓ_2), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 ਕਮਾਂਡ')
            assert b'PANIC' not in ਲੌਗ_ਕਤਾਰ and b'SELFTEST FAIL' not in ਲੌਗ_ਕਤਾਰ
            print('PASS: {} 부팅, Java 자체 시험, 직렬 ਕਮਾਂਡ, PS/2 입력, ਨਿਰਧਾਰਿਤ_ਕਰੋ_ਸਟੋਰੇਜ/반환, 정지'.format(종류))
            return ਲੌਗ_ਕਤਾਰ.decode('utf-8', 'replace')
        finally:
            직렬.close()
            ਮੌਨੀਟਰ_ਕੀਮਤ.close()
            ਕਾਰਵਾਈ_ਕੀਮਤ.terminate()
            try:
                ਕਾਰਵਾਈ_ਕੀਮਤ.wait(timeout=3)
            except subprocess.TimeoutExpired:
                ਕਾਰਵਾਈ_ਕੀਮਤ.kill()
                ਕਾਰਵਾਈ_ਕੀਮਤ.wait()


if __name__ == '__main__':
    ਮਾਪ = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (ਸਥਿਤੀ / 'build/부팅시험.json').write_text(json.dumps(ਮਾਪ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
