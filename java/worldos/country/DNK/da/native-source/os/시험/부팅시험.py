#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

Placering = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        KR = 검사()
        if KR:
            return KR
        time.sleep(0.05)
    raise AssertionError('TID_VÆRDI 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        monitor_sti = 임시 / 'monitor.sock'
        Kommando = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_sti) + ',server,nowait']
        Kommando += ['-kernel', str(Placering / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(Placering / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        Kommando += ['-S']
        Proces_VÆRDI = subprocess.Popen(Kommando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        monitor_VÆRDI = socket.socket(socket.AF_UNIX)
        LOG_post = bytearray()
        try:
            def Tilrettelæg_socket():
                if Proces_VÆRDI.poll() is not None:
                    raise AssertionError(Proces_VÆRDI.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and monitor_sti.exists()
            기다리기(Tilrettelæg_socket, 'QEMU socket_VÆRDI')
            직렬.connect(str(직렬경로))
            monitor_VÆRDI.connect(str(monitor_sti))
            직렬.setblocking(False)
            monitor_VÆRDI.sendall(b'cont\n')

            def 포함(streng_VÆRDI, Kør_2=0):
                Læse, _, _ = select.select([직렬], [], [], 0.1)
                if Læse:
                    data = 직렬.recv(65536)
                    if not data:
                        raise AssertionError('직렬 Tilslut Afslut_app')
                    LOG_post.extend(data)
                if Proces_VÆRDI.poll() is not None:
                    raise AssertionError('QEMU 비정상 Afslut_app: ' + str(Proces_VÆRDI.returncode))
                return streng_VÆRDI.encode('utf-8') in LOG_post[Kør_2:]

            def 명령시험(input_VÆRDI, 기대):
                Kør_2 = len(LOG_post)
                직렬.sendall(input_VÆRDI.encode('ascii'))
                기다리기(lambda: 포함(기대, Kør_2), 기대)
                기다리기(lambda: 포함('jkoros> ', Kør_2), 'Kommando 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in LOG_post
            assert '자바 기계어 kerne_VÆRDI Kør_2'.encode() in LOG_post
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for INDEKS in range(8):
                명령시험('alloc\n', 'sektion_VÆRDI INDEKS: ' + str(INDEKS))
            명령시험('alloc\n', 'sektion_VÆRDI INDEKS: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 sektion_VÆRDI')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'sektion_VÆRDI INDEKS: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 tal 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Kør_2 = len(LOG_post)
            for tast_VÆRDI in ('i', 'n', 'f', 'o', 'ret'):
                monitor_VÆRDI.sendall(('sendkey ' + tast_VÆRDI + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', Kør_2), 'PS/2 info input_VÆRDI')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 Kommando')
            assert b'PANIC' not in LOG_post and b'SELFTEST FAIL' not in LOG_post
            print('PASS: {} 부팅, Java eget 시험, 직렬 Kommando, PS/2 input_VÆRDI, tildel_Lager/returnere_KR, 정지'.format(종류))
            return LOG_post.decode('utf-8', 'replace')
        finally:
            직렬.close()
            monitor_VÆRDI.close()
            Proces_VÆRDI.terminate()
            try:
                Proces_VÆRDI.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Proces_VÆRDI.kill()
                Proces_VÆRDI.wait()


if __name__ == '__main__':
    KR = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (Placering / 'build/부팅시험.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
