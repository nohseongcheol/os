#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. hos 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from laksanakan_perintah import Perintah


def Jalan():
    penghurai = argparse.ArgumentParser(description=__doc__)
    penghurai.add_argument('file', type=Path)
    penghurai.add_argument('arguments', nargs='*')
    penghurai.add_argument('--class-name', help='패키지가 있는 .class의 전체 Nama(예: sahkan.ujian_pakej)')
    penghurai.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    penghurai.add_argument('--vnc', help='예: 127.0.0.1:2')
    penghurai.add_argument('--include', action='append', type=Path, default=[], help='Tambah_pemasukan class Fail 또는 class 디렉터리(패키지 Nama 유지)')
    argumen_ARRAY = penghurai.parse_args()
    data = argumen_ARRAY.file.read_bytes()
    if argumen_ARRAY.class_name and argumen_ARRAY.file.suffix != '.class': penghurai.error('--class-name은 .class 입력에서 사용합니다.')
    Nama = argumen_ARRAY.class_name + '.class' if argumen_ARRAY.class_name else argumen_ARRAY.file.name
    if len(data) > 16384 or not 1 <= len(Nama.encode('utf-8')) <= 63 or '\n' in Nama or '\r' in Nama:
        penghurai.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    bidang_VALUE = '.elf' if data[:4] == b'\x7fELF' else argumen_ARRAY.file.suffix
    if argumen_ARRAY.linux and bidang_VALUE != '.elf': penghurai.error('--linux는 ELF 바이너리에만 사용합니다.')
    if bidang_VALUE not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        penghurai.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argumen_ARRAY.arguments) > 7 or any(len(rentetan_data.encode('utf-8')) > 255 or '\n' in rentetan_data or '\r' in rentetan_data for rentetan_data in argumen_ARRAY.arguments):
        penghurai.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Opsyen = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argumen_ARRAY.vnc: Opsyen += ['-vnc', argumen_ARRAY.vnc]
    Proses = subprocess.Popen(Perintah() + Opsyen, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    준비선택기 = selectors.DefaultSelector(); 준비선택기.register(Proses.stdout, selectors.EVENT_READ)
    def 수신하기(penanda, 시간제한=45):
        출력결과 = bytearray(); tamat_Ofset = time.monotonic() + 시간제한
        while penanda not in 출력결과:
            if time.monotonic() > tamat_Ofset: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in 준비선택기.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Proses.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def e_mel_9aee63bd(baris, penanda=b'jkoros-native> '):
        Proses.stdin.write(baris.encode('utf-8') + b'\n'); Proses.stdin.flush()
        return 수신하기(penanda)
    def laksanakan_perintah(baris):
        출력결과 = e_mel_9aee63bd(baris); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        fail_Senarai = []
        for 포함항목 in argumen_ARRAY.include:
            if 포함항목.is_dir():
                fail_Senarai += [(str(data_jawatan.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', data_jawatan.read_bytes()) for data_jawatan in sorted(포함항목.rglob('*.class'))]
            else:
                fail_Senarai.append((포함항목.name, 포함항목.read_bytes()))
        fail_Senarai = [(item_COUNT, destinasi_data) for item_COUNT, destinasi_data in fail_Senarai if item_COUNT != Nama] + [(Nama, data)]
        for Upload_nama, Upload_data in fail_Senarai:
            if len(Upload_data) > 16384 or len(Upload_nama.encode('utf-8')) > 63 or '\n' in Upload_nama or '\r' in Upload_nama:
                raise ValueError('Tambah_pemasukan 파일의 Nama/Saiz 제한 초과: ' + Upload_nama)
            e_mel_9aee63bd('load ' + shlex.quote(Upload_nama), b'hex> ')
            for 순번 in range(0, len(Upload_data), 64): e_mel_9aee63bd(Upload_data[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in e_mel_9aee63bd('.'): raise RuntimeError('upload failed: ' + Upload_nama)
            갈무리자료 = e_mel_9aee63bd('hex ' + shlex.quote(Upload_nama))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Upload_data: raise RuntimeError('upload verification failed')
        if bidang_VALUE == '.java' and laksanakan_perintah('javac ' + shlex.quote(Nama)) != 0: return 1
        fail_boleh_laku_imej = argumen_ARRAY.file.stem + '.elf'
        if bidang_VALUE == '.c' and laksanakan_perintah('cc ' + shlex.quote(Nama) + ' -o ' + shlex.quote(fail_boleh_laku_imej)) != 0: return 1
        aplikasi = 'java ' + shlex.quote(argumen_ARRAY.class_name or argumen_ARRAY.file.stem) if bidang_VALUE in ('.java', '.class') else ('python ' if bidang_VALUE == '.py' else 'run ') + shlex.quote(Nama)
        if bidang_VALUE == '.jar': aplikasi = 'java -jar ' + shlex.quote(Nama)
        if bidang_VALUE == '.c': aplikasi = 'run ' + shlex.quote(fail_boleh_laku_imej)
        if argumen_ARRAY.linux: aplikasi = 'run --linux ' + shlex.quote(Nama)
        if argumen_ARRAY.arguments: aplikasi += ' ' + ' '.join(shlex.quote(rentetan_data) for rentetan_data in argumen_ARRAY.arguments)
        return 0 if laksanakan_perintah(aplikasi) == 0 else 1
    finally:
        if Proses.poll() is None:
            Proses.terminate()
            try: Proses.wait(timeout=5)
            except subprocess.TimeoutExpired: Proses.kill(); Proses.wait(timeout=5)
        준비선택기.close(); Proses.stdin.close(); Proses.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Jalan())
