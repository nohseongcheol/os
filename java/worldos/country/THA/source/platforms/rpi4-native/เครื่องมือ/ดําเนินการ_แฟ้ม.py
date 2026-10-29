#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. โฮสต์ 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from ดําเนินการ_คําสั่ง import คําสั่ง


def เรียกใช้งาน():
    ตัวแยกวิเคราะห์ = argparse.ArgumentParser(description=__doc__)
    ตัวแยกวิเคราะห์.add_argument('file', type=Path)
    ตัวแยกวิเคราะห์.add_argument('arguments', nargs='*')
    ตัวแยกวิเคราะห์.add_argument('--class-name', help='패키지가 있는 .class의 전체 ชื่อ(예: ตรวจสอบความถูกต้อง.การทดสอบ_รวม)')
    ตัวแยกวิเคราะห์.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI ใช้_ค่า')
    ตัวแยกวิเคราะห์.add_argument('--vnc', help='예: 127.0.0.1:2')
    ตัวแยกวิเคราะห์.add_argument('--include', action='append', type=Path, default=[], help='ผนวก_รายการ class แฟ้ม 또는 class 디렉터리(패키지 ชื่อ 유지)')
    อาร์กิวเมนต์_อาร์เรย์ = ตัวแยกวิเคราะห์.parse_args()
    ข้อมูล = อาร์กิวเมนต์_อาร์เรย์.file.read_bytes()
    if อาร์กิวเมนต์_อาร์เรย์.class_name and อาร์กิวเมนต์_อาร์เรย์.file.suffix != '.class': ตัวแยกวิเคราะห์.error('--class-name은 .class 입력에서 사용합니다.')
    ชื่อ = อาร์กิวเมนต์_อาร์เรย์.class_name + '.class' if อาร์กิวเมนต์_อาร์เรย์.class_name else อาร์กิวเมนต์_อาร์เรย์.file.name
    if len(ข้อมูล) > 16384 or not 1 <= len(ชื่อ.encode('utf-8')) <= 63 or '\n' in ชื่อ or '\r' in ชื่อ:
        ตัวแยกวิเคราะห์.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    ประเภท_ค่า = '.elf' if ข้อมูล[:4] == b'\x7fELF' else อาร์กิวเมนต์_อาร์เรย์.file.suffix
    if อาร์กิวเมนต์_อาร์เรย์.linux and ประเภท_ค่า != '.elf': ตัวแยกวิเคราะห์.error('--linux는 ELF 바이너리에만 사용합니다.')
    if ประเภท_ค่า not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        ตัวแยกวิเคราะห์.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(อาร์กิวเมนต์_อาร์เรย์.arguments) > 7 or any(len(สตริง_ข้อมูล.encode('utf-8')) > 255 or '\n' in สตริง_ข้อมูล or '\r' in สตริง_ข้อมูล for สตริง_ข้อมูล in อาร์กิวเมนต์_อาร์เรย์.arguments):
        ตัวแยกวิเคราะห์.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    ตัวเลือก = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if อาร์กิวเมนต์_อาร์เรย์.vnc: ตัวเลือก += ['-vnc', อาร์กิวเมนต์_อาร์เรย์.vnc]
    โพรเซส = subprocess.Popen(คําสั่ง() + ตัวเลือก, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ตัวเลือก_582fe3b9 = selectors.DefaultSelector(); ตัวเลือก_582fe3b9.register(โพรเซส.stdout, selectors.EVENT_READ)
    def รับ_อีเมล(มาร์กเกอร์, 시간제한=45):
        ผลผลิต = bytearray(); สิ้นสุดการโทร_ออฟเซต = time.monotonic() + 시간제한
        while มาร์กเกอร์ not in ผลผลิต:
            if time.monotonic() > สิ้นสุดการโทร_ออฟเซต: raise RuntimeError('UART timeout: ' + ผลผลิต.decode('utf-8', 'replace'))
            for 누름값, _ in ตัวเลือก_582fe3b9.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: ผลผลิต.extend(조각)
            if b'PANIC:' in ผลผลิต or b'FAIL ' in ผลผลิต: raise RuntimeError(ผลผลิต.decode('utf-8', 'replace'))
            if โพรเซส.poll() is not None: raise RuntimeError('QEMU exited: ' + ผลผลิต.decode('utf-8', 'replace'))
        return bytes(ผลผลิต)
    def ส่ง(บรรทัด, มาร์กเกอร์=b'jkoros-native> '):
        โพรเซส.stdin.write(บรรทัด.encode('utf-8') + b'\n'); โพรเซส.stdin.flush()
        return รับ_อีเมล(มาร์กเกอร์)
    def ดําเนินการ_คําสั่ง(บรรทัด):
        ผลผลิต = ส่ง(บรรทัด); sys.stdout.buffer.write(ผลผลิต); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', ผลผลิต)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        รับ_อีเมล(b'jkoros-native> ')
        แฟ้ม_รายการ = []
        for รวม_e6c90571 in อาร์กิวเมนต์_อาร์เรย์.include:
            if รวม_e6c90571.is_dir():
                แฟ้ม_รายการ += [(str(ข้อมูล_ตําแหน่ง.relative_to(รวม_e6c90571).with_suffix('')).replace('/', '.') + '.class', ข้อมูล_ตําแหน่ง.read_bytes()) for ข้อมูล_ตําแหน่ง in sorted(รวม_e6c90571.rglob('*.class'))]
            else:
                แฟ้ม_รายการ.append((รวม_e6c90571.name, รวม_e6c90571.read_bytes()))
        แฟ้ม_รายการ = [(개수, ปลายทาง_ข้อมูล) for 개수, ปลายทาง_ข้อมูล in แฟ้ม_รายการ if 개수 != ชื่อ] + [(ชื่อ, ข้อมูล)]
        for อัปโหลด_ชื่อ, อัปโหลด_ข้อมูล in แฟ้ม_รายการ:
            if len(อัปโหลด_ข้อมูล) > 16384 or len(อัปโหลด_ชื่อ.encode('utf-8')) > 63 or '\n' in อัปโหลด_ชื่อ or '\r' in อัปโหลด_ชื่อ:
                raise ValueError('ผนวก_รายการ 파일의 ชื่อ/ขนาด 제한 초과: ' + อัปโหลด_ชื่อ)
            ส่ง('load ' + shlex.quote(อัปโหลด_ชื่อ), b'hex> ')
            for 순번 in range(0, len(อัปโหลด_ข้อมูล), 64): ส่ง(อัปโหลด_ข้อมูล[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in ส่ง('.'): raise RuntimeError('upload failed: ' + อัปโหลด_ชื่อ)
            갈무리자료 = ส่ง('hex ' + shlex.quote(อัปโหลด_ชื่อ))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != อัปโหลด_ข้อมูล: raise RuntimeError('upload verification failed')
        if ประเภท_ค่า == '.java' and ดําเนินการ_คําสั่ง('javac ' + shlex.quote(ชื่อ)) != 0: return 1
        แฟ้มปฏิบัติการ_รูป = อาร์กิวเมนต์_อาร์เรย์.file.stem + '.elf'
        if ประเภท_ค่า == '.c' and ดําเนินการ_คําสั่ง('cc ' + shlex.quote(ชื่อ) + ' -o ' + shlex.quote(แฟ้มปฏิบัติการ_รูป)) != 0: return 1
        แอป = 'java ' + shlex.quote(อาร์กิวเมนต์_อาร์เรย์.class_name or อาร์กิวเมนต์_อาร์เรย์.file.stem) if ประเภท_ค่า in ('.java', '.class') else ('python ' if ประเภท_ค่า == '.py' else 'run ') + shlex.quote(ชื่อ)
        if ประเภท_ค่า == '.jar': แอป = 'java -jar ' + shlex.quote(ชื่อ)
        if ประเภท_ค่า == '.c': แอป = 'run ' + shlex.quote(แฟ้มปฏิบัติการ_รูป)
        if อาร์กิวเมนต์_อาร์เรย์.linux: แอป = 'run --linux ' + shlex.quote(ชื่อ)
        if อาร์กิวเมนต์_อาร์เรย์.arguments: แอป += ' ' + ' '.join(shlex.quote(สตริง_ข้อมูล) for สตริง_ข้อมูล in อาร์กิวเมนต์_อาร์เรย์.arguments)
        return 0 if ดําเนินการ_คําสั่ง(แอป) == 0 else 1
    finally:
        if โพรเซส.poll() is None:
            โพรเซส.terminate()
            try: โพรเซส.wait(timeout=5)
            except subprocess.TimeoutExpired: โพรเซส.kill(); โพรเซส.wait(timeout=5)
        ตัวเลือก_582fe3b9.close(); โพรเซส.stdin.close(); โพรเซส.stdout.close()


if __name__ == '__main__':
    raise SystemExit(เรียกใช้งาน())
