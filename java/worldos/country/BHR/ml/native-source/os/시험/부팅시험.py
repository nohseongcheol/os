#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

സ്ഥാനം = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        അളവ് = 검사()
        if അളവ്:
            return അളവ്
        time.sleep(0.05)
    raise AssertionError('സമയ_മൂല്യം 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        മോണിട്ടര്_പാത = 임시 / 'monitor.sock'
        ആജ്ഞ = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(മോണിട്ടര്_പാത) + ',server,nowait']
        ആജ്ഞ += ['-kernel', str(സ്ഥാനം / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(സ്ഥാനം / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        ആജ്ഞ += ['-S']
        പ്രോസസ്_മൂല്യം = subprocess.Popen(ആജ്ഞ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        മോണിട്ടര്_മൂല്യം = socket.socket(socket.AF_UNIX)
        ലോഗ്_രേഖ = bytearray()
        try:
            def 소켓준비():
                if പ്രോസസ്_മൂല്യം.poll() is not None:
                    raise AssertionError(പ്രോസസ്_മൂല്യം.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and മോണിട്ടര്_പാത.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            മോണിട്ടര്_മൂല്യം.connect(str(മോണിട്ടര്_പാത))
            직렬.setblocking(False)
            മോണിട്ടര്_മൂല്യം.sendall(b'cont\n')

            def 포함(സ്ട്രിംഗ്_മൂല്യം, നടപ്പിലാക്കുക=0):
                വായന, _, _ = select.select([직렬], [], [], 0.1)
                if വായന:
                    ഡാറ്റാ = 직렬.recv(65536)
                    if not ഡാറ്റാ:
                        raise AssertionError('직렬 കണക്ടു്_ചെയ്യുക പുറത്തുകടക്കൽ_പ്രോഗ്രാം')
                    ലോഗ്_രേഖ.extend(ഡാറ്റാ)
                if പ്രോസസ്_മൂല്യം.poll() is not None:
                    raise AssertionError('QEMU 비정상 പുറത്തുകടക്കൽ_പ്രോഗ്രാം: ' + str(പ്രോസസ്_മൂല്യം.returncode))
                return സ്ട്രിംഗ്_മൂല്യം.encode('utf-8') in ലോഗ്_രേഖ[നടപ്പിലാക്കുക:]

            def 명령시험(입력, 기대):
                നടപ്പിലാക്കുക = len(ലോഗ്_രേഖ)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, നടപ്പിലാക്കുക), 기대)
                기다리기(lambda: 포함('jkoros> ', നടപ്പിലാക്കുക), 'ആജ്ഞ 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in ലോഗ്_രേഖ
            assert '자바 기계어 കെര്_ണല്_മൂല്യം നടപ്പിലാക്കുക'.encode() in ലോഗ്_രേഖ
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for സൂചിക in range(8):
                명령시험('alloc\n', 'വിഭാഗം_മൂല്യം സൂചിക: ' + str(സൂചിക))
            명령시험('alloc\n', 'വിഭാഗം_മൂല്യം സൂചിക: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 വിഭാഗം_മൂല്യം')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'വിഭാഗം_മൂല്യം സൂചിക: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            നടപ്പിലാക്കുക = len(ലോഗ്_രേഖ)
            for കീ_മൂല്യം in ('i', 'n', 'f', 'o', 'ret'):
                മോണിട്ടര്_മൂല്യം.sendall(('sendkey ' + കീ_മൂല്യം + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', നടപ്പിലാക്കുക), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 ആജ്ഞ')
            assert b'PANIC' not in ലോഗ്_രേഖ and b'SELFTEST FAIL' not in ലോഗ്_രേഖ
            print('PASS: {} 부팅, Java 자체 시험, 직렬 ആജ്ഞ, PS/2 입력, അനുവദിക്കുക_സംഭരണം/반환, 정지'.format(종류))
            return ലോഗ്_രേഖ.decode('utf-8', 'replace')
        finally:
            직렬.close()
            മോണിട്ടര്_മൂല്യം.close()
            പ്രോസസ്_മൂല്യം.terminate()
            try:
                പ്രോസസ്_മൂല്യം.wait(timeout=3)
            except subprocess.TimeoutExpired:
                പ്രോസസ്_മൂല്യം.kill()
                പ്രോസസ്_മൂല്യം.wait()


if __name__ == '__main__':
    അളവ് = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (സ്ഥാനം / 'build/부팅시험.json').write_text(json.dumps(അളവ്, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
