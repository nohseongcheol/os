#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

პოზიცია = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        გაზომვა = 검사()
        if გაზომვა:
            return გაზომვა
        time.sleep(0.05)
    raise AssertionError('დრო_მნიშვნელობა 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        მონიტორი_მდებარეობა = 임시 / 'monitor.sock'
        ბრძანება = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(მონიტორი_მდებარეობა) + ',server,nowait']
        ბრძანება += ['-kernel', str(პოზიცია / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(პოზიცია / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        ბრძანება += ['-S']
        პროცესი_მნიშვნელობა = subprocess.Popen(ბრძანება, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        მონიტორი_მნიშვნელობა = socket.socket(socket.AF_UNIX)
        ჟურნალი_ჩაწერა = bytearray()
        try:
            def 소켓준비():
                if პროცესი_მნიშვნელობა.poll() is not None:
                    raise AssertionError(პროცესი_მნიშვნელობა.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and მონიტორი_მდებარეობა.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            მონიტორი_მნიშვნელობა.connect(str(მონიტორი_მდებარეობა))
            직렬.setblocking(False)
            მონიტორი_მნიშვნელობა.sendall(b'cont\n')

            def 포함(სტრიქონი_მნიშვნელობა, გაშვება=0):
                კითხვა, _, _ = select.select([직렬], [], [], 0.1)
                if კითხვა:
                    მონაცემები = 직렬.recv(65536)
                    if not მონაცემები:
                        raise AssertionError('직렬 დაკავშირება გასვლა_აპი')
                    ჟურნალი_ჩაწერა.extend(მონაცემები)
                if პროცესი_მნიშვნელობა.poll() is not None:
                    raise AssertionError('QEMU 비정상 გასვლა_აპი: ' + str(პროცესი_მნიშვნელობა.returncode))
                return სტრიქონი_მნიშვნელობა.encode('utf-8') in ჟურნალი_ჩაწერა[გაშვება:]

            def 명령시험(입력, 기대):
                გაშვება = len(ჟურნალი_ჩაწერა)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, გაშვება), 기대)
                기다리기(lambda: 포함('jkoros> ', გაშვება), 'ბრძანება 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in ჟურნალი_ჩაწერა
            assert '자바 기계어 ბირთვი_მნიშვნელობა გაშვება'.encode() in ჟურნალი_ჩაწერა
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for ინდექსი in range(8):
                명령시험('alloc\n', 'სექცია_მნიშვნელობა ინდექსი: ' + str(ინდექსი))
            명령시험('alloc\n', 'სექცია_მნიშვნელობა ინდექსი: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 სექცია_მნიშვნელობა')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'სექცია_მნიშვნელობა ინდექსი: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            გაშვება = len(ჟურნალი_ჩაწერა)
            for კლავიში_მნიშვნელობა in ('i', 'n', 'f', 'o', 'ret'):
                მონიტორი_მნიშვნელობა.sendall(('sendkey ' + კლავიში_მნიშვნელობა + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', გაშვება), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 ბრძანება')
            assert b'PANIC' not in ჟურნალი_ჩაწერა and b'SELFTEST FAIL' not in ჟურნალი_ჩაწერა
            print('PASS: {} 부팅, Java 자체 시험, 직렬 ბრძანება, PS/2 입력, გამოყოფა_საცავი/დაბრუნება_გაზომვა, 정지'.format(종류))
            return ჟურნალი_ჩაწერა.decode('utf-8', 'replace')
        finally:
            직렬.close()
            მონიტორი_მნიშვნელობა.close()
            პროცესი_მნიშვნელობა.terminate()
            try:
                პროცესი_მნიშვნელობა.wait(timeout=3)
            except subprocess.TimeoutExpired:
                პროცესი_მნიშვნელობა.kill()
                პროცესი_მნიშვნელობა.wait()


if __name__ == '__main__':
    გაზომვა = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (პოზიცია / 'build/부팅시험.json').write_text(json.dumps(გაზომვა, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
