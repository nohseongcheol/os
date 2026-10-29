#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

অবস্থান = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        পরিমাপ = 검사()
        if পরিমাপ:
            return পরিমাপ
        time.sleep(0.05)
    raise AssertionError('সময়_মান 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        মনিটর_পথ = 임시 / 'monitor.sock'
        আদেশ = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(মনিটর_পথ) + ',server,nowait']
        আদেশ += ['-kernel', str(অবস্থান / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(অবস্থান / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        আদেশ += ['-S']
        প্রসেসর_মান = subprocess.Popen(আদেশ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        মনিটর_মান = socket.socket(socket.AF_UNIX)
        লগ_সারি = bytearray()
        try:
            def 소켓준비():
                if প্রসেসর_মান.poll() is not None:
                    raise AssertionError(প্রসেসর_মান.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and মনিটর_পথ.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            মনিটর_মান.connect(str(মনিটর_পথ))
            직렬.setblocking(False)
            মনিটর_মান.sendall(b'cont\n')

            def 포함(স্ট্রিং_মান, চালনা=0):
                পড়া, _, _ = select.select([직렬], [], [], 0.1)
                if পড়া:
                    ডাটা = 직렬.recv(65536)
                    if not ডাটা:
                        raise AssertionError('직렬 সংযোগ_স্থাপনা প্রস্থান_অ্যাপ')
                    লগ_সারি.extend(ডাটা)
                if প্রসেসর_মান.poll() is not None:
                    raise AssertionError('QEMU 비정상 প্রস্থান_অ্যাপ: ' + str(প্রসেসর_মান.returncode))
                return স্ট্রিং_মান.encode('utf-8') in লগ_সারি[চালনা:]

            def 명령시험(입력, 기대):
                চালনা = len(লগ_সারি)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, চালনা), 기대)
                기다리기(lambda: 포함('jkoros> ', চালনা), 'আদেশ 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in লগ_সারি
            assert '자바 기계어 কারনেল_মান চালনা'.encode() in লগ_সারি
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for সূচি in range(8):
                명령시험('alloc\n', 'শাখা_মান_366e0bfa সূচি: ' + str(সূচি))
            명령시험('alloc\n', 'শাখা_মান_366e0bfa সূচি: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 শাখা_মান_366e0bfa')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'শাখা_মান_366e0bfa সূচি: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            চালনা = len(লগ_সারি)
            for কী_মান in ('i', 'n', 'f', 'o', 'ret'):
                মনিটর_মান.sendall(('sendkey ' + কী_মান + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', চালনা), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 আদেশ')
            assert b'PANIC' not in লগ_সারি and b'SELFTEST FAIL' not in লগ_সারি
            print('PASS: {} 부팅, Java নিজ 시험, 직렬 আদেশ, PS/2 입력, বন্টন_করা_স্টোরেজ/반환, 정지'.format(종류))
            return লগ_সারি.decode('utf-8', 'replace')
        finally:
            직렬.close()
            মনিটর_মান.close()
            প্রসেসর_মান.terminate()
            try:
                প্রসেসর_মান.wait(timeout=3)
            except subprocess.TimeoutExpired:
                প্রসেসর_মান.kill()
                প্রসেসর_মান.wait()


if __name__ == '__main__':
    পরিমাপ = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (অবস্থান / 'build/부팅시험.json').write_text(json.dumps(পরিমাপ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
