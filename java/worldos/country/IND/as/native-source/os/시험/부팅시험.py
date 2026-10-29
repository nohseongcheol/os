#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

অৱস্থান = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        পৰিমাপ = 검사()
        if পৰিমাপ:
            return পৰিমাপ
        time.sleep(0.05)
    raise AssertionError('시간 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        মনিটৰ_পথ = 임시 / 'monitor.sock'
        কমান্ড = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(মনিটৰ_পথ) + ',server,nowait']
        কমান্ড += ['-kernel', str(অৱস্থান / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(অৱস্থান / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        কমান্ড += ['-S']
        প্ৰক্ৰিয়া_মান = subprocess.Popen(কমান্ড, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        মনিটৰ_মান = socket.socket(socket.AF_UNIX)
        লগ_শাৰী = bytearray()
        try:
            def 소켓준비():
                if প্ৰক্ৰিয়া_মান.poll() is not None:
                    raise AssertionError(প্ৰক্ৰিয়া_মান.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and মনিটৰ_পথ.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            মনিটৰ_মান.connect(str(মনিটৰ_পথ))
            직렬.setblocking(False)
            মনিটৰ_মান.sendall(b'cont\n')

            def 포함(ষ্ট্ৰিং_মান, সঞ্চালন=0):
                পড়া, _, _ = select.select([직렬], [], [], 0.1)
                if পড়া:
                    ডাটা = 직렬.recv(65536)
                    if not ডাটা:
                        raise AssertionError('직렬 সংযোগ_স্থাপনা প্ৰস্থান_এপ্প্')
                    লগ_শাৰী.extend(ডাটা)
                if প্ৰক্ৰিয়া_মান.poll() is not None:
                    raise AssertionError('QEMU 비정상 প্ৰস্থান_এপ্প্: ' + str(প্ৰক্ৰিয়া_মান.returncode))
                return ষ্ট্ৰিং_মান.encode('utf-8') in লগ_শাৰী[সঞ্চালন:]

            def 명령시험(입력, 기대):
                সঞ্চালন = len(লগ_শাৰী)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, সঞ্চালন), 기대)
                기다리기(lambda: 포함('jkoros> ', সঞ্চালন), 'কমান্ড 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in লগ_শাৰী
            assert '자바 기계어 কাৰ্ণেল_মান সঞ্চালন'.encode() in লগ_শাৰী
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for ইনডেক্স in range(8):
                명령시험('alloc\n', 'শাখা_মান_366e0bfa ইনডেক্স: ' + str(ইনডেক্স))
            명령시험('alloc\n', 'শাখা_মান_366e0bfa ইনডেক্স: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 শাখা_মান_366e0bfa')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'শাখা_মান_366e0bfa ইনডেক্স: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            সঞ্চালন = len(লগ_শাৰী)
            for কী_মান in ('i', 'n', 'f', 'o', 'ret'):
                মনিটৰ_মান.sendall(('sendkey ' + কী_মান + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', সঞ্চালন), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 কমান্ড')
            assert b'PANIC' not in লগ_শাৰী and b'SELFTEST FAIL' not in লগ_শাৰী
            print('PASS: {} 부팅, Java 자체 시험, 직렬 কমান্ড, PS/2 입력, আৱণ্টন_ষ্ট_ৰেজ/반환, 정지'.format(종류))
            return লগ_শাৰী.decode('utf-8', 'replace')
        finally:
            직렬.close()
            মনিটৰ_মান.close()
            প্ৰক্ৰিয়া_মান.terminate()
            try:
                প্ৰক্ৰিয়া_মান.wait(timeout=3)
            except subprocess.TimeoutExpired:
                প্ৰক্ৰিয়া_মান.kill()
                প্ৰক্ৰিয়া_মান.wait()


if __name__ == '__main__':
    পৰিমাপ = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (অৱস্থান / 'build/부팅시험.json').write_text(json.dumps(পৰিমাপ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
