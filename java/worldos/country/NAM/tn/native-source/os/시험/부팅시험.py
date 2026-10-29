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
        monithara_tsela = 임시 / 'monitor.sock'
        Taelo = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monithara_tsela) + ',server,nowait']
        Taelo += ['-kernel', str(위치 / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(위치 / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        Taelo += ['-S']
        Thulaganyo_Boleng = subprocess.Popen(Taelo, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        monithara_Boleng = socket.socket(socket.AF_UNIX)
        rekota_mola = bytearray()
        try:
            def 소켓준비():
                if Thulaganyo_Boleng.poll() is not None:
                    raise AssertionError(Thulaganyo_Boleng.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and monithara_tsela.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            monithara_Boleng.connect(str(monithara_tsela))
            직렬.setblocking(False)
            monithara_Boleng.sendall(b'cont\n')

            def 포함(dikwalwa_Boleng, dirisa=0):
                읽기, _, _ = select.select([직렬], [], [], 0.1)
                if 읽기:
                    tshedimosetso = 직렬.recv(65536)
                    if not tshedimosetso:
                        raise AssertionError('직렬 Golaganya tswaya_Tiriso')
                    rekota_mola.extend(tshedimosetso)
                if Thulaganyo_Boleng.poll() is not None:
                    raise AssertionError('QEMU 비정상 tswaya_Tiriso: ' + str(Thulaganyo_Boleng.returncode))
                return dikwalwa_Boleng.encode('utf-8') in rekota_mola[dirisa:]

            def 명령시험(입력, 기대):
                dirisa = len(rekota_mola)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, dirisa), 기대)
                기다리기(lambda: 포함('jkoros> ', dirisa), 'Taelo 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in rekota_mola
            assert '자바 기계어 Khenele_Boleng dirisa'.encode() in rekota_mola
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for tshupane in range(8):
                명령시험('alloc\n', 'karolo_Boleng tshupane: ' + str(tshupane))
            명령시험('alloc\n', 'karolo_Boleng tshupane: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 karolo_Boleng')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'karolo_Boleng tshupane: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            dirisa = len(rekota_mola)
            for taetsi_Boleng in ('i', 'n', 'f', 'o', 'ret'):
                monithara_Boleng.sendall(('sendkey ' + taetsi_Boleng + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', dirisa), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 Taelo')
            assert b'PANIC' not in rekota_mola and b'SELFTEST FAIL' not in rekota_mola
            print('PASS: {} 부팅, Java 자체 시험, 직렬 Taelo, PS/2 입력, abela_Polokelo/반환, 정지'.format(종류))
            return rekota_mola.decode('utf-8', 'replace')
        finally:
            직렬.close()
            monithara_Boleng.close()
            Thulaganyo_Boleng.terminate()
            try:
                Thulaganyo_Boleng.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Thulaganyo_Boleng.kill()
                Thulaganyo_Boleng.wait()


if __name__ == '__main__':
    결과 = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (위치 / 'build/부팅시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
