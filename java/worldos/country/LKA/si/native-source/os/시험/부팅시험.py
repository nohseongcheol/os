#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

පිහිටීම = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        결과 = 검사()
        if 결과:
            return 결과
        time.sleep(0.05)
    raise AssertionError('시간 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        මොනිටරය_පෙත = 임시 / 'monitor.sock'
        විධානය = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(මොනිටරය_පෙත) + ',server,nowait']
        විධානය += ['-kernel', str(පිහිටීම / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(පිහිටීම / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        විධානය += ['-S']
        ක්_රියාවලිය_අගය = subprocess.Popen(විධානය, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        මොනිටරය_අගය = socket.socket(socket.AF_UNIX)
        ලොගය_පේළිය = bytearray()
        try:
            def 소켓준비():
                if ක්_රියාවලිය_අගය.poll() is not None:
                    raise AssertionError(ක්_රියාවලිය_අගය.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and මොනිටරය_පෙත.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            මොනිටරය_අගය.connect(str(මොනිටරය_පෙත))
            직렬.setblocking(False)
            මොනිටරය_අගය.sendall(b'cont\n')

            def 포함(අනුලකුණු_වැල_අගය, ක්_රියාත්මක_කරන්න_2=0):
                කියවීම, _, _ = select.select([직렬], [], [], 0.1)
                if කියවීම:
                    දත්ත = 직렬.recv(65536)
                    if not දත්ත:
                        raise AssertionError('직렬 සම්බන්ද_වන්න පිටවීම_යෙදු')
                    ලොගය_පේළිය.extend(දත්ත)
                if ක්_රියාවලිය_අගය.poll() is not None:
                    raise AssertionError('QEMU 비정상 පිටවීම_යෙදු: ' + str(ක්_රියාවලිය_අගය.returncode))
                return අනුලකුණු_වැල_අගය.encode('utf-8') in ලොගය_පේළිය[ක්_රියාත්මක_කරන්න_2:]

            def 명령시험(입력, 기대):
                ක්_රියාත්මක_කරන්න_2 = len(ලොගය_පේළිය)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, ක්_රියාත්මක_කරන්න_2), 기대)
                기다리기(lambda: 포함('jkoros> ', ක්_රියාත්මක_කරන්න_2), 'විධානය 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in ලොගය_පේළිය
            assert '자바 기계어 කර්නලය_අගය ක්_රියාත්මක_කරන්න_2'.encode() in ලොගය_පේළිය
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for සූචිය in range(8):
                명령시험('alloc\n', 'අංශය_අගය සූචිය: ' + str(සූචිය))
            명령시험('alloc\n', 'අංශය_අගය සූචිය: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 අංශය_අගය')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'අංශය_අගය සූචිය: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            ක්_රියාත්මක_කරන්න_2 = len(ලොගය_පේළිය)
            for යතුර_අගය in ('i', 'n', 'f', 'o', 'ret'):
                මොනිටරය_අගය.sendall(('sendkey ' + යතුර_අගය + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', ක්_රියාත්මක_කරන්න_2), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 විධානය')
            assert b'PANIC' not in ලොගය_පේළිය and b'SELFTEST FAIL' not in ලොගය_පේළිය
            print('PASS: {} 부팅, Java 자체 시험, 직렬 විධානය, PS/2 입력, විබෙදන්න_ගබඩාව/반환, 정지'.format(종류))
            return ලොගය_පේළිය.decode('utf-8', 'replace')
        finally:
            직렬.close()
            මොනිටරය_අගය.close()
            ක්_රියාවලිය_අගය.terminate()
            try:
                ක්_රියාවලිය_අගය.wait(timeout=3)
            except subprocess.TimeoutExpired:
                ක්_රියාවලිය_අගය.kill()
                ක්_රියාවලිය_අගය.wait()


if __name__ == '__main__':
    결과 = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (පිහිටීම / 'build/부팅시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
