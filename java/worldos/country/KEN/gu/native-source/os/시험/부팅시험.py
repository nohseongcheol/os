#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

સ્થાન = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        પરિમાણ = 검사()
        if પરિમાણ:
            return પરિમાણ
        time.sleep(0.05)
    raise AssertionError('સમય_મૂલ્ય 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        મૉનિટર_પાથ = 임시 / 'monitor.sock'
        આદેશ = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(મૉનિટર_પાથ) + ',server,nowait']
        આદેશ += ['-kernel', str(સ્થાન / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(સ્થાન / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        આદેશ += ['-S']
        પ્રક્રિયા_મૂલ્ય = subprocess.Popen(આદેશ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        મૉનિટર_મૂલ્ય = socket.socket(socket.AF_UNIX)
        લૉગ_પંક્તિ = bytearray()
        try:
            def 소켓준비():
                if પ્રક્રિયા_મૂલ્ય.poll() is not None:
                    raise AssertionError(પ્રક્રિયા_મૂલ્ય.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and મૉનિટર_પાથ.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            મૉનિટર_મૂલ્ય.connect(str(મૉનિટર_પાથ))
            직렬.setblocking(False)
            મૉનિટર_મૂલ્ય.sendall(b'cont\n')

            def 포함(સ્ટ્રિંગ_મૂલ્ય, ચલાવો_2=0):
                વાંચો, _, _ = select.select([직렬], [], [], 0.1)
                if વાંચો:
                    ડેટા = 직렬.recv(65536)
                    if not ડેટા:
                        raise AssertionError('직렬 સંપર્ક_કરો પ્રસ્થાન_એપ્લિકેશન')
                    લૉગ_પંક્તિ.extend(ડેટા)
                if પ્રક્રિયા_મૂલ્ય.poll() is not None:
                    raise AssertionError('QEMU 비정상 પ્રસ્થાન_એપ્લિકેશન: ' + str(પ્રક્રિયા_મૂલ્ય.returncode))
                return સ્ટ્રિંગ_મૂલ્ય.encode('utf-8') in લૉગ_પંક્તિ[ચલાવો_2:]

            def 명령시험(입력, 기대):
                ચલાવો_2 = len(લૉગ_પંક્તિ)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, ચલાવો_2), 기대)
                기다리기(lambda: 포함('jkoros> ', ચલાવો_2), 'આદેશ 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in લૉગ_પંક્તિ
            assert '자바 기계어 કર્નેલ_મૂલ્ય ચલાવો_2'.encode() in લૉગ_પંક્તિ
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for અનુક્રમણિકા in range(8):
                명령시험('alloc\n', 'અનુભાગ_મૂલ્ય અનુક્રમણિકા: ' + str(અનુક્રમણિકા))
            명령시험('alloc\n', 'અનુભાગ_મૂલ્ય અનુક્રમણિકા: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 અનુભાગ_મૂલ્ય')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'અનુભાગ_મૂલ્ય અનુક્રમણિકા: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            ચલાવો_2 = len(લૉગ_પંક્તિ)
            for કી_મૂલ્ય in ('i', 'n', 'f', 'o', 'ret'):
                મૉનિટર_મૂલ્ય.sendall(('sendkey ' + કી_મૂલ્ય + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', ચલાવો_2), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 આદેશ')
            assert b'PANIC' not in લૉગ_પંક્તિ and b'SELFTEST FAIL' not in લૉગ_પંક્તિ
            print('PASS: {} 부팅, Java 자체 시험, 직렬 આદેશ, PS/2 입력, ફાળવો_સંગ્રહ/반환, 정지'.format(종류))
            return લૉગ_પંક્તિ.decode('utf-8', 'replace')
        finally:
            직렬.close()
            મૉનિટર_મૂલ્ય.close()
            પ્રક્રિયા_મૂલ્ય.terminate()
            try:
                પ્રક્રિયા_મૂલ્ય.wait(timeout=3)
            except subprocess.TimeoutExpired:
                પ્રક્રિયા_મૂલ્ય.kill()
                પ્રક્રિયા_મૂલ્ય.wait()


if __name__ == '__main__':
    પરિમાણ = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (સ્થાન / 'build/부팅시험.json').write_text(json.dumps(પરિમાણ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
