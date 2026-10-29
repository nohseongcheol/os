#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

స్థానము = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        ప్రమాణం = 검사()
        if ప్రమాణం:
            return ప్రమాణం
        time.sleep(0.05)
    raise AssertionError('సమయం_మూల్యం 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        మానిటర్_పథం = 임시 / 'monitor.sock'
        ఆదేశము = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(మానిటర్_పథం) + ',server,nowait']
        ఆదేశము += ['-kernel', str(స్థానము / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(స్థానము / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        ఆదేశము += ['-S']
        విధానం_మూల్యం = subprocess.Popen(ఆదేశము, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        మానిటర్_మూల్యం = socket.socket(socket.AF_UNIX)
        లాగ్_వరుస = bytearray()
        try:
            def 소켓준비():
                if విధానం_మూల్యం.poll() is not None:
                    raise AssertionError(విధానం_మూల్యం.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and మానిటర్_పథం.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            మానిటర్_మూల్యం.connect(str(మానిటర్_పథం))
            직렬.setblocking(False)
            మానిటర్_మూల్యం.sendall(b'cont\n')

            def 포함(అక్షరసరం_మూల్యం, నడుపుము=0):
                చదువు, _, _ = select.select([직렬], [], [], 0.1)
                if చదువు:
                    డేటా = 직렬.recv(65536)
                    if not డేటా:
                        raise AssertionError('직렬 కనెక్టుచేయి నిష్క్రమణ_అనువర్తనం')
                    లాగ్_వరుస.extend(డేటా)
                if విధానం_మూల్యం.poll() is not None:
                    raise AssertionError('QEMU 비정상 నిష్క్రమణ_అనువర్తనం: ' + str(విధానం_మూల్యం.returncode))
                return అక్షరసరం_మూల్యం.encode('utf-8') in లాగ్_వరుస[నడుపుము:]

            def 명령시험(입력, 기대):
                నడుపుము = len(లాగ్_వరుస)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, నడుపుము), 기대)
                기다리기(lambda: 포함('jkoros> ', నడుపుము), 'ఆదేశము 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in లాగ్_వరుస
            assert '자바 기계어 కెర్నల్_మూల్యం నడుపుము'.encode() in లాగ్_వరుస
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for సూచీ in range(8):
                명령시험('alloc\n', 'విభాగం_మూల్యం సూచీ: ' + str(సూచీ))
            명령시험('alloc\n', 'విభాగం_మూల్యం సూచీ: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 విభాగం_మూల్యం')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'విభాగం_మూల్యం సూచీ: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            నడుపుము = len(లాగ్_వరుస)
            for కీ_మూల్యం in ('i', 'n', 'f', 'o', 'ret'):
                మానిటర్_మూల్యం.sendall(('sendkey ' + కీ_మూల్యం + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', నడుపుము), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 ఆదేశము')
            assert b'PANIC' not in లాగ్_వరుస and b'SELFTEST FAIL' not in లాగ్_వరుస
            print('PASS: {} 부팅, Java 자체 시험, 직렬 ఆదేశము, PS/2 입력, కేటాయించు_నిల్వ/반환, 정지'.format(종류))
            return లాగ్_వరుస.decode('utf-8', 'replace')
        finally:
            직렬.close()
            మానిటర్_మూల్యం.close()
            విధానం_మూల్యం.terminate()
            try:
                విధానం_మూల్యం.wait(timeout=3)
            except subprocess.TimeoutExpired:
                విధానం_మూల్యం.kill()
                విధానం_మూల్యం.wait()


if __name__ == '__main__':
    ప్రమాణం = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (స్థానము / 'build/부팅시험.json').write_text(json.dumps(ప్రమాణం, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
