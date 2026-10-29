#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

स्थिती = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        मेजप = 검사()
        if मेजप:
            return मेजप
        time.sleep(0.05)
    raise AssertionError('TIME_मोल 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        मॉनिटर_पाथ = 임시 / 'monitor.sock'
        आदेश = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(मॉनिटर_पाथ) + ',server,nowait']
        आदेश += ['-kernel', str(स्थिती / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(स्थिती / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        आदेश += ['-S']
        प्रक्रिया_मोल = subprocess.Popen(आदेश, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        मॉनिटर_मोल = socket.socket(socket.AF_UNIX)
        LOG_नोंद = bytearray()
        try:
            def 소켓준비():
                if प्रक्रिया_मोल.poll() is not None:
                    raise AssertionError(प्रक्रिया_मोल.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and मॉनिटर_पाथ.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            मॉनिटर_मोल.connect(str(मॉनिटर_पाथ))
            직렬.setblocking(False)
            मॉनिटर_मोल.sendall(b'cont\n')

            def 포함(स्ट्रिंग_मोल, चलोवप=0):
                읽기, _, _ = select.select([직렬], [], [], 0.1)
                if 읽기:
                    डेटा = 직렬.recv(65536)
                    if not डेटा:
                        raise AssertionError('직렬 कनॅक्ट प्रस्थान_करचें_एप्लिकेशन')
                    LOG_नोंद.extend(डेटा)
                if प्रक्रिया_मोल.poll() is not None:
                    raise AssertionError('QEMU 비정상 प्रस्थान_करचें_एप्लिकेशन: ' + str(प्रक्रिया_मोल.returncode))
                return स्ट्रिंग_मोल.encode('utf-8') in LOG_नोंद[चलोवप:]

            def 명령시험(입력, 기대):
                चलोवप = len(LOG_नोंद)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, चलोवप), 기대)
                기다리기(lambda: 포함('jkoros> ', चलोवप), 'आदेश 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in LOG_नोंद
            assert '자바 기계어 कर्नेल_मोल चलोवप'.encode() in LOG_नोंद
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for INDEX in range(8):
                명령시험('alloc\n', 'विभाग_मोल INDEX: ' + str(INDEX))
            명령시험('alloc\n', 'विभाग_मोल INDEX: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 विभाग_मोल')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'विभाग_मोल INDEX: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            चलोवप = len(LOG_नोंद)
            for की_मोल in ('i', 'n', 'f', 'o', 'ret'):
                मॉनिटर_मोल.sendall(('sendkey ' + की_मोल + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', चलोवप), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 आदेश')
            assert b'PANIC' not in LOG_नोंद and b'SELFTEST FAIL' not in LOG_नोंद
            print('PASS: {} 부팅, Java 자체 시험, 직렬 आदेश, PS/2 입력, नेमून_दिवचें_सांठवण/return_मेजप, 정지'.format(종류))
            return LOG_नोंद.decode('utf-8', 'replace')
        finally:
            직렬.close()
            मॉनिटर_मोल.close()
            प्रक्रिया_मोल.terminate()
            try:
                प्रक्रिया_मोल.wait(timeout=3)
            except subprocess.TimeoutExpired:
                प्रक्रिया_मोल.kill()
                प्रक्रिया_मोल.wait()


if __name__ == '__main__':
    मेजप = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (स्थिती / 'build/부팅시험.json').write_text(json.dumps(मेजप, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
