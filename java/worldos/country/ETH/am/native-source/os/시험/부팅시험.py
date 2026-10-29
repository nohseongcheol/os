#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

አካባቢ = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        ልኬት = 검사()
        if ልኬት:
            return ልኬት
        time.sleep(0.05)
    raise AssertionError('ጊዜ_እሴት 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        ማሳያ_ዱካ = 임시 / 'monitor.sock'
        ትእዛዝ = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(ማሳያ_ዱካ) + ',server,nowait']
        ትእዛዝ += ['-kernel', str(አካባቢ / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(አካባቢ / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        ትእዛዝ += ['-S']
        ሂደት_እሴት = subprocess.Popen(ትእዛዝ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        ማሳያ_እሴት = socket.socket(socket.AF_UNIX)
        መዝግብ_ረድፍ = bytearray()
        try:
            def 소켓준비():
                if ሂደት_እሴት.poll() is not None:
                    raise AssertionError(ሂደት_እሴት.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and ማሳያ_ዱካ.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            ማሳያ_እሴት.connect(str(ማሳያ_ዱካ))
            직렬.setblocking(False)
            ማሳያ_እሴት.sendall(b'cont\n')

            def 포함(ኅብረቁምፊ_እሴት, ማስኬጃ=0):
                ማንበቢያ, _, _ = select.select([직렬], [], [], 0.1)
                if ማንበቢያ:
                    ውሂብ = 직렬.recv(65536)
                    if not ውሂብ:
                        raise AssertionError('직렬 መገናኛ ውጣ_ፕሮግራም')
                    መዝግብ_ረድፍ.extend(ውሂብ)
                if ሂደት_እሴት.poll() is not None:
                    raise AssertionError('QEMU 비정상 ውጣ_ፕሮግራም: ' + str(ሂደት_እሴት.returncode))
                return ኅብረቁምፊ_እሴት.encode('utf-8') in መዝግብ_ረድፍ[ማስኬጃ:]

            def 명령시험(입력, 기대):
                ማስኬጃ = len(መዝግብ_ረድፍ)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, ማስኬጃ), 기대)
                기다리기(lambda: 포함('jkoros> ', ማስኬጃ), 'ትእዛዝ 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in መዝግብ_ረድፍ
            assert '자바 기계어 ዓንኳር_እሴት ማስኬጃ'.encode() in መዝግብ_ረድፍ
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for መረጃ_ጠቆመ in range(8):
                명령시험('alloc\n', 'ክፍል_እሴት መረጃ_ጠቆመ: ' + str(መረጃ_ጠቆመ))
            명령시험('alloc\n', 'ክፍል_እሴት መረጃ_ጠቆመ: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 ክፍል_እሴት')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'ክፍል_እሴት መረጃ_ጠቆመ: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            ማስኬጃ = len(መዝግብ_ረድፍ)
            for ቁልፍ_እሴት in ('i', 'n', 'f', 'o', 'ret'):
                ማሳያ_እሴት.sendall(('sendkey ' + ቁልፍ_እሴት + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', ማስኬጃ), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 ትእዛዝ')
            assert b'PANIC' not in መዝግብ_ረድፍ and b'SELFTEST FAIL' not in መዝግብ_ረድፍ
            print('PASS: {} 부팅, Java 자체 시험, 직렬 ትእዛዝ, PS/2 입력, መደብ_ማከማቻ/반환, 정지'.format(종류))
            return መዝግብ_ረድፍ.decode('utf-8', 'replace')
        finally:
            직렬.close()
            ማሳያ_እሴት.close()
            ሂደት_እሴት.terminate()
            try:
                ሂደት_እሴት.wait(timeout=3)
            except subprocess.TimeoutExpired:
                ሂደት_እሴት.kill()
                ሂደት_እሴት.wait()


if __name__ == '__main__':
    ልኬት = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (አካባቢ / 'build/부팅시험.json').write_text(json.dumps(ልኬት, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
