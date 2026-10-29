#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. host 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from Jalankan_perintah import perintah


def jalankan():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('arguments', nargs='*')
    parser.add_argument('--class-name', help='패키지가 있는 .class의 전체 Nama_2(예: validasi.꾸러미시험)')
    parser.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI gunakan_VALUE')
    parser.add_argument('--vnc', help='예: 127.0.0.1:2')
    parser.add_argument('--include', action='append', type=Path, default=[], help='tambah_entri class berkas 또는 class 디렉터리(패키지 Nama_2 유지)')
    argumen_ARRAY = parser.parse_args()
    data = argumen_ARRAY.file.read_bytes()
    if argumen_ARRAY.class_name and argumen_ARRAY.file.suffix != '.class': parser.error('--class-name은 .class 입력에서 사용합니다.')
    Nama_2 = argumen_ARRAY.class_name + '.class' if argumen_ARRAY.class_name else argumen_ARRAY.file.name
    if len(data) > 16384 or not 1 <= len(Nama_2.encode('utf-8')) <= 63 or '\n' in Nama_2 or '\r' in Nama_2:
        parser.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    area_VALUE = '.elf' if data[:4] == b'\x7fELF' else argumen_ARRAY.file.suffix
    if argumen_ARRAY.linux and area_VALUE != '.elf': parser.error('--linux는 ELF 바이너리에만 사용합니다.')
    if area_VALUE not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        parser.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argumen_ARRAY.arguments) > 7 or any(len(string_data.encode('utf-8')) > 255 or '\n' in string_data or '\r' in string_data for string_data in argumen_ARRAY.arguments):
        parser.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Opsi = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argumen_ARRAY.vnc: Opsi += ['-vnc', argumen_ARRAY.vnc]
    Proses = subprocess.Popen(perintah() + Opsi, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    pemilih = selectors.DefaultSelector(); pemilih.register(Proses.stdout, selectors.EVENT_READ)
    def terima_email(확인표시, 시간제한=45):
        출력결과 = bytearray(); mengakhiri_OFFSET = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > mengakhiri_OFFSET: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in pemilih.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Proses.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def kirim(baris_masukan, 확인표시=b'jkoros-native> '):
        Proses.stdin.write(baris_masukan.encode('utf-8') + b'\n'); Proses.stdin.flush()
        return terima_email(확인표시)
    def Jalankan_perintah(baris_masukan):
        출력결과 = kirim(baris_masukan); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        terima_email(b'jkoros-native> ')
        file_Daftar = []
        for sertakan in argumen_ARRAY.include:
            if sertakan.is_dir():
                file_Daftar += [(str(data_posisi.relative_to(sertakan).with_suffix('')).replace('/', '.') + '.class', data_posisi.read_bytes()) for data_posisi in sorted(sertakan.rglob('*.class'))]
            else:
                file_Daftar.append((sertakan.name, sertakan.read_bytes()))
        file_Daftar = [(item_COUNT, tujuan_data) for item_COUNT, tujuan_data in file_Daftar if item_COUNT != Nama_2] + [(Nama_2, data)]
        for Upload_nama, Upload_data in file_Daftar:
            if len(Upload_data) > 16384 or len(Upload_nama.encode('utf-8')) > 63 or '\n' in Upload_nama or '\r' in Upload_nama:
                raise ValueError('tambah_entri 파일의 Nama_2/Ukuran 제한 초과: ' + Upload_nama)
            kirim('load ' + shlex.quote(Upload_nama), b'hex> ')
            for 순번 in range(0, len(Upload_data), 64): kirim(Upload_data[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in kirim('.'): raise RuntimeError('upload failed: ' + Upload_nama)
            갈무리자료 = kirim('hex ' + shlex.quote(Upload_nama))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Upload_data: raise RuntimeError('upload verification failed')
        if area_VALUE == '.java' and Jalankan_perintah('javac ' + shlex.quote(Nama_2)) != 0: return 1
        실행가능파일 = argumen_ARRAY.file.stem + '.elf'
        if area_VALUE == '.c' and Jalankan_perintah('cc ' + shlex.quote(Nama_2) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        apl = 'java ' + shlex.quote(argumen_ARRAY.class_name or argumen_ARRAY.file.stem) if area_VALUE in ('.java', '.class') else ('python ' if area_VALUE == '.py' else 'run ') + shlex.quote(Nama_2)
        if area_VALUE == '.jar': apl = 'java -jar ' + shlex.quote(Nama_2)
        if area_VALUE == '.c': apl = 'run ' + shlex.quote(실행가능파일)
        if argumen_ARRAY.linux: apl = 'run --linux ' + shlex.quote(Nama_2)
        if argumen_ARRAY.arguments: apl += ' ' + ' '.join(shlex.quote(string_data) for string_data in argumen_ARRAY.arguments)
        return 0 if Jalankan_perintah(apl) == 0 else 1
    finally:
        if Proses.poll() is None:
            Proses.terminate()
            try: Proses.wait(timeout=5)
            except subprocess.TimeoutExpired: Proses.kill(); Proses.wait(timeout=5)
        pemilih.close(); Proses.stdin.close(); Proses.stdout.close()


if __name__ == '__main__':
    raise SystemExit(jalankan())
