#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

ځای = Path(__file__).resolve().parents[1]


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
        ليدانى_يونلور = 임시 / 'monitor.sock'
        بولۍ = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(ليدانى_يونلور) + ',server,nowait']
        بولۍ += ['-kernel', str(ځای / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(ځای / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        بولۍ += ['-S']
        과정 = subprocess.Popen(بولۍ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        ليدانى_ارزښت = socket.socket(socket.AF_UNIX)
        خبرال_کیل = bytearray()
        try:
            def 소켓준비():
                if 과정.poll() is not None:
                    raise AssertionError(과정.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and ليدانى_يونلور.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            ليدانى_ارزښت.connect(str(ليدانى_يونلور))
            직렬.setblocking(False)
            ليدانى_ارزښت.sendall(b'cont\n')

            def 포함(مزى_ارزښت_6ca8363c, ځغلول=0):
                لوستل, _, _ = select.select([직렬], [], [], 0.1)
                if لوستل:
                    اومتوک = 직렬.recv(65536)
                    if not اومتوک:
                        raise AssertionError('직렬 نښلېدل وتون_کاريال')
                    خبرال_کیل.extend(اومتوک)
                if 과정.poll() is not None:
                    raise AssertionError('QEMU 비정상 وتون_کاريال: ' + str(과정.returncode))
                return مزى_ارزښت_6ca8363c.encode('utf-8') in خبرال_کیل[ځغلول:]

            def 명령시험(입력, 기대):
                ځغلول = len(خبرال_کیل)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, ځغلول), 기대)
                기다리기(lambda: 포함('jkoros> ', ځغلول), 'بولۍ 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in خبرال_کیل
            assert '자바 기계어 نوغی_ارزښت ځغلول'.encode() in خبرال_کیل
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for لړیال in range(8):
                명령시험('alloc\n', 'برخه_ارزښت لړیال: ' + str(لړیال))
            명령시험('alloc\n', 'برخه_ارزښت لړیال: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 برخه_ارزښت')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'برخه_ارزښت لړیال: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            ځغلول = len(خبرال_کیل)
            for کيلي_ارزښت in ('i', 'n', 'f', 'o', 'ret'):
                ليدانى_ارزښت.sendall(('sendkey ' + کيلي_ارزښت + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', ځغلول), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 بولۍ')
            assert b'PANIC' not in خبرال_کیل and b'SELFTEST FAIL' not in خبرال_کیل
            print('PASS: {} 부팅, Java 자체 시험, 직렬 بولۍ, PS/2 입력, 할당/반환, 정지'.format(종류))
            return خبرال_کیل.decode('utf-8', 'replace')
        finally:
            직렬.close()
            ليدانى_ارزښت.close()
            과정.terminate()
            try:
                과정.wait(timeout=3)
            except subprocess.TimeoutExpired:
                과정.kill()
                과정.wait()


if __name__ == '__main__':
    결과 = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (ځای / 'build/부팅시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
