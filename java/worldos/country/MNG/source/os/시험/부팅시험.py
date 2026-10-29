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
        хяналтын_төхөөрөмж_зам = 임시 / 'monitor.sock'
        Тушаал = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(хяналтын_төхөөрөмж_зам) + ',server,nowait']
        Тушаал += ['-kernel', str(위치 / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(위치 / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        Тушаал += ['-S']
        үйл_явц_утга = subprocess.Popen(Тушаал, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        хяналтын_төхөөрөмж_утга = socket.socket(socket.AF_UNIX)
        бичих_мөр_6e8b375a = bytearray()
        try:
            def 소켓준비():
                if үйл_явц_утга.poll() is not None:
                    raise AssertionError(үйл_явц_утга.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and хяналтын_төхөөрөмж_зам.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            хяналтын_төхөөрөмж_утга.connect(str(хяналтын_төхөөрөмж_зам))
            직렬.setblocking(False)
            хяналтын_төхөөрөмж_утга.sendall(b'cont\n')

            def 포함(мөр_утга_6ca8363c, Ажиллуулах=0):
                Унших, _, _ = select.select([직렬], [], [], 0.1)
                if Унших:
                    өгөгдөл = 직렬.recv(65536)
                    if not өгөгдөл:
                        raise AssertionError('직렬 Холбох Гарах_програм')
                    бичих_мөр_6e8b375a.extend(өгөгдөл)
                if үйл_явц_утга.poll() is not None:
                    raise AssertionError('QEMU 비정상 Гарах_програм: ' + str(үйл_явц_утга.returncode))
                return мөр_утга_6ca8363c.encode('utf-8') in бичих_мөр_6e8b375a[Ажиллуулах:]

            def 명령시험(입력, 기대):
                Ажиллуулах = len(бичих_мөр_6e8b375a)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, Ажиллуулах), 기대)
                기다리기(lambda: 포함('jkoros> ', Ажиллуулах), 'Тушаал 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in бичих_мөр_6e8b375a
            assert '자바 기계어 кернел_утга Ажиллуулах'.encode() in бичих_мөр_6e8b375a
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for индекс in range(8):
                명령시험('alloc\n', 'хэсэг_утга индекс: ' + str(индекс))
            명령시험('alloc\n', 'хэсэг_утга индекс: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 хэсэг_утга')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'хэсэг_утга индекс: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Ажиллуулах = len(бичих_мөр_6e8b375a)
            for түлхүүр_утга in ('i', 'n', 'f', 'o', 'ret'):
                хяналтын_төхөөрөмж_утга.sendall(('sendkey ' + түлхүүр_утга + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', Ажиллуулах), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 Тушаал')
            assert b'PANIC' not in бичих_мөр_6e8b375a and b'SELFTEST FAIL' not in бичих_мөр_6e8b375a
            print('PASS: {} 부팅, Java 자체 시험, 직렬 Тушаал, PS/2 입력, хуваарилах_Санах_ой/반환, 정지'.format(종류))
            return бичих_мөр_6e8b375a.decode('utf-8', 'replace')
        finally:
            직렬.close()
            хяналтын_төхөөрөмж_утга.close()
            үйл_явц_утга.terminate()
            try:
                үйл_явц_утга.wait(timeout=3)
            except subprocess.TimeoutExpired:
                үйл_явц_утга.kill()
                үйл_явц_утга.wait()


if __name__ == '__main__':
    결과 = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (위치 / 'build/부팅시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
