#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

ตําแหน่ง = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        ผลลัพธ์ = 검사()
        if ผลลัพธ์:
            return ผลลัพธ์
        time.sleep(0.05)
    raise AssertionError('ค่าเวลา 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        จอภาพ_พาธ = 임시 / 'monitor.sock'
        คําสั่ง = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(จอภาพ_พาธ) + ',server,nowait']
        คําสั่ง += ['-kernel', str(ตําแหน่ง / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(ตําแหน่ง / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        คําสั่ง += ['-S']
        กระบวนการ_ค่า = subprocess.Popen(คําสั่ง, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        จอภาพ_ค่า = socket.socket(socket.AF_UNIX)
        บันทึก_สถิติ = bytearray()
        try:
            def 소켓준비():
                if กระบวนการ_ค่า.poll() is not None:
                    raise AssertionError(กระบวนการ_ค่า.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and จอภาพ_พาธ.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            จอภาพ_ค่า.connect(str(จอภาพ_พาธ))
            직렬.setblocking(False)
            จอภาพ_ค่า.sendall(b'cont\n')

            def 포함(สตริง_ค่า, เรียกใช้งาน=0):
                อ่าน, _, _ = select.select([직렬], [], [], 0.1)
                if อ่าน:
                    ข้อมูล = 직렬.recv(65536)
                    if not ข้อมูล:
                        raise AssertionError('직렬 เชื่อมต่อ ออก_แอป')
                    บันทึก_สถิติ.extend(ข้อมูล)
                if กระบวนการ_ค่า.poll() is not None:
                    raise AssertionError('QEMU 비정상 ออก_แอป: ' + str(กระบวนการ_ค่า.returncode))
                return สตริง_ค่า.encode('utf-8') in บันทึก_สถิติ[เรียกใช้งาน:]

            def 명령시험(입력, 기대):
                เรียกใช้งาน = len(บันทึก_สถิติ)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, เรียกใช้งาน), 기대)
                기다리기(lambda: 포함('jkoros> ', เรียกใช้งาน), 'คําสั่ง 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in บันทึก_สถิติ
            assert '자바 기계어 เคอร์เนล_ค่า เรียกใช้งาน'.encode() in บันทึก_สถิติ
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for ดัชนี in range(8):
                명령시험('alloc\n', 'ส่วน_ค่า ดัชนี: ' + str(ดัชนี))
            명령시험('alloc\n', 'ส่วน_ค่า ดัชนี: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 ส่วน_ค่า')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'ส่วน_ค่า ดัชนี: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 หมายเลข 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            เรียกใช้งาน = len(บันทึก_สถิติ)
            for คีย์_ค่า in ('i', 'n', 'f', 'o', 'ret'):
                จอภาพ_ค่า.sendall(('sendkey ' + คีย์_ค่า + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', เรียกใช้งาน), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 คําสั่ง')
            assert b'PANIC' not in บันทึก_สถิติ and b'SELFTEST FAIL' not in บันทึก_สถิติ
            print('PASS: {} 부팅, Java เอง 시험, 직렬 คําสั่ง, PS/2 입력, จัดสรร_ที่เก็บ/ส่งคืน_เมตริก, 정지'.format(종류))
            return บันทึก_สถิติ.decode('utf-8', 'replace')
        finally:
            직렬.close()
            จอภาพ_ค่า.close()
            กระบวนการ_ค่า.terminate()
            try:
                กระบวนการ_ค่า.wait(timeout=3)
            except subprocess.TimeoutExpired:
                กระบวนการ_ค่า.kill()
                กระบวนการ_ค่า.wait()


if __name__ == '__main__':
    ผลลัพธ์ = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (ตําแหน่ง / 'build/부팅시험.json').write_text(json.dumps(ผลลัพธ์, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
