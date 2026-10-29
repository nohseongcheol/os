#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

स्थिति = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        मापन = 검사()
        if मापन:
            return मापन
        time.sleep(0.05)
    raise AssertionError('시간 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        मनिटर_बाटो = 임시 / 'monitor.sock'
        आदेश = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(मनिटर_बाटो) + ',server,nowait']
        आदेश += ['-kernel', str(स्थिति / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(स्थिति / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        आदेश += ['-S']
        प्रक्रिया_मान = subprocess.Popen(आदेश, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        मनिटर_मान = socket.socket(socket.AF_UNIX)
        लग_रेकर्ड = bytearray()
        try:
            def 소켓준비():
                if प्रक्रिया_मान.poll() is not None:
                    raise AssertionError(प्रक्रिया_मान.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and मनिटर_बाटो.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            मनिटर_मान.connect(str(मनिटर_बाटो))
            직렬.setblocking(False)
            मनिटर_मान.sendall(b'cont\n')

            def 포함(स्ट्रिङ_मान, चलाउनुहोस्=0):
                पढनुहोस्, _, _ = select.select([직렬], [], [], 0.1)
                if पढनुहोस्:
                    लगत = 직렬.recv(65536)
                    if not लगत:
                        raise AssertionError('직렬 जडान बाहिर_जानुहोस्_अनुप्रयोग')
                    लग_रेकर्ड.extend(लगत)
                if प्रक्रिया_मान.poll() is not None:
                    raise AssertionError('QEMU 비정상 बाहिर_जानुहोस्_अनुप्रयोग: ' + str(प्रक्रिया_मान.returncode))
                return स्ट्रिङ_मान.encode('utf-8') in लग_रेकर्ड[चलाउनुहोस्:]

            def 명령시험(입력, 기대):
                चलाउनुहोस् = len(लग_रेकर्ड)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, चलाउनुहोस्), 기대)
                기다리기(lambda: 포함('jkoros> ', चलाउनुहोस्), 'आदेश 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in लग_रेकर्ड
            assert '자바 기계어 कर्णेल_मान चलाउनुहोस्'.encode() in लग_रेकर्ड
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for अनुक्रमणिका in range(8):
                명령시험('alloc\n', 'सेक्सन_मान अनुक्रमणिका: ' + str(अनुक्रमणिका))
            명령시험('alloc\n', 'सेक्सन_मान अनुक्रमणिका: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 सेक्सन_मान')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'सेक्सन_मान अनुक्रमणिका: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            चलाउनुहोस् = len(लग_रेकर्ड)
            for कुञ्जी_मान in ('i', 'n', 'f', 'o', 'ret'):
                मनिटर_मान.sendall(('sendkey ' + कुञ्जी_मान + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', चलाउनुहोस्), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 आदेश')
            assert b'PANIC' not in लग_रेकर्ड and b'SELFTEST FAIL' not in लग_रेकर्ड
            print('PASS: {} 부팅, Java निज 시험, 직렬 आदेश, PS/2 입력, निर्धारण_गर्नुहोस्_भण्डारण/반환, 정지'.format(종류))
            return लग_रेकर्ड.decode('utf-8', 'replace')
        finally:
            직렬.close()
            मनिटर_मान.close()
            प्रक्रिया_मान.terminate()
            try:
                प्रक्रिया_मान.wait(timeout=3)
            except subprocess.TimeoutExpired:
                प्रक्रिया_मान.kill()
                प्रक्रिया_मान.wait()


if __name__ == '__main__':
    मापन = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (स्थिति / 'build/부팅시험.json').write_text(json.dumps(मापन, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
