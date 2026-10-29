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
        imonitha_indlela = 임시 / 'monitor.sock'
        Umyalelo = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(imonitha_indlela) + ',server,nowait']
        Umyalelo += ['-kernel', str(위치 / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(위치 / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        Umyalelo += ['-S']
        Inkqubo_ixabiso = subprocess.Popen(Umyalelo, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        imonitha_ixabiso = socket.socket(socket.AF_UNIX)
        ilog_umqolo = bytearray()
        try:
            def 소켓준비():
                if Inkqubo_ixabiso.poll() is not None:
                    raise AssertionError(Inkqubo_ixabiso.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and imonitha_indlela.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            imonitha_ixabiso.connect(str(imonitha_indlela))
            직렬.setblocking(False)
            imonitha_ixabiso.sendall(b'cont\n')

            def 포함(uluhlu_lweekharektha_ixabiso, Phumeza=0):
                Funda, _, _ = select.select([직렬], [], [], 0.1)
                if Funda:
                    iingcombolo = 직렬.recv(65536)
                    if not iingcombolo:
                        raise AssertionError('직렬 Nxulumanisa phuma_inkqubo')
                    ilog_umqolo.extend(iingcombolo)
                if Inkqubo_ixabiso.poll() is not None:
                    raise AssertionError('QEMU 비정상 phuma_inkqubo: ' + str(Inkqubo_ixabiso.returncode))
                return uluhlu_lweekharektha_ixabiso.encode('utf-8') in ilog_umqolo[Phumeza:]

            def 명령시험(입력, 기대):
                Phumeza = len(ilog_umqolo)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, Phumeza), 기대)
                기다리기(lambda: 포함('jkoros> ', Phumeza), 'Umyalelo 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in ilog_umqolo
            assert '자바 기계어 ikheneli_ixabiso Phumeza'.encode() in ilog_umqolo
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for indeksa in range(8):
                명령시험('alloc\n', 'icandelo_ixabiso indeksa: ' + str(indeksa))
            명령시험('alloc\n', 'icandelo_ixabiso indeksa: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 icandelo_ixabiso')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'icandelo_ixabiso indeksa: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Phumeza = len(ilog_umqolo)
            for iqhosha_ixabiso in ('i', 'n', 'f', 'o', 'ret'):
                imonitha_ixabiso.sendall(('sendkey ' + iqhosha_ixabiso + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', Phumeza), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 Umyalelo')
            assert b'PANIC' not in ilog_umqolo and b'SELFTEST FAIL' not in ilog_umqolo
            print('PASS: {} 부팅, Java 자체 시험, 직렬 Umyalelo, PS/2 입력, yabela_Ugcino/반환, 정지'.format(종류))
            return ilog_umqolo.decode('utf-8', 'replace')
        finally:
            직렬.close()
            imonitha_ixabiso.close()
            Inkqubo_ixabiso.terminate()
            try:
                Inkqubo_ixabiso.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Inkqubo_ixabiso.kill()
                Inkqubo_ixabiso.wait()


if __name__ == '__main__':
    결과 = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (위치 / 'build/부팅시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
