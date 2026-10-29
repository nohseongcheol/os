#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

مرتب_کردن = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        سنجش = 검사()
        if سنجش:
            return سنجش
        time.sleep(0.05)
    raise AssertionError('زمان_مقدار 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        مانیتور_مسیر = 임시 / 'monitor.sock'
        فرمان = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(مانیتور_مسیر) + ',server,nowait']
        فرمان += ['-kernel', str(مرتب_کردن / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(مرتب_کردن / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        فرمان += ['-S']
        فرآیند_مقدار = subprocess.Popen(فرمان, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        مانیتور_مقدار = socket.socket(socket.AF_UNIX)
        واقعه_نگار_ردیف = bytearray()
        try:
            def 소켓준비():
                if فرآیند_مقدار.poll() is not None:
                    raise AssertionError(فرآیند_مقدار.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and مانیتور_مسیر.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            مانیتور_مقدار.connect(str(مانیتور_مسیر))
            직렬.setblocking(False)
            مانیتور_مقدار.sendall(b'cont\n')

            def 포함(رشته_مقدار_6ca8363c, اجرا_2=0):
                خواندن, _, _ = select.select([직렬], [], [], 0.1)
                if خواندن:
                    داده_ها = 직렬.recv(65536)
                    if not داده_ها:
                        raise AssertionError('직렬 اتصال خروج_برنامه')
                    واقعه_نگار_ردیف.extend(داده_ها)
                if فرآیند_مقدار.poll() is not None:
                    raise AssertionError('QEMU 비정상 خروج_برنامه: ' + str(فرآیند_مقدار.returncode))
                return رشته_مقدار_6ca8363c.encode('utf-8') in واقعه_نگار_ردیف[اجرا_2:]

            def 명령시험(입력, 기대):
                اجرا_2 = len(واقعه_نگار_ردیف)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, اجرا_2), 기대)
                기다리기(lambda: 포함('jkoros> ', اجرا_2), 'فرمان 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in واقعه_نگار_ردیف
            assert '자바 기계어 هسته_مقدار اجرا_2'.encode() in واقعه_نگار_ردیف
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for فهرست in range(8):
                명령시험('alloc\n', 'قسمت_مقدار فهرست: ' + str(فهرست))
            명령시험('alloc\n', 'قسمت_مقدار فهرست: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 قسمت_مقدار')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'قسمت_مقدار فهرست: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            اجرا_2 = len(واقعه_نگار_ردیف)
            for کلید_مقدار in ('i', 'n', 'f', 'o', 'ret'):
                مانیتور_مقدار.sendall(('sendkey ' + کلید_مقدار + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', اجرا_2), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 فرمان')
            assert b'PANIC' not in واقعه_نگار_ردیف and b'SELFTEST FAIL' not in واقعه_نگار_ردیف
            print('PASS: {} 부팅, Java بومی 시험, 직렬 فرمان, PS/2 입력, اختصاص_دادن_حافظه_تلفن/بازگرداندن_سنجش, 정지'.format(종류))
            return واقعه_نگار_ردیف.decode('utf-8', 'replace')
        finally:
            직렬.close()
            مانیتور_مقدار.close()
            فرآیند_مقدار.terminate()
            try:
                فرآیند_مقدار.wait(timeout=3)
            except subprocess.TimeoutExpired:
                فرآیند_مقدار.kill()
                فرآیند_مقدار.wait()


if __name__ == '__main__':
    سنجش = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (مرتب_کردن / 'build/부팅시험.json').write_text(json.dumps(سنجش, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
