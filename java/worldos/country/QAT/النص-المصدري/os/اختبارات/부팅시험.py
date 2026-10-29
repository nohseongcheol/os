#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

موضع = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        نتيجة = 검사()
        if نتيجة:
            return نتيجة
        time.sleep(0.05)
    raise AssertionError('قيمة_الوقت 초과: ' + 설명)


def اختبارات(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        يراقب_مسار = 임시 / 'monitor.sock'
        أمر = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(يراقب_مسار) + ',server,nowait']
        أمر += ['-kernel', str(موضع / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(موضع / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        أمر += ['-S']
        عملية_قيمة = subprocess.Popen(أمر, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        يراقب_قيمة = socket.socket(socket.AF_UNIX)
        سجل_سجل = bytearray()
        try:
            def إعداد_مأخذ_التوصيل():
                if عملية_قيمة.poll() is not None:
                    raise AssertionError(عملية_قيمة.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and يراقب_مسار.exists()
            기다리기(إعداد_مأخذ_التوصيل, 'QEMU مأخذ_التوصيل_قيمة')
            직렬.connect(str(직렬경로))
            يراقب_قيمة.connect(str(يراقب_مسار))
            직렬.setblocking(False)
            يراقب_قيمة.sendall(b'cont\n')

            def تصريحات(سلسلة_قيمة, تشغيل=0):
                قراءة, _, _ = select.select([직렬], [], [], 0.1)
                if قراءة:
                    بيانات = 직렬.recv(65536)
                    if not بيانات:
                        raise AssertionError('직렬 اتصال خروج_تطبيق')
                    سجل_سجل.extend(بيانات)
                if عملية_قيمة.poll() is not None:
                    raise AssertionError('QEMU 비정상 خروج_تطبيق: ' + str(عملية_قيمة.returncode))
                return سلسلة_قيمة.encode('utf-8') in سجل_سجل[تشغيل:]

            def 명령시험(إدخال_قيمة, 기대):
                تشغيل = len(سجل_سجل)
                직렬.sendall(إدخال_قيمة.encode('ascii'))
                기다리기(lambda: تصريحات(기대, تشغيل), 기대)
                기다리기(lambda: تصريحات('jkoros> ', تشغيل), 'أمر 후 프롬프트')

            기다리기(lambda: تصريحات('READY'), 종류 + ' إقلاع_الآلة')
            assert b'JAVA SELFTEST PASS' in سجل_سجل
            assert '자바 기계어 نواة_قيمة تشغيل'.encode() in سجل_سجل
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for فهرس in range(8):
                명령시험('alloc\n', 'قسم_قيمة_366e0bfa فهرس: ' + str(فهرس))
            명령시험('alloc\n', 'قسم_قيمة_366e0bfa فهرس: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 قسم_قيمة_366e0bfa')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'قسم_قيمة_366e0bfa فهرس: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 رقم 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            تشغيل = len(سجل_سجل)
            for مفتاح_قيمة in ('i', 'n', 'f', 'o', 'ret'):
                يراقب_قيمة.sendall(('sendkey ' + مفتاح_قيمة + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: تصريحات('embedded subset JVM / polling kernel', تشغيل), 'PS/2 info إدخال_قيمة')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: تصريحات('HALTED'), '정지 أمر')
            assert b'PANIC' not in سجل_سجل and b'SELFTEST FAIL' not in سجل_سجل
            print('PASS: {} إقلاع_الآلة, Java ذاتي اختبارات, 직렬 أمر, PS/2 إدخال_قيمة, يخصص_تخزين/إرجاع_مقياس, 정지'.format(종류))
            return سجل_سجل.decode('utf-8', 'replace')
        finally:
            직렬.close()
            يراقب_قيمة.close()
            عملية_قيمة.terminate()
            try:
                عملية_قيمة.wait(timeout=3)
            except subprocess.TimeoutExpired:
                عملية_قيمة.kill()
                عملية_قيمة.wait()


if __name__ == '__main__':
    نتيجة = {종류: اختبارات(종류) for 종류 in ('elf', 'iso')}
    (موضع / 'build/부팅시험.json').write_text(json.dumps(نتيجة, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
