#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

កំណត់ទីតាំង = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        ការវាស់វែង = 검사()
        if ការវាស់វែង:
            return ការវាស់វែង
        time.sleep(0.05)
    raise AssertionError('ពេល_វេលា_តំលៃ 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        ម៉ូនីទ័រ_ផ្លូវ = 임시 / 'monitor.sock'
        ពាក្យ_បញ្ជា = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(ម៉ូនីទ័រ_ផ្លូវ) + ',server,nowait']
        ពាក្យ_បញ្ជា += ['-kernel', str(កំណត់ទីតាំង / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(កំណត់ទីតាំង / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        ពាក្យ_បញ្ជា += ['-S']
        ដំណើរការ_តំលៃ = subprocess.Popen(ពាក្យ_បញ្ជា, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        ម៉ូនីទ័រ_តំលៃ = socket.socket(socket.AF_UNIX)
        កំណត់_ហេតុ_ថត = bytearray()
        try:
            def 소켓준비():
                if ដំណើរការ_តំលៃ.poll() is not None:
                    raise AssertionError(ដំណើរការ_តំលៃ.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and ម៉ូនីទ័រ_ផ្លូវ.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            ម៉ូនីទ័រ_តំលៃ.connect(str(ម៉ូនីទ័រ_ផ្លូវ))
            직렬.setblocking(False)
            ម៉ូនីទ័រ_តំលៃ.sendall(b'cont\n')

            def 포함(សំនុំអក្សរ_តំលៃ, រត់=0):
                អាន, _, _ = select.select([직렬], [], [], 0.1)
                if អាន:
                    ទិន្នន័យ = 직렬.recv(65536)
                    if not ទិន្នន័យ:
                        raise AssertionError('직렬 ភ្ជាប់ ចេញ_កម្មវិធី')
                    កំណត់_ហេតុ_ថត.extend(ទិន្នន័យ)
                if ដំណើរការ_តំលៃ.poll() is not None:
                    raise AssertionError('QEMU 비정상 ចេញ_កម្មវិធី: ' + str(ដំណើរការ_តំលៃ.returncode))
                return សំនុំអក្សរ_តំលៃ.encode('utf-8') in កំណត់_ហេតុ_ថត[រត់:]

            def 명령시험(입력, 기대):
                រត់ = len(កំណត់_ហេតុ_ថត)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, រត់), 기대)
                기다리기(lambda: 포함('jkoros> ', រត់), 'ពាក្យ_បញ្ជា 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in កំណត់_ហេតុ_ថត
            assert '자바 기계어 ខឺណេល_តំលៃ រត់'.encode() in កំណត់_ហេតុ_ថត
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for សន្ទស្សន៏ in range(8):
                명령시험('alloc\n', 'ផ្នែក_តំលៃ សន្ទស្សន៏: ' + str(សន្ទស្សន៏))
            명령시험('alloc\n', 'ផ្នែក_តំលៃ សន្ទស្សន៏: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 ផ្នែក_តំលៃ')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'ផ្នែក_តំលៃ សន្ទស្សន៏: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            រត់ = len(កំណត់_ហេតុ_ថត)
            for ឃី_តំលៃ in ('i', 'n', 'f', 'o', 'ret'):
                ម៉ូនីទ័រ_តំលៃ.sendall(('sendkey ' + ឃី_តំលៃ + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', រត់), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 ពាក្យ_បញ្ជា')
            assert b'PANIC' not in កំណត់_ហេតុ_ថត and b'SELFTEST FAIL' not in កំណត់_ហេតុ_ថត
            print('PASS: {} 부팅, Java 자체 시험, 직렬 ពាក្យ_បញ្ជា, PS/2 입력, លៃទុក_ការផ្ទុក/반환, 정지'.format(종류))
            return កំណត់_ហេតុ_ថត.decode('utf-8', 'replace')
        finally:
            직렬.close()
            ម៉ូនីទ័រ_តំលៃ.close()
            ដំណើរការ_តំលៃ.terminate()
            try:
                ដំណើរការ_តំលៃ.wait(timeout=3)
            except subprocess.TimeoutExpired:
                ដំណើរការ_តំលៃ.kill()
                ដំណើរការ_តំលៃ.wait()


if __name__ == '__main__':
    ការវាស់វែង = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (កំណត់ទីតាំង / 'build/부팅시험.json').write_text(json.dumps(ការវាស់វែង, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
