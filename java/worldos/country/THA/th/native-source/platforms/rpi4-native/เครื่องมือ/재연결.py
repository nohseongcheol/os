#!/usr/bin/env python3
"""การกระจาย_ค่า 묶음에서 libassh/TinyCC를 교체하고 เอง 커널을 ลองอีกครั้ง_ค่า 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

แสดง_ราก = Path(__file__).resolve().parent


def ดําเนินการ_คําสั่ง(คํา_ข้อความ):
    subprocess.check_call([str(รายการ_ค่า) for รายการ_ค่า in คํา_ข้อความ], cwd=str(แสดง_ราก))


def เรียกใช้งาน():
    ตัวแยกวิเคราะห์_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 ยืนยัน')
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a ใช้_ค่า')
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 ลองอีกครั้ง_ค่า 컴파일하고 커널에 탑재')
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    อาร์กิวเมนต์ = ตัวแยกวิเคราะห์_48ee4b1b.parse_args()
    명세 = json.loads((แสดง_ราก / 'relink.json').read_text())
    สร้าง = แสดง_ราก / 'build'
    새묶음 = สร้าง / 'relinked'
    새묶음.mkdir(exist_ok=True)
    คอมไพเลอร์_เครื่องมือ = os.environ.get('ARM64_CC', 'clang')
    หัวต่อ = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    เก็บถาวร_เครื่องมือ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    ระยะไกล_การตั้งค่า = json.loads((สร้าง / 'remote/libassh-build.json').read_text())
    ตั้งค่า = ระยะไกล_การตั้งค่า['flags']
    if อาร์กิวเมนต์.libassh_archive:
        ความปลอดภัย_รวม = อาร์กิวเมนต์.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', แสดง_ราก / 'ระยะไกล_ค่า', '-I', แสดง_ราก / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for ชื่อ in ระยะไกล_การตั้งค่า['sources']:
            ปลายทาง_ค่า_a0fbc067 = 새묶음 / (Path(ชื่อ).stem + '.o')
            ดําเนินการ_คําสั่ง([คอมไพเลอร์_เครื่องมือ] + ตั้งค่า + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', แสดง_ราก / ชื่อ, '-o', ปลายทาง_ค่า_a0fbc067])
            목적들.append(ปลายทาง_ค่า_a0fbc067)
        ความปลอดภัย_รวม = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            ดําเนินการ_คําสั่ง([เก็บถาวร_เครื่องมือ, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(ความปลอดภัย_รวม)
    if อาร์กิวเมนต์.tinycc:
        if not อาร์กิวเมนต์.sdk:
            ตัวแยกวิเคราะห์_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = อาร์กิวเมนต์.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            ตัวแยกวิเคราะห์_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [การเลือก_ค่า for การเลือก_ค่า in ตั้งค่า if การเลือก_ค่า != '-mgeneral-regs-only']
        ปลายทาง_ค่า_a0fbc067 = 새묶음 / 'คอมไพเลอร์_เครื่องมือ.o'
        ดําเนินการ_คําสั่ง([คอมไพเลอร์_เครื่องมือ] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', แสดง_ราก / '시언어번역기', '-I', แสดง_ราก / 'vendor/tinycc', '-I', แสดง_ราก / 'ผู้ใช้',
             '-I', สร้าง / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', แสดง_ราก / '시언어번역기/คอมไพเลอร์_เครื่องมือ.c', '-o', ปลายทาง_ค่า_a0fbc067])
        ดําเนินการ_คําสั่ง([หัวต่อ, '--gc-sections', '-T', แสดง_ราก / 'ผู้ใช้/ลิงก์_การนําทาง.ld', '-z', 'max-page-size=4096',
             '-o', สร้าง / 'user/cc.elf', สร้าง / 'user/start.o', สร้าง / 'user/runtime.o', ปลายทาง_ค่า_a0fbc067] +
             [สร้าง / 'ccompiler' / (ชื่อ + '.o') for ชื่อ in ('รันไทม์_สนับสนุน', 'เรียกใช้งาน', '미리번역', 'ส่งคืน_บริดจ์')] +
             [สร้าง / 'user' / (ชื่อ + '.o') for ชื่อ in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = สร้าง / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((สร้าง / 'user/cc.elf').stat().st_size), 머리.read_text()))
        ดําเนินการ_คําสั่ง([คอมไพเลอร์_เครื่องมือ] + ตั้งค่า + ['-c', สร้าง / 'programs.S', '-o', แสดง_ราก / 'objects/programs.o'])
        ดําเนินการ_คําสั่ง([คอมไพเลอร์_เครื่องมือ] + ตั้งค่า + ['-std=c11', '-I', แสดง_ราก / 'posix-kor/arm64-native/포함', '-I', สร้าง,
             '-c', แสดง_ราก / 'เครื่อง/ผู้ใช้.c', '-o', แสดง_ราก / 'objects/user.o'])
    ดําเนินการ_คําสั่ง([หัวต่อ, '--gc-sections', '-T', แสดง_ราก / '부팅/ลิงก์_การนําทาง.ld', '-o', 새묶음 / 'kernel.elf'] +
         [แสดง_ราก / เส้นทาง for เส้นทาง in 명세['objects']] + ['--start-group'] +
         [ความปลอดภัย_รวม if เส้นทาง == 'objects/libassh.a' else แสดง_ราก / เส้นทาง for เส้นทาง in 명세['libraries']] + ['--end-group'])
    ดําเนินการ_คําสั่ง([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    แฮช_แฟ้ม = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if อาร์กิวเมนต์.verify and แฮช_แฟ้ม != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + แฮช_แฟ้ม)
    print('RELINK PASS', แฮช_แฟ้ม, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    เรียกใช้งาน()
