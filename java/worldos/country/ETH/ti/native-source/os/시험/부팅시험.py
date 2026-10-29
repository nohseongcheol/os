#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

위치 = Path(__file__).resolve().parents[1]


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
        መርኣዪ_መገዲ = 임시 / 'monitor.sock'
        ትእዛዝ = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(መርኣዪ_መገዲ) + ',server,nowait']
        ትእዛዝ += ['-kernel', str(위치 / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(위치 / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        ትእዛዝ += ['-S']
        መስርሕ_ዋጋ = subprocess.Popen(ትእዛዝ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        መርኣዪ_ዋጋ = socket.socket(socket.AF_UNIX)
        ምዝጉብ_ሪጋ = bytearray()
        try:
            def 소켓준비():
                if መስርሕ_ዋጋ.poll() is not None:
                    raise AssertionError(መስርሕ_ዋጋ.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and መርኣዪ_መገዲ.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            መርኣዪ_ዋጋ.connect(str(መርኣዪ_መገዲ))
            직렬.setblocking(False)
            መርኣዪ_ዋጋ.sendall(b'cont\n')

            def 포함(ሕብረ_ቁምፊ_ዋጋ, ኣኺድ=0):
                읽기, _, _ = select.select([직렬], [], [], 0.1)
                if 읽기:
                    ሓበሬታ = 직렬.recv(65536)
                    if not ሓበሬታ:
                        raise AssertionError('직렬 ኣላግብ ውጻእ_መተግበሪ')
                    ምዝጉብ_ሪጋ.extend(ሓበሬታ)
                if መስርሕ_ዋጋ.poll() is not None:
                    raise AssertionError('QEMU 비정상 ውጻእ_መተግበሪ: ' + str(መስርሕ_ዋጋ.returncode))
                return ሕብረ_ቁምፊ_ዋጋ.encode('utf-8') in ምዝጉብ_ሪጋ[ኣኺድ:]

            def 명령시험(입력, 기대):
                ኣኺድ = len(ምዝጉብ_ሪጋ)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, ኣኺድ), 기대)
                기다리기(lambda: 포함('jkoros> ', ኣኺድ), 'ትእዛዝ 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in ምዝጉብ_ሪጋ
            assert '자바 기계어 ፍረ_ዋጋ ኣኺድ'.encode() in ምዝጉብ_ሪጋ
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for መሐበሪ in range(8):
                명령시험('alloc\n', 'ክፋል_ዋጋ መሐበሪ: ' + str(መሐበሪ))
            명령시험('alloc\n', 'ክፋል_ዋጋ መሐበሪ: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 ክፋል_ዋጋ')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'ክፋል_ዋጋ መሐበሪ: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            ኣኺድ = len(ምዝጉብ_ሪጋ)
            for መፍትሕ_ዋጋ in ('i', 'n', 'f', 'o', 'ret'):
                መርኣዪ_ዋጋ.sendall(('sendkey ' + መፍትሕ_ዋጋ + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', ኣኺድ), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 ትእዛዝ')
            assert b'PANIC' not in ምዝጉብ_ሪጋ and b'SELFTEST FAIL' not in ምዝጉብ_ሪጋ
            print('PASS: {} 부팅, Java 자체 시험, 직렬 ትእዛዝ, PS/2 입력, ምምዳብ_መኽዘን/반환, 정지'.format(종류))
            return ምዝጉብ_ሪጋ.decode('utf-8', 'replace')
        finally:
            직렬.close()
            መርኣዪ_ዋጋ.close()
            መስርሕ_ዋጋ.terminate()
            try:
                መስርሕ_ዋጋ.wait(timeout=3)
            except subprocess.TimeoutExpired:
                መስርሕ_ዋጋ.kill()
                መስርሕ_ዋጋ.wait()


if __name__ == '__main__':
    결과 = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (위치 / 'build/부팅시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
