#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

ଅବସ୍ଥାନ = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        ମାପ = 검사()
        if ମାପ:
            return ମାପ
        time.sleep(0.05)
    raise AssertionError('ସମୟ_ମୂଲ୍ୟ 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        ମନିଟର୍_ପଥ = 임시 / 'monitor.sock'
        ନିର୍ଦ୍ଦେଶ = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(ମନିଟର୍_ପଥ) + ',server,nowait']
        ନିର୍ଦ୍ଦେଶ += ['-kernel', str(ଅବସ୍ଥାନ / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(ଅବସ୍ଥାନ / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        ନିର୍ଦ୍ଦେଶ += ['-S']
        ପ୍ରୋସେସ୍_ମୂଲ୍ୟ = subprocess.Popen(ନିର୍ଦ୍ଦେଶ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        ମନିଟର୍_ମୂଲ୍ୟ = socket.socket(socket.AF_UNIX)
        ଲଗ୍_ଧାଡ଼ି = bytearray()
        try:
            def 소켓준비():
                if ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.poll() is not None:
                    raise AssertionError(ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and ମନିଟର୍_ପଥ.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            ମନିଟର୍_ମୂଲ୍ୟ.connect(str(ମନିଟର୍_ପଥ))
            직렬.setblocking(False)
            ମନିଟର୍_ମୂଲ୍ୟ.sendall(b'cont\n')

            def 포함(ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ, ଚଳାନ୍ତୁ=0):
                ପଢନ୍ତୁ, _, _ = select.select([직렬], [], [], 0.1)
                if ପଢନ୍ତୁ:
                    ଡାଟା = 직렬.recv(65536)
                    if not ଡାଟା:
                        raise AssertionError('직렬 ସଂଯୋଗ_କରନ୍ତୁ ପ୍ରସ୍ଥାନ_ଅନୁପ୍ରୟୋଗ')
                    ଲଗ୍_ଧାଡ଼ି.extend(ଡାଟା)
                if ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.poll() is not None:
                    raise AssertionError('QEMU 비정상 ପ୍ରସ୍ଥାନ_ଅନୁପ୍ରୟୋଗ: ' + str(ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.returncode))
                return ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ.encode('utf-8') in ଲଗ୍_ଧାଡ଼ି[ଚଳାନ୍ତୁ:]

            def 명령시험(입력, 기대):
                ଚଳାନ୍ତୁ = len(ଲଗ୍_ଧାଡ଼ି)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, ଚଳାନ୍ତୁ), 기대)
                기다리기(lambda: 포함('jkoros> ', ଚଳାନ୍ତୁ), 'ନିର୍ଦ୍ଦେଶ 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in ଲଗ୍_ଧାଡ଼ି
            assert '자바 기계어 କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ ଚଳାନ୍ତୁ'.encode() in ଲଗ୍_ଧାଡ଼ି
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for ଅନୁକ୍ରମଣିକା in range(8):
                명령시험('alloc\n', 'ବିଭାଗ_ମୂଲ୍ୟ ଅନୁକ୍ରମଣିକା: ' + str(ଅନୁକ୍ରମଣିକା))
            명령시험('alloc\n', 'ବିଭାଗ_ମୂଲ୍ୟ ଅନୁକ୍ରମଣିକା: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 ବିଭାଗ_ମୂଲ୍ୟ')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'ବିଭାଗ_ମୂଲ୍ୟ ଅନୁକ୍ରମଣିକା: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            ଚଳାନ୍ତୁ = len(ଲଗ୍_ଧାଡ଼ି)
            for କୀ_ମୂଲ୍ୟ in ('i', 'n', 'f', 'o', 'ret'):
                ମନିଟର୍_ମୂଲ୍ୟ.sendall(('sendkey ' + କୀ_ମୂଲ୍ୟ + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', ଚଳାନ୍ତୁ), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 ନିର୍ଦ୍ଦେଶ')
            assert b'PANIC' not in ଲଗ୍_ଧାଡ଼ି and b'SELFTEST FAIL' not in ଲଗ୍_ଧାଡ଼ି
            print('PASS: {} 부팅, Java 자체 시험, 직렬 ନିର୍ଦ୍ଦେଶ, PS/2 입력, ବଣ୍ଟନ_ଷ୍ଟୋରେଜ୍/반환, 정지'.format(종류))
            return ଲଗ୍_ଧାଡ଼ି.decode('utf-8', 'replace')
        finally:
            직렬.close()
            ମନିଟର୍_ମୂଲ୍ୟ.close()
            ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.terminate()
            try:
                ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.wait(timeout=3)
            except subprocess.TimeoutExpired:
                ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.kill()
                ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.wait()


if __name__ == '__main__':
    ମାପ = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (ଅବସ୍ଥାନ / 'build/부팅시험.json').write_text(json.dumps(ମାପ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
