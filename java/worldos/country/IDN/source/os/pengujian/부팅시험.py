#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

posisi = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        hasil = 검사()
        if hasil:
            return hasil
        time.sleep(0.05)
    raise AssertionError('TIME_VALUE 초과: ' + 설명)


def pengujian(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        pantau_jalur = 임시 / 'monitor.sock'
        perintah = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(pantau_jalur) + ',server,nowait']
        perintah += ['-kernel', str(posisi / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(posisi / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        perintah += ['-S']
        Proses_VALUE = subprocess.Popen(perintah, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        pantau_VALUE = socket.socket(socket.AF_UNIX)
        LOG_baris = bytearray()
        try:
            def 소켓준비():
                if Proses_VALUE.poll() is not None:
                    raise AssertionError(Proses_VALUE.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and pantau_jalur.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            pantau_VALUE.connect(str(pantau_jalur))
            직렬.setblocking(False)
            pantau_VALUE.sendall(b'cont\n')

            def deklarasi(string_VALUE, jalankan=0):
                Baca, _, _ = select.select([직렬], [], [], 0.1)
                if Baca:
                    data = 직렬.recv(65536)
                    if not data:
                        raise AssertionError('직렬 Sambung Keluar_apl')
                    LOG_baris.extend(data)
                if Proses_VALUE.poll() is not None:
                    raise AssertionError('QEMU 비정상 Keluar_apl: ' + str(Proses_VALUE.returncode))
                return string_VALUE.encode('utf-8') in LOG_baris[jalankan:]

            def 명령시험(입력, 기대):
                jalankan = len(LOG_baris)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: deklarasi(기대, jalankan), 기대)
                기다리기(lambda: deklarasi('jkoros> ', jalankan), 'perintah 후 프롬프트')

            기다리기(lambda: deklarasi('READY'), 종류 + ' awal_mesin')
            assert b'JAVA SELFTEST PASS' in LOG_baris
            assert '자바 기계어 kernel_VALUE jalankan'.encode() in LOG_baris
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for INDEX in range(8):
                명령시험('alloc\n', 'seksi_VALUE INDEX: ' + str(INDEX))
            명령시험('alloc\n', 'seksi_VALUE INDEX: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 seksi_VALUE')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'seksi_VALUE INDEX: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            jalankan = len(LOG_baris)
            for Kunci_VALUE in ('i', 'n', 'f', 'o', 'ret'):
                pantau_VALUE.sendall(('sendkey ' + Kunci_VALUE + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: deklarasi('embedded subset JVM / polling kernel', jalankan), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: deklarasi('HALTED'), '정지 perintah')
            assert b'PANIC' not in LOG_baris and b'SELFTEST FAIL' not in LOG_baris
            print('PASS: {} awal_mesin, Java Asli pengujian, 직렬 perintah, PS/2 입력, alokasi_Storage/kembalikan_KR, 정지'.format(종류))
            return LOG_baris.decode('utf-8', 'replace')
        finally:
            직렬.close()
            pantau_VALUE.close()
            Proses_VALUE.terminate()
            try:
                Proses_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Proses_VALUE.kill()
                Proses_VALUE.wait()


if __name__ == '__main__':
    hasil = {종류: pengujian(종류) for 종류 in ('elf', 'iso')}
    (posisi / 'build/부팅시험.json').write_text(json.dumps(hasil, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
