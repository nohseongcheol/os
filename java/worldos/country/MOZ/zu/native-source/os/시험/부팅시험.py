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
        imonitha_umzila = 임시 / 'monitor.sock'
        Umlayelo = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(imonitha_umzila) + ',server,nowait']
        Umlayelo += ['-kernel', str(위치 / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(위치 / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        Umlayelo += ['-S']
        Inqubo_inani = subprocess.Popen(Umlayelo, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        imonitha_inani = socket.socket(socket.AF_UNIX)
        loga_umugqa = bytearray()
        try:
            def 소켓준비():
                if Inqubo_inani.poll() is not None:
                    raise AssertionError(Inqubo_inani.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and imonitha_umzila.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            imonitha_inani.connect(str(imonitha_umzila))
            직렬.setblocking(False)
            imonitha_inani.sendall(b'cont\n')

            def 포함(uchunge_inani, Sebenzisa=0):
                Funda, _, _ = select.select([직렬], [], [], 0.1)
                if Funda:
                    imininingwane = 직렬.recv(65536)
                    if not imininingwane:
                        raise AssertionError('직렬 Xhumanisa phuma_i_app')
                    loga_umugqa.extend(imininingwane)
                if Inqubo_inani.poll() is not None:
                    raise AssertionError('QEMU 비정상 phuma_i_app: ' + str(Inqubo_inani.returncode))
                return uchunge_inani.encode('utf-8') in loga_umugqa[Sebenzisa:]

            def 명령시험(입력, 기대):
                Sebenzisa = len(loga_umugqa)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, Sebenzisa), 기대)
                기다리기(lambda: 포함('jkoros> ', Sebenzisa), 'Umlayelo 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in loga_umugqa
            assert '자바 기계어 ikhenela_inani Sebenzisa'.encode() in loga_umugqa
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for thola_inkomba in range(8):
                명령시험('alloc\n', 'isigaba_inani thola_inkomba: ' + str(thola_inkomba))
            명령시험('alloc\n', 'isigaba_inani thola_inkomba: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 isigaba_inani')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'isigaba_inani thola_inkomba: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Sebenzisa = len(loga_umugqa)
            for inkomba_inani in ('i', 'n', 'f', 'o', 'ret'):
                imonitha_inani.sendall(('sendkey ' + inkomba_inani + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', Sebenzisa), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 Umlayelo')
            assert b'PANIC' not in loga_umugqa and b'SELFTEST FAIL' not in loga_umugqa
            print('PASS: {} 부팅, Java 자체 시험, 직렬 Umlayelo, PS/2 입력, abela_Indawo_yokugcina/반환, 정지'.format(종류))
            return loga_umugqa.decode('utf-8', 'replace')
        finally:
            직렬.close()
            imonitha_inani.close()
            Inqubo_inani.terminate()
            try:
                Inqubo_inani.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Inqubo_inani.kill()
                Inqubo_inani.wait()


if __name__ == '__main__':
    결과 = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (위치 / 'build/부팅시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
