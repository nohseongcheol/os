#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

Θέση = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        μέτρηση = 검사()
        if μέτρηση:
            return μέτρηση
        time.sleep(0.05)
    raise AssertionError('τιμή_ώρας 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        οθόνη_διαδρομή = 임시 / 'monitor.sock'
        Εντολή = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(οθόνη_διαδρομή) + ',server,nowait']
        Εντολή += ['-kernel', str(Θέση / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(Θέση / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        Εντολή += ['-S']
        διεργασία_τιμή = subprocess.Popen(Εντολή, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        οθόνη_τιμή = socket.socket(socket.AF_UNIX)
        καταγράφω_ρεκόρ = bytearray()
        try:
            def Προετοίμασε_υποδοχή():
                if διεργασία_τιμή.poll() is not None:
                    raise AssertionError(διεργασία_τιμή.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and οθόνη_διαδρομή.exists()
            기다리기(Προετοίμασε_υποδοχή, 'QEMU υποδοχή_τιμή')
            직렬.connect(str(직렬경로))
            οθόνη_τιμή.connect(str(οθόνη_διαδρομή))
            직렬.setblocking(False)
            οθόνη_τιμή.sendall(b'cont\n')

            def 포함(συμβολοσειρά_τιμή, Εκτέλεση_2=0):
                Ανάγνωση, _, _ = select.select([직렬], [], [], 0.1)
                if Ανάγνωση:
                    δεδομένα = 직렬.recv(65536)
                    if not δεδομένα:
                        raise AssertionError('직렬 Σύνδεση Έξοδος_εφαρμογή')
                    καταγράφω_ρεκόρ.extend(δεδομένα)
                if διεργασία_τιμή.poll() is not None:
                    raise AssertionError('QEMU 비정상 Έξοδος_εφαρμογή: ' + str(διεργασία_τιμή.returncode))
                return συμβολοσειρά_τιμή.encode('utf-8') in καταγράφω_ρεκόρ[Εκτέλεση_2:]

            def 명령시험(είσοδος_τιμή, 기대):
                Εκτέλεση_2 = len(καταγράφω_ρεκόρ)
                직렬.sendall(είσοδος_τιμή.encode('ascii'))
                기다리기(lambda: 포함(기대, Εκτέλεση_2), 기대)
                기다리기(lambda: 포함('jkoros> ', Εκτέλεση_2), 'Εντολή 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in καταγράφω_ρεκόρ
            assert '자바 기계어 πυρήνας_τιμή Εκτέλεση_2'.encode() in καταγράφω_ρεκόρ
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for Ευρετήριο in range(8):
                명령시험('alloc\n', 'ενότητα_τιμή Ευρετήριο: ' + str(Ευρετήριο))
            명령시험('alloc\n', 'ενότητα_τιμή Ευρετήριο: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 ενότητα_τιμή')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'ενότητα_τιμή Ευρετήριο: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Εκτέλεση_2 = len(καταγράφω_ρεκόρ)
            for Κλειδί_τιμή in ('i', 'n', 'f', 'o', 'ret'):
                οθόνη_τιμή.sendall(('sendkey ' + Κλειδί_τιμή + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', Εκτέλεση_2), 'PS/2 info είσοδος_τιμή')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 Εντολή')
            assert b'PANIC' not in καταγράφω_ρεκόρ and b'SELFTEST FAIL' not in καταγράφω_ρεκόρ
            print('PASS: {} 부팅, Java ίδιο 시험, 직렬 Εντολή, PS/2 είσοδος_τιμή, εκχωρώ_Χώρος_αποθήκευσης/επιστρέφω_μέτρηση, 정지'.format(종류))
            return καταγράφω_ρεκόρ.decode('utf-8', 'replace')
        finally:
            직렬.close()
            οθόνη_τιμή.close()
            διεργασία_τιμή.terminate()
            try:
                διεργασία_τιμή.wait(timeout=3)
            except subprocess.TimeoutExpired:
                διεργασία_τιμή.kill()
                διεργασία_τιμή.wait()


if __name__ == '__main__':
    μέτρηση = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (Θέση / 'build/부팅시험.json').write_text(json.dumps(μέτρηση, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
