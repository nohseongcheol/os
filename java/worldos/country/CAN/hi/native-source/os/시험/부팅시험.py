#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

स्थान = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        परिणाम = 검사()
        if परिणाम:
            return परिणाम
        time.sleep(0.05)
    raise AssertionError('समय_उपयोगिता 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        मॉनीटर_पथ = 임시 / 'monitor.sock'
        आदेश = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(मॉनीटर_पथ) + ',server,nowait']
        आदेश += ['-kernel', str(स्थान / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(स्थान / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        आदेश += ['-S']
        प्रक्रिया_मान = subprocess.Popen(आदेश, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        मॉनीटर_मान = socket.socket(socket.AF_UNIX)
        लॉग_रिकॉर्ड = bytearray()
        try:
            def 소켓준비():
                if प्रक्रिया_मान.poll() is not None:
                    raise AssertionError(प्रक्रिया_मान.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and मॉनीटर_पथ.exists()
            기다리기(소켓준비, 'QEMU सॉकेट_मान')
            직렬.connect(str(직렬경로))
            मॉनीटर_मान.connect(str(मॉनीटर_पथ))
            직렬.setblocking(False)
            मॉनीटर_मान.sendall(b'cont\n')

            def 포함(स्ट्रिंग_मान, चलाएँ=0):
                पढ़ें, _, _ = select.select([직렬], [], [], 0.1)
                if पढ़ें:
                    आँकड़े = 직렬.recv(65536)
                    if not आँकड़े:
                        raise AssertionError('직렬 जोड़ना निर्गमन_ऐप')
                    लॉग_रिकॉर्ड.extend(आँकड़े)
                if प्रक्रिया_मान.poll() is not None:
                    raise AssertionError('QEMU 비정상 निर्गमन_ऐप: ' + str(प्रक्रिया_मान.returncode))
                return स्ट्रिंग_मान.encode('utf-8') in लॉग_रिकॉर्ड[चलाएँ:]

            def 명령시험(입력, 기대):
                चलाएँ = len(लॉग_रिकॉर्ड)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, चलाएँ), 기대)
                기다리기(lambda: 포함('jkoros> ', चलाएँ), 'आदेश 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in लॉग_रिकॉर्ड
            assert '자바 기계어 कर्नेल_मान चलाएँ'.encode() in लॉग_रिकॉर्ड
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for इंडेक्स in range(8):
                명령시험('alloc\n', 'खंड_मान इंडेक्स: ' + str(इंडेक्स))
            명령시험('alloc\n', 'खंड_मान इंडेक्स: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 खंड_मान')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'खंड_मान इंडेक्स: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            चलाएँ = len(लॉग_रिकॉर्ड)
            for कुंजी_मान in ('i', 'n', 'f', 'o', 'ret'):
                मॉनीटर_मान.sendall(('sendkey ' + कुंजी_मान + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', चलाएँ), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 आदेश')
            assert b'PANIC' not in लॉग_रिकॉर्ड and b'SELFTEST FAIL' not in लॉग_रिकॉर्ड
            print('PASS: {} 부팅, Java निज 시험, 직렬 आदेश, PS/2 입력, आवंटित_करें_संग्रहण/वापस_करें_परिणाम, 정지'.format(종류))
            return लॉग_रिकॉर्ड.decode('utf-8', 'replace')
        finally:
            직렬.close()
            मॉनीटर_मान.close()
            प्रक्रिया_मान.terminate()
            try:
                प्रक्रिया_मान.wait(timeout=3)
            except subprocess.TimeoutExpired:
                प्रक्रिया_मान.kill()
                प्रक्रिया_मान.wait()


if __name__ == '__main__':
    परिणाम = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (स्थान / 'build/부팅시험.json').write_text(json.dumps(परिणाम, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
